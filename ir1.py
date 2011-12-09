import compiler
from compiler.ast import *

class ArithInstr(Node):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def getChildren(self):
        return [self.lhs] + self.rhs

    def getChildNodes(self):
        return [self.lhs] + self.rhs

    def __repr__(self):
        return "%s(%s, [%s])" % (self.__class__.__name__, \
                                 repr(self.lhs), \
                                 ','.join([repr(c) for c in self.rhs]))
    

class IntAddInstr(ArithInstr):
    def __init__(self, lhs, rhs):
        ArithInstr.__init__(self, lhs, rhs)

class IntSubInstr(ArithInstr):
    def __init__(self, lhs, rhs):
        ArithInstr.__init__(self, lhs, rhs)

class IntLEAInstr(ArithInstr):
    def __init__(self, lhs, rhs):
        ArithInstr.__init__(self, lhs, rhs)

class IntMoveInstr(ArithInstr):
    def __init__(self, lhs, rhs):
        ArithInstr.__init__(self, lhs, rhs)


class IntNegInstr(ArithInstr):
    def __init__(self, lhs, rhs):
        ArithInstr.__init__(self, lhs, rhs)

class Call(Node):
    def __init__(self, name, lhs, rhs):
        self.name = name
        self.lhs = lhs
        self.rhs = rhs

    def getChildren(self):
        return []

    def getChildNodes(self):
        return []

    def __repr__(self):
        return "%s <- call %s(%s)" % (repr(self.lhs), self.name, \
                                 ','.join([repr(c) for c in self.rhs]))

class Register(Node):
    def __init__(self, name):
        self.name = name

    def getChildren(self):
        return []

    def getChildNodes(self):
        return []

    def __repr__(self):
        return "Register(%s)" % self.name

def assigned_vars(n):
    if isinstance(n, Stmt):
        return reduce(lambda a,b: a | b, \
                      [assigned_vars(s) for s in n.nodes], set([]))
    elif isinstance(n, ArithInstr):
        if isinstance(n.lhs, Name):
            return set([n.lhs.name])
        else:
            return set([])
    elif isinstance(n, Call):
        if n.lhs:
            return set([n.lhs.name])
        else:
            return set([])
    else:
        return set([])
