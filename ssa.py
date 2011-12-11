from print_visitor3 import PrintVisitor3
from ir2 import *
from ir_x86_3 import *

printIR = False

def countStmtVars(node):
    if isinstance(node,IntMoveInstr):
        if 'tmp' not in node.lhs.name:
            if node.lhs.name not in elseVars:
                testVars[node.lhs.name] = 1
            else:
                testVars[node.lhs.name] += 1
            if isinstance(stmt,If):
                TbranchTest,TbranchElse = countVars(stmt)
                for var in TbranchTest:
                    if var in elseVars:
                        testVars[var]+=TbranchTest[var]
                    else:
                        testVars[var] =TbranchTest[var]
                for var in TbranchElse:
                    if var in elseVars:
                        testVars[var]+=TbranchElse[var]
                    else:
                        testVars[var] =TbranchElse[var]

def countVars(IfNode,testVars={},elseVars={}):
    for stmt in IfNode.tests[0]:
        if isinstance(stmt,IntMoveInstr):
            #if 'tmp' not in stmt.lhs.name and 'list' not in node.lhs.name and 'letify' not in node.lhs.name:
            if '_' not in stmt.lhs.name:
                if stmt.lhs.name not in testVarz:
                    testVarz[stmt.lhs.name] = 1
                else:
                    testVars[stmt.lhs.name] += 1
        if isinstance(stmt,Stmt):
            for node in stmt:
                if isinstance(node,IntMoveInstr):
                    #if 'tmp' not in node.lhs.name and 'list' not in node.lhs.name and 'letify' not in node.lhs.name:
                    if '_' not in node.lhs.name:
                        if node.lhs.name not in testVars:
                            testVars[node.lhs.name] = 1
                        else:
                            testVars[node.lhs.name] += 1
                if isinstance(stmt,If):
                    TbranchTest,TbranchElse = countVars(stmt)
                    for var in TbranchTest:
                        if var in elseVars:
                            testVars[var]+=TbranchTest[var]
                        else:
                            testVars[var] =TbranchTest[var]
                    for var in TbranchElse:
                        if var in elseVars:
                            testVars[var]+=TbranchElse[var]
                        else:
                            testVars[var] =TbranchElse[var]
    for stmt in IfNode.else_:
        if isinstance(stmt,IntMoveInstr):
            #if 'tmp' not in stmt.lhs.name and 'list' not in stmt.lhs.name and 'letify' not in stmt.lhs.name:
            if '_' not in stmt.lhs.name:
                if stmt.lhs.name not in elseVars:
                    elseVars[stmt.lhs.name] = 1
                else:
                    elseVars[stmt.lhs.name] += 1
        if isinstance(stmt,Stmt):
            for node in stmt:
                if isinstance(stmt,IntMoveInstr):
                    #if 'tmp' not in stmt.lhs.name and 'list' not in stmt.lhs.name and 'letify' not in stmt.lhs.name:
                    if '_' not in stmt.lhs.name:
                        if stmt.lhs.name not in elseVars:
                            elseVars[stmt.lhs.name] = 1
                        else:
                            elseVars[stmt.lhs.name] += 1
        if isinstance(stmt,If):
            EbranchTest,EbranchElse = countVars(stmt)
            for var in EbranchTest:
                if var in elseVars:
                    elseVars[var]+=EbranchTest[var]
                else:
                    elseVars[var] =EbranchTest[var]
            for var in EbranchElse:
                if var in elseVars:
                    elseVars[var]+=EbranchElse[var]
                else:
                    elseVars[var] =EbranchElse[var]
    
    return testVars,elseVars

def rename(nameNode, varz, ptrs={}):
    name = nameNode.name
    if name in varz:
        if '_' not in nameNode.name:
            
            newName = name+'@'+str(varz[name])
            nameNode.name = newName
            ptrs[name].append(nameNode)
    
    return nameNode

def update(nameNode, varz, ptrs={}):
    name = nameNode.name
    if '_' not in name:
        if name not in varz:
            varz[name] = 1
        else:
            varz[name] += 1
        ptrs[name] = []

def merge(tPtrs,ePtrs,varz):
    
    print 'tPtrs:',tPtrs['x']
    print 'ePtrs:',ePtrs['x']
    ptrs = tPtrs.copy()
    
    for var,refs in ePtrs.items():
        if var in ptrs:
            refs = ptrs[var] + refs
            
            varz[var] += 1
            for nameNode in refs:
                nameNode.name = '%s@%d'%(var,varz[var])
        else:
            ptrs[var] = refs
    print ' ptrs:', ptrs['x']
    print
    return ptrs

def makeSSA(funs):
    #'vars' is a keyword in python so i spellled with a z
    varz = {}
    for fun in funs:
        if printIR == True:
            print PrintVisitor3().preorder(fun)
        else:
            ssaStmt(fun.code,varz)
                    
        #for node in fun.code.nodes:
        #   print node
    return funs

def ssaStmt(stmt, varz,ptrs={}):
    for node in stmt.nodes:
        ptrs = ssaNode(node,varz,ptrs)
    return ptrs

def ssaNode(node, varz, ptrs={}):
    if isinstance(node,If):
        tPtrs = ssaStmt(node.tests[0][1], varz, ptrs.copy())
        ePtrs = ssaStmt(node.else_, varz, ptrs)
        if tPtrs != ePtrs:
            ptrs = merge(tPtrs, ePtrs, varz)
    if isinstance(node,IntMoveInstr):
        update(node.lhs,varz,ptrs)
        rename(node.lhs,varz,ptrs)
        if isinstance(node.rhs[0],Name):
            rename(node.rhs[0], varz,ptrs)
    if isinstance(node,Push):
        if isinstance(node.arg,Name):
            rename(node.arg,varz,ptrs)
    return ptrs
