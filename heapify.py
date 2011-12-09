from vis import Visitor
from free_vars import FreeVarsVisitor
from compiler.ast import *
from explicit import *
from explicate2 import ExplicateVisitor2
from find_locals import FindLocalsVisitor
from compiler_utilities import *

class FreeInFunVisitor(FreeVarsVisitor):

    def visitLambda(self, n):
        local_vars = FindLocalsVisitor().preorder(n.code)
        free_in_fun = FreeVarsVisitor().preorder(n.code)
        return (free_in_fun - local_vars) - set(n.argnames)

    def visitName(self, n):
        return set([])

    def visitIf(self, n):
        return self.dispatch(n.tests[0][0]) | \
               self.dispatch(n.tests[0][1]) | \
               self.dispatch(n.else_)

    def visitWhile(self, n):
        return self.dispatch(n.test) | \
               self.dispatch(n.body)

class HeapifyVisitor(Visitor):

    def visitModule(self, n):
        local_vars = FindLocalsVisitor().preorder(n.node)
        free_in_fun = FreeInFunVisitor().preorder(n.node)
        body = self.dispatch(n.node, local_vars & free_in_fun)
        local_inits = [Assign(nodes=[AssName(x, 'OP_ASSIGN')],
                              expr=ExplicateVisitor2().preorder(List([Const(0)]))) \
                       for x in local_vars & free_in_fun]
        return Module(n.doc, Stmt(local_inits + body.nodes))

    def visitLambda(self, n, vars_to_heapify):
        local_vars = FindLocalsVisitor().preorder(n.code)
        free_in_fun = FreeInFunVisitor().preorder(n.code)
        from_above = (vars_to_heapify - local_vars) - set(n.argnames)
        from_here = (local_vars | set(n.argnames)) & free_in_fun
        body = self.dispatch(n.code, from_above | from_here)
        local_inits = [Assign(nodes=[AssName(x, 'OP_ASSIGN')],
                              expr=ExplicateVisitor2().preorder(List([Const(0)]))) \
                       for x in local_vars & free_in_fun]

        param2new = {}
        params_free_in_fun = set(n.argnames) & free_in_fun
        for x in params_free_in_fun:
            param2new[x] = generate_name(x) 
        
        param_allocs = [Assign(nodes=[AssName(x, 'OP_ASSIGN')],
                               expr=ExplicateVisitor2().preorder(List([Const(0)]))) 
                        for x in params_free_in_fun]
        param_inits = [Discard(SetSubscript(Name(x), Const(0),
                                            Name(param2new[x])))
                       for x in params_free_in_fun]
        new_argnames = [param2new[x] if x in param2new else x 
                        for x in n.argnames]
        return Lambda(new_argnames, n.defaults, n.flags,
                      Stmt(param_allocs + param_inits + local_inits + body.nodes))

    def visitReturn(self, n, vars_to_heapify):
        return Return(self.dispatch(n.value, vars_to_heapify))

    def visitStmt(self, n, vars_to_heapify):
        ss  = [self.dispatch(s, vars_to_heapify) for s in n.nodes]
        return Stmt(ss)

    def visitPrintnl(self, n, vars_to_heapify):
        e = self.dispatch(n.nodes[0], vars_to_heapify)
        return Printnl([e], n.dest)

    def visitAssign(self, n, vars_to_heapify):
        rhs = self.dispatch(n.expr, vars_to_heapify)
        if isinstance(n.nodes[0], AssName):
            if n.nodes[0].name in vars_to_heapify:
                return Discard(SetSubscript(Name(n.nodes[0].name), Const(0), rhs))
            else:
                return Assign(nodes=n.nodes, expr=rhs)
        else:
            raise Exception('Heapify: unhandled lhs of assign')

    def visitIf(self, n, vars_to_heapify):
        test = self.dispatch(n.tests[0][0], vars_to_heapify)
        then = self.dispatch(n.tests[0][1], vars_to_heapify)
        else_ = self.dispatch(n.else_, vars_to_heapify)
        return If([(test, then)], else_)

    def visitWhile(self, n, vars_to_heapify):
        test = self.dispatch(n.test, vars_to_heapify)
        body = self.dispatch(n.body, vars_to_heapify)
        return While(test, body, n.else_)

    def visitConst(self, n, vars_to_heapify):
        return n

    def visitName(self, n, vars_to_heapify):
        if n.name in vars_to_heapify:
            return Subscript(Name(n.name), 'OP_APPLY', [Const(0)])
        else:
            return n

    def visitAdd(self, n, vars_to_heapify):
        left = self.dispatch(n.left, vars_to_heapify)
        right = self.dispatch(n.right, vars_to_heapify)
        return Add((left, right))

    def visitUnarySub(self, n, vars_to_heapify):
        return UnarySub(self.dispatch(n.expr, vars_to_heapify))
        
    def visitCallFunc(self, n, vars_to_heapify):
        return CallFunc(self.dispatch(n.node, vars_to_heapify),
                        [self.dispatch(a, vars_to_heapify) for a in n.args])

    def visitCompare(self, n, vars_to_heapify):
        left = self.dispatch(n.expr, vars_to_heapify)
        right = self.dispatch(n.ops[0][1], vars_to_heapify)
        return Compare(left, [(n.ops[0][0], right)])

    def visitAnd(self, n, vars_to_heapify):
        left = self.dispatch(n.nodes[0], vars_to_heapify)
        right = self.dispatch(n.nodes[1], vars_to_heapify)
        return And([left, right])

    def visitOr(self, n, vars_to_heapify):
        left = self.dispatch(n.nodes[0], vars_to_heapify)
        right = self.dispatch(n.nodes[1], vars_to_heapify)
        return Or([left, right])

    def visitIfExp(self, n, vars_to_heapify):
        test = self.dispatch(n.test, vars_to_heapify)
        then = self.dispatch(n.then, vars_to_heapify)
        else_ = self.dispatch(n.else_, vars_to_heapify)
        return IfExp(test, then, else_)

    def visitNot(self, n, vars_to_heapify):
        expr = self.dispatch(n.expr, vars_to_heapify)
        return Not(expr)

    def visitDict(self, n, vars_to_heapify):
        items = [(self.dispatch(k, vars_to_heapify),
                  self.dispatch(e, vars_to_heapify)) for (k, e) in n.items]
        return Dict(items)
    
    def visitList(self, n, vars_to_heapify):
        return List([self.dispatch(e) for e in n.nodes])

    def visitSubscript(self, n, vars_to_heapify):
        expr = self.dispatch(n.expr, vars_to_heapify)
        subs = [self.dispatch(e, vars_to_heapify) for e in n.subs]
        return Subscript(expr, n.flags, subs)

    def visitSetSubscript(self, n, vars_to_heapify):
        c = self.dispatch(n.container, vars_to_heapify)
        k = self.dispatch(n.key, vars_to_heapify)
        v = self.dispatch(n.val, vars_to_heapify)
        return SetSubscript(c, k, v)

    def visitDiscard(self, n, vars_to_heapify):
        e = self.dispatch(n.expr, vars_to_heapify)
        return Discard(e)

    def visitInjectFrom(self, n, vars_to_heapify):
        return InjectFrom(n.typ, self.dispatch(n.arg, vars_to_heapify))

    def visitProjectTo(self, n, vars_to_heapify):
        return ProjectTo(n.typ, self.dispatch(n.arg, vars_to_heapify))

    def visitGetTag(self, n, vars_to_heapify):
        return GetTag(self.dispatch(n.arg, vars_to_heapify))

    def visitLet(self, n, vars_to_heapify):
        rhs = self.dispatch(n.rhs, vars_to_heapify)
        body = self.dispatch(n.body, vars_to_heapify - set([n.var]))
        return Let(n.var, rhs, body)

