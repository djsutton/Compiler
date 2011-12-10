#! /usr/local/bin/python
import ssa2 as ssa
import pdb
import sys
import compiler
from compiler.ast import *
from ir_x86 import *
from explicit2 import PrintASTVisitor2
from heapify import HeapifyVisitor
from explicate3 import ExplicateVisitor3
from type_check2 import TypeCheckVisitor2
from closure_conversion import ClosureConversionVisitor
from flatten4 import FlattenVisitor4
from instruction_selection4 import InstrSelVisitor4
from register_alloc3 import RegisterAlloc3
from print_visitor3 import PrintVisitor3
from generate_x86_3 import GenX86Visitor3, string_constants
from generate_x86_1 import fun_prefix
from remove_structured_control import RemoveStructuredControl
from declassify import DeclassifyVisitor
from os.path import splitext
#from parse_p3 import P3Parser
debug = False

ifDepth = 0
def printIf(IfNode):
    global ifDepth
    ifDepth += 1
    print '  '*(ifDepth-1)+'If{'
    for stmt in IfNode.tests[0]:
        if isinstance(stmt,If):
            printIf(stmt)
        elif isinstance(stmt,Stmt):
            printStmt(stmt)
        else:
            print '  '*ifDepth+str(stmt)
    print '\n'
    for stmt in IfNode.else_:
        if isinstance(stmt,If):
            printIf(stmt)
        elif isinstance(stmt,Stmt):
            printStmt(stmt)
        else:
            print '  '*ifDepth+str(stmt)
    print '  '*(ifDepth-1)+'}',ssa.countVars(IfNode)
    ifDepth-=1
    return

def printStmt(stmt):
    global ifDepth
    ifDepth+=1
    print '  '*(ifDepth-1)+'Stmt{'
    for node in stmt:
        if isinstance(node,If):
            printIf(node)
        else:
            print '  '*ifDepth+str(node)
    ifDepth-=1
    print '  '*(ifDepth)+'}'
    return

if True:
    #pdb.set_trace()
    if debug:
        print 'starting'
    input_file_name = sys.argv[1]
    ast = compiler.parseFile(input_file_name)
#    input_file = open(input_file_name)
#    ast = P3Parser().parse(input_file.read())
    if debug:
        print 'finished parsing'
        print ast

    ast = DeclassifyVisitor().preorder(ast)
    if debug:
        print 'finished declassifying'
        print ast
        print PrintASTVisitor2().preorder(ast)
        print 'starting to explicate'

    ast = ExplicateVisitor3().preorder(ast)
    if debug:
        print 'finished explicating'
        print PrintASTVisitor2().preorder(ast)
        print 'starting to heapify'
        
    ast = HeapifyVisitor().preorder(ast)

    if debug:
        print 'finished heapifying'
        print PrintASTVisitor2().preorder(ast)        
        print 'type checking'
    TypeCheckVisitor2().preorder(ast)

    if debug:
        print 'starting closure conversion'
    ast = ClosureConversionVisitor().preorder(ast)

    if debug:
        print 'finished closure conversion'
        print PrintASTVisitor2().preorder(ast)
        print 'starting to flatten'
    instrs = FlattenVisitor4().preorder(ast)
    if debug:
        print 'finished flattening'
        print PrintASTVisitor2().preorder(instrs)
        print 'starting instruction selection'
        
    funs = InstrSelVisitor4().preorder(instrs)
    if debug:
        print 'finished instruction selection'
        for fun in funs:
            print PrintVisitor3().preorder(fun)
        print 'starting SSA generation'
  
    if False:
        for fun in funs:
            #fun.code.nodes.reverse()
            for node in fun.code.nodes:
                if isinstance(node,If):
                    printIf(node)
                else:
                    print node
    funs = ssa.makeSSA(funs)
    if True:
        for fun in funs:
            #fun.code.nodes.reverse()
            for node in fun.code.nodes:
                if isinstance(node,If):
                    printIf(node)
                else:
                    print node

    if debug:
        print 'finished making SSA'
        for fun in funs:
            print PrintVisitor3().preorder(fun)
        print 'starting register allocation'

    new_funs = []
    for fun in funs:
        new_funs += [RegisterAlloc3().allocate_registers(fun,
                                           input_file_name + '_' + fun.name)]
    funs = new_funs
    if debug:
        print 'finished register allocation'

    if False:
        for fun in funs:
            print PrintVisitor3().preorder(fun)

    for fun in funs:
        fun.code = RemoveStructuredControl().preorder(fun.code)
    if debug:
        print 'finished removing structured control'
        for fun in funs:
            print PrintVisitor3().preorder(fun)

    x86 = GenX86Visitor3().preorder(Stmt(funs))
    if debug:
        print 'finished generating x86'

    x86 = ('.globl %smain' % fun_prefix) + x86

    if len(string_constants.keys()) > 0:
        if sys.platform == 'darwin':
            strings = '''\n\t.cstring\n'''
        else:
            strings = ''
        for (var,str) in string_constants.items():
            if sys.platform == 'darwin':
                strings += ('''%s:\n\t.ascii "%s\\0"\n''' % (var, str)) 
            else:
                strings += ('''\n%s:\n\t.string "%s"\n''' % (var, str))
    else:
        strings = ''
    x86 = strings + '\t.text\n' + x86
    asm_file = open(splitext(input_file_name)[0] + '.s', 'w')
    print >>asm_file, x86

'''except EOFError:
    print "Could not open file %s." % sys.argv[1]
except Exception, e:
    print e.args[0]
    exit(-1)'''
