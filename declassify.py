from explicit import *
from vis import Visitor
from compiler_utilities import *
from find_locals import FindLocalsVisitor
from explicate1 import pure

def letify_list(exprs, var_list, k):
    if len(exprs) == 0:
        return k(var_list)
    else:
        hd = exprs[0]
        tl = exprs[1:]
        if pure(hd):
            return letify_list(tl, var_list + [hd], k)
        else:
            n = generate_name('letify')
            return Let(n, hd, letify_list(tl, var_list + [Name(n)], k))

class DeclassifyVisitor(Visitor):
    def visitModule(self, n):
        local_vars = FindLocalsVisitor().preorder(n.node)
        return Module(n.doc, self.dispatch(n.node, None, [], local_vars))

    def visitStmt(self, n, cls, cls_attrs, vars):
        ss  = [self.dispatch(s, cls, cls_attrs, vars) for s in n.nodes]
        return Stmt(ss)

    def visitClass(self, n, cls, cls_attrs, vars):
        tmp = generate_name(n.name)
        my_attrs = FindLocalsVisitor().preorder(n.code)
        bases = [self.dispatch(b, cls, cls_attrs, vars) for b in n.bases]
        code = self.dispatch(n.code, tmp, my_attrs, vars)
        tmp_assign = Assign([AssName(n.name, 'OP_ASSIGN')], Name(tmp))
        return Stmt([Assign([AssName(tmp, 'OP_ASSIGN')],
                            CallFunc(Name('create_class'), [List(bases)]))] + \
                    [code] + \
                    [self.dispatch(tmp_assign, cls, cls_attrs, vars)])

    def visitPrintnl(self, n, cls, cls_attrs, vars):
        e = self.dispatch(n.nodes[0], cls, cls_attrs, vars)
        return Printnl([e], n.dest)

    def visitAssign(self, n, cls, cls_attrs, vars):
        rhs = self.dispatch(n.expr, cls, cls_attrs, vars)
        lhs = n.nodes[0]
        if isinstance(lhs, AssName):
            if cls:
                return Discard(CallFunc(Name('set_attr'),
                                        [Name(cls),
                                         Const(lhs.name),
                                         rhs]))
            else:
                return Assign(nodes=n.nodes, expr=rhs)
        elif isinstance(lhs, Subscript):
            c = self.dispatch(lhs.expr, cls, cls_attrs, vars)
            k = self.dispatch(lhs.subs[0], cls, cls_attrs, vars)
            return Assign(nodes=[Subscript(expr=c,subs=[k],flags=lhs.flags)], expr=rhs)
        elif isinstance(lhs, AssAttr):
            # AssAttr(Name('self'), 'x', 'OP_ASSIGN')
            expr = self.dispatch(lhs.expr, cls, cls_attrs, vars)
            return Discard(CallFunc(Name('set_attr'),
                                    [expr,
                                     Const(lhs.attrname),
                                     rhs]))
        else:
            raise Exception('unrecognized lhs in Assign: %s' % repr(lhs))

    def visitIf(self, n, cls, cls_attrs, vars):
        test = self.dispatch(n.tests[0][0], cls, cls_attrs, vars)
        then = self.dispatch(n.tests[0][1], cls, cls_attrs, vars)
        else_ = self.dispatch(n.else_, cls, cls_attrs, vars)
        return If([(test, then)], else_)

    def visitWhile(self, n, cls, cls_attrs, vars):
        test = self.dispatch(n.test, cls, cls_attrs, vars)
        body = self.dispatch(n.body, cls, cls_attrs, vars)
        return While(test, body, n.else_)

    def visitGetattr(self, n, cls, cls_attrs, vars):
        expr = self.dispatch(n.expr, cls, cls_attrs, vars)
        return CallFunc(Name('get_attr'),
                        [expr, Const(n.attrname)])

    def visitConst(self, n, cls, cls_attrs, vars):
        return n

    def visitName(self, n, cls, cls_attrs, vars):
        if n.name in cls_attrs and n.name in vars:
            return IfExp(CallFunc(Name('has_attr'), [Name(cls),
                                                     Const(n.name)]),
                         CallFunc(Name('get_attr'), [Name(cls),
                                                     Const(n.name)]),
                         n)
        elif n.name in cls_attrs:
            return CallFunc(Name('get_attr'), [Name(cls),
                                               Const(n.name)])
        else:
            return n

    def visitAdd(self, n, cls, cls_attrs, vars):
        left = self.dispatch(n.left, cls, cls_attrs, vars)
        right = self.dispatch(n.right, cls, cls_attrs, vars)
        return Add((left, right))

    def visitUnarySub(self, n, cls, cls_attrs, vars):
        return UnarySub(self.dispatch(n.expr, cls, cls_attrs, vars))

    def visitCallFunc(self, n, cls, cls_attrs, vars):
        rator = self.dispatch(n.node, cls, cls_attrs, vars)
        rands = [self.dispatch(a, cls, cls_attrs, vars) for a in n.args]

        if isinstance(rator, Name) and rator.name == 'input':
            return CallFunc(rator, rands)
        else:
            f = generate_name('rator')
            o = generate_name('obj')
            get_init = CallFunc(Name('get_function'),
                                [CallFunc(Name('get_attr'),
                                          [Name(f), Const('__init__')])])
            tmp = generate_name('_')
            return letify_list(rands, [],
                               lambda rands: \
                               Let(f, rator,
                                   IfExp(CallFunc(Name('is_class'), [Name(f)]),
                                         Let(o, CallFunc(Name('create_object'), [Name(f)]),
                                             IfExp(CallFunc(Name('has_attr'),
                                                            [Name(f), Const('__init__')]),
                                                   Let(tmp, CallFunc(get_init, [Name(o)] + rands),
                                                       Name(o)),
                                                   Name(o))),
                                         IfExp(CallFunc(Name('is_bound_method'), [Name(f)]),
                                               CallFunc(CallFunc(Name('get_function'), [Name(f)]),
                                                        [CallFunc(Name('get_receiver'),
                                                                  [Name(f)])] + rands),
                                               IfExp(CallFunc(Name('is_unbound_method'),
                                                              [Name(f)]),
                                                     CallFunc(CallFunc(Name('get_function'),
                                                                       [Name(f)]),
                                                              rands),
                                                     CallFunc(Name(f), rands))))))

    def visitCompare(self, n, cls, cls_attrs, vars):
        left = self.dispatch(n.expr, cls, cls_attrs, vars)
        op = n.ops[0][0]
        right = self.dispatch(n.ops[0][1], cls, cls_attrs, vars)
        return Compare(left, [(op, right)])

    def visitAnd(self, n, cls, cls_attrs, vars):
        left = self.dispatch(n.nodes[0], cls, cls_attrs, vars)
        right = self.dispatch(n.nodes[1], cls, cls_attrs, vars)
        return And([left, right])

    def visitOr(self, n, cls, cls_attrs, vars):
        left = self.dispatch(n.nodes[0], cls, cls_attrs, vars)
        right = self.dispatch(n.nodes[1], cls, cls_attrs, vars)
        return Or([left, right])

    def visitIfExp(self, n, cls, cls_attrs, vars):
        test = self.dispatch(n.test, cls, cls_attrs, vars)
        then = self.dispatch(n.then, cls, cls_attrs, vars)
        else_ = self.dispatch(n.else_, cls, cls_attrs, vars)
        return IfExp(test, then, else_, cls)

    def visitNot(self, n, cls, cls_attrs, vars):
        expr = self.dispatch(n.expr, cls, cls_attrs, vars)
        return Not(expr)

    def visitDict(self, n, cls, cls_attrs, vars):
        items = [(self.dispatch(k, cls, cls_attrs, vars),
                  self.dispatch(e, cls, cls_attrs, vars))
                 for (k, e) in n.items]
        return Dict(items)
    
    def visitList(self, n, cls, cls_attrs, vars):
        nodes = [self.dispatch(e, cls, cls_attrs, vars) for e in n.nodes]
        return List(nodes)

    def visitSubscript(self, n, cls, cls_attrs, vars):
        expr = self.dispatch(n.expr, cls, cls_attrs, vars)
        subs = [self.dispatch(e, cls, cls_attrs, vars) for e in n.subs]
        return Subscript(expr, n.flags, subs)

    def visitDiscard(self, n, cls, cls_attrs, vars):
        e = self.dispatch(n.expr, cls, cls_attrs, vars)
        return Discard(e)

    def visitFunction(self, n, cls, cls_attrs, vars):
        local_vars = FindLocalsVisitor().preorder(n.code)
        code = self.dispatch(n.code, None, [],
                             vars | set(n.argnames) | set(local_vars))
        if cls:
            f_tmp = generate_name(n.name)
            return Stmt([Function(n.decorators, f_tmp, n.argnames, n.defaults, n.flags, n.doc, code),
                         Discard(CallFunc(Name('set_attr'),
                                          [Name(cls),
                                           Const(n.name),
                                           Name(f_tmp)]))])
        else:
            return Function(n.decorators, n.name, n.argnames, n.defaults,
                            n.flags, n.doc, code)

    def visitReturn(self, n, cls, cls_attrs, vars):
        return Return(self.dispatch(n.value, cls, cls_attrs, vars))

    def visitLambda(self, n, cls, cls_attrs, vars):
        return Lambda(n.argnames, n.defaults, n.flags,
                      self.dispatch(n.code, None, [],
                                    vars | set(n.argnames)))
