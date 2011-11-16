#! /usr/bin/python
import compiler
import sys
import operator
import sets
from compiler.ast import *
import copy
import re

debug_flag = False


class x86_ir_move(Node):
	def __init__(self,src_name,dest_name):
		self.dest_name = dest_name
		self.src_name = src_name
	def __str__(self):
		return "x86_ir_move(" + str(self.src_name)+", " + str(self.dest_name)+")"
	def __repr__(self):
		return "x86_ir_move(" + repr(self.src_name)+", " + repr(self.dest_name)+")"
class x86_ir_add(Node):
	def __init__(self,left_name,right_name):
		self.right_name = right_name
		self.left_name = left_name
	def __repr__(self):
		return "x86_ir_add(" + repr(self.left_name)+", " + repr(self.right_name)+")"
class x86_ir_neg(Node):
	def __init__(self,src_name):
		self.src_name = src_name
		#remember neg takes the dest_name negates it and puts it back in the dest
	
class x86_ir_call(Node):
	def __init__(self,name):
		self.name = name
	def __repr__(self):
		return "x_86_ir_Call(" +repr(self.name)+")"
class x86_ir_call_star(Node):
	def __init__(self,pointer):
		self.pointer = pointer
	def __repr__(self):
	        return "x_86_ir_Call*(" +repr(self.pointer)+")"

class x86_ir_push(Node):
	def __init__(self,to_push):
		self.to_push = to_push
	def __repr__(self):
		return "x86_ir_push(" + repr(self.to_push) + ')'
class x86_ir_and(Node):
	#andl A, B A&B -> B (bitwise-and)
	def __init__(self,left_name,right_name):
		self.right_name = right_name
		self.left_name = left_name
	def __repr__(self):
		return "x86_ir_and(" + repr(self.left_name)+", " + repr(self.right_name)+")"
class x86_ir_or(Node):
	#orl A, B A|B -> B (bitwise-and)
	def __init__(self,left_name,right_name):
		self.right_name = right_name
		self.left_name = left_name
	def __repr__(self):
		return "x86_ir_or(" + repr(self.left_name)+", " + repr(self.right_name)+")"
class x86_ir_not(Node):
	#notl A    ~A -> A (bitwise complement)


	def __init__(self,src_name):
		self.src_name = src_name
class x86_ir_sar(Node):
	#sarl A, B B >> A -> B (where A is a constant)
	def __init__(self,src_name):
		self.src_name = src_name
	def __repr__(self):
		return "x86_ir_sar(" + repr(SHIFT)+", " + repr(self.src_name)+")"
class x86_ir_sal(Node):
	#sall A, B B << A -> B (where A is a constant)
	def __init__(self,src_name):
		self.src_name = src_name
	def __repr__(self):
		return "x86_ir_sal(" + repr(SHIFT)+", " + repr(self.src_name)+")"
class x86_ir_cmp(Node):
	def __init__(self,left_name,right_name):
		self.right_name = right_name
		self.left_name = left_name
	def __repr__(self):
		return "x86_ir_cmp(" + repr(self.left_name)+", " + repr(self.right_name)+")"
class x86_ir_movzbl(Node):
	def __init__(self,left_name,right_name):
		self.right_name = right_name
		self.left_name = left_name #this is reg al
	def __repr__(self):
		return "x86_ir_movzbl(" + repr(self.left_name)+", " + repr(self.right_name)+")"
class x86_ir_sete(Node):
	def __init__(self,junk):
		self.junk = -1
	def __repr__(self):
		return "x86_ir_sete()"
class x86_ir_setne(Node):
	def __init__(self,junk):
		self.junk = -1

	def __repr__(self):
		return "x86_ir_setne()"
class x86_ir_leave(Node):
	def __init__(self,junk):
		self.junk = junk
	def __repr__(self):
		return "x86_ir_leave()"
class x86_ir_ret(Node):
	def __init__(self,junk):
		self.junk = junk
	def __repr__(self):
		return "x86_ir_ret()"
class x86_ir_label(Node):
	def __init__(self,label):
		self.label = label
	def __repr__(self):
		return "x86_ir_label(label)"
class x86_ir_je(Node):
	def __init__(self,label):
		self.label = label
class x86_ir_jmp(Node):
	def __init__(self,label):
		self.label = label
class GetTag(Node):
	def __init__(self, arg):
		self.arg = arg
	def __str__(self):
		return "GetTag(" + str(self.arg)+")"
	def __repr__(self):
		return "GetTag(" + repr(self.arg)+")"
									
'''
pyobj set_subscript(pyobj c, pyobj key, pyobj val)
{
  switch (tag(c)) {
  case BIG_TAG: {
    big_pyobj* b = project_big(c);
    return subscript_assign(b, key, val);
  }
  default:
    printf("error in set subscript, not a list or dictionary\n");
    assert(0);
  }
  assert(0);
}
'''
class SetSubScript(Node):
	def __init__(self, c,key,val ):
		self.c = c
		self.key = key
		self.val = val
	def __str__(self):
		return "SetSubScript(" + str(self.c) +", "+ str(self.key)+", " + str(self.val)+")"
	def __repr__(self):
		return "SetSubScript(" + repr(self.c)+", " + repr(self.key)+", " + repr(self.val)+")"

class GetSubScript(Node):
	def __init__(self,c,key):
		self.c = c
		self.key = key
	def __str__(self):
		return "GetSubScript(" + str(self.c)+", " + str(self.key)+")"
	def __repr__(self):
		return "GetSubScript(" + repr(self.c)+", " + repr(self.key)+")"
class get_fun_ptr(Node):
	def __init__(self,name,params):
		self.name = name
		self.params = params
	def __repr__(self):
		return "get_fun_ptr(" + repr(self.name) + ", " + repr(self.params) + ")"
class get_free_vars(Node):
	def __init__(self,name):
		self.name = name
	def __repr__(self):
		return "get_free_vars(" + repr(self.name) +")"






class create_closure(Node):
	def __init__(self,name,enviroment):
		self.name = name
		self.enviroment = enviroment
	def __repr__(self):
		return "create_closure(" + repr(self.name) + ", " + repr(self.enviroment) + ")"
	
class CreateList(Node):
	def __init__(self,length,list_name,listItems):
		self.length = length
		self.list_name = list_name
		self.listItems = listItems
	def __repr__(self):
		return "CreateList(" + repr(self.length) + ", " + repr(self.list_name) + ", " + repr(self.listItems) +")"
	
class CreateListCall(Node):
	def __init__(self,length,list_name):
		self.length = length
		self.list_name = list_name
	def __repr__(self):
		return "CreateListCall(" + repr(self.length) + ", " + repr(self.list_name) + ")"
	

class CreateDict(Node):
	def __init__(self,dict_name,dictItems):
		self.dict_name = dict_name
		self.dictItems = dictItems
class CreateDictCall(Node):
	def __init__(self,dict_name):
		self.dict_name = dict_name
class InjectFrom(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def __repr__(self):
		return "InjectFrom(%s, %s)" % (repr(self.typ), repr(self.arg))
class ProjectTo(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def __repr__(self):
		return "ProjectTo(%s, %s)" % (repr(self.typ), repr(self.arg))
class Let(Node):
	def __init__(self, var, rhs, body):
		self.var = var
		self.rhs = rhs
		self.body = body
	def __str__(self):
		return "Let(%s, %s, %s)" % (str(self.var), str(self.rhs), str(self.body))
	def __repr__(self):
		return "Let(%s, %s, %s)" % (repr(self.var), repr(self.rhs), repr(self.body))


#my new classes for callingFuncs later on

class is_true(Node):
	def __init__(self,name):
		self.name = name
	def __repr__(self):
		return "is_true(" + repr(self.name) + ")"
class addBig(Node):
	def __init__(self,left_name,right_name):
		self.right_name = right_name
		self.left_name = left_name
	def __repr__(self):
		return "addBig(" + repr(self.left_name)+", " + repr(self.right_name)+")"
class ERROREXIT(Node):
	def __init__(self,error_code):
		self.error_code = error_code
	def __repr__(self):
		return "ERROREXIT('Type Error')"
class equalBig(Node):
	def __init__(self,left_name,right_name):
		self.right_name = right_name
		self.left_name = left_name
	def __repr__(self):
		return "equalBig(" + repr(self.left_name)+", " + repr(self.right_name)+")"
class nequalBig(Node):
	def __init__(self,left_name,right_name):
		self.right_name = right_name
		self.left_name = left_name
	def __repr__(self):
		return "nequalBig(" + repr(self.left_name)+", " + repr(self.right_name)+")"

class create_class(Node):
	def __init__(self,bases):
		self.bases = bases
	def __repr__(self):
		return "create_class(" + repr(self.bases) + ")"


class create_object(Node):
	def __init__(self,c):
		self.c = c
	def __repr__(self):
		return "create_object(" + repr(self.c) + ")"
class inherits(Node):
	def __init__(self,c1,c2):
		self.c1 = c1
		self.c2 = c2
	def __repr__(self):
		return "inherits(" + repr(self.c1) + ", " +repr(self.c2) + ")"

class get_class(Node):
	def __init__(self,o):
		self.o = o
	def __repr__(self):
		return "get_class(" + repr(self.o) + ")"
class is_class(Node):
	def __init__(self,c):
		self.c = c
	def __repr__(self):
		return "is_class("+ repr(self.c) + ")"
class get_receiver(Node):
	def __init__(self,o):
		self.o = o
	def __repr__(self):
		return "get_receiver(" + repr(self.o) + ")"
class get_function(Node):
	def __init__(self,o):
		self.o = o
	def __repr__(self):
		return "get_function(" + repr(self.o) + ")"

class has_attr(Node):
	def __init__(self,o,attr):
		self.o = o
		self.attr = attr
	def __repr__(self):
		return "has_attr(" + repr(self.o) + ", " +repr(self.attr) + ")"

class get_attr(Node):
	def __init__(self,c,attr):
		self.c = c
		self.attr = attr
	def __repr__(self):
		return "get_attr(" + repr(self.c) + ", " +repr(self.attr) + ")"

class set_attr(Node):
	def __init__(self,c,attr,val):
		self.c = c
		self.attr = attr
		self.val = val
	def __repr__(self):
		return "set_attr(" + repr(self.c) + ", " +repr(self.attr) +", " +repr(self.val) + ")"
class is_unbound_method(Node):
	def __init__(self,val):
		self.val = val
	def __repr__(self):
		return "is_unbound_method(" +repr(self.val) + ")"
class is_bound_method(Node):
	def __init__(self,val):
		self.val = val
	def __repr__(self):
		return "is_bound_method(" +repr(self.val) + ")"

if (len(sys.argv) > 1):
	f = open(sys.argv[1], 'r')
	data = f.read()
	f = open(sys.argv[1][0:-3] + ".s", 'w')
	if (len(sys.argv) > 2):
		if sys.argv[2] =='-d':
			debug_flag = 'True'
else:
		raise Exception("Error: No test file provided.")


vIndex  = -1
lIndex = -1
flat_stmts = []
var_colors = {}
usr_var_map = {}
string_label_map = {}

uni_dict = {}
uni_index = -1
overIndex_dict = {}
unspillable = []
top_level_functions = []
func_index = -1
func_names = set([])
vars_to_heapify = set([])



MASK = '$3'      #    /* 11 */
SHIFT  = '$2'

INT_TAG = '$0'   #  /* 00 */

BOOL_TAG='$1'    #/* 01 */

BIG_TAG = '$3' #  /* 11 */

def generate_lambda_name():
	global func_index
	func_index = func_index +1
	new_name = "lambda_" + str(func_index)
	return new_name

def generator(usr_var_name = ""):
	global vIndex
	if (usr_var_name == ""):
	   vIndex = vIndex + 1
	   var_name = "jtg_tmp"+ str(vIndex)
	   var_colors[var_name] = ""

	else:
		#this is if usr_var_name is provided
		#there are two cases if the var has been added to the usr_var_map or not
		if usr_var_name not in usr_var_map:
			vIndex = vIndex + 1
			var_name = "tmp"+ str(vIndex)
			#add to the appropriate places
			usr_var_map[usr_var_name] = var_name
			#var_dict[var_name] = -4*(vIndex+1)
			var_colors[var_name] = ""
		else:
			#this means the variable has already been recognized and in this case we should just assign var_name
			var_name = usr_var_map[usr_var_name]
	return var_name
def generateLabel():
	global lIndex
	lIndex = lIndex + 1
	return "label"+ str(lIndex)
def generateStringLabel(string):
	if not string in string_label_map:
		stringLabel = ".LB" + string
		string_label_map[string] = stringLabel
	

def flatten_code(ast,flat_stmts):
	global vIndex
	if isinstance(ast,Module):
		return (Module(None,flatten_code(ast.node,flat_stmts)))
	elif isinstance(ast,Stmt):
		return (Stmt([simple for complex in ast.nodes for simple in flatten_code(complex,flat_stmts)]))
	elif isinstance(ast,Printnl):
		aExpr, aStmts = flatten_code(ast.nodes[0],flat_stmts)
		return aStmts + [Printnl(aExpr,ast.dest)]
	elif isinstance(ast,Discard):
		aexpr, aStmts = flatten_code(ast.expr,flat_stmts)
		return aStmts + [Discard(aexpr)]
	elif isinstance(ast,Assign):
		if isinstance(ast.nodes[0],AssName):
			usr_var_name = ast.nodes[0].name
			if isinstance(ast.expr,CallFunc):
				aExpr, aStmts = ast.expr , []
				
			else:
				aExpr, aStmts = flatten_code(ast.expr,flat_stmts)
			var_name = generator(usr_var_name)
			return aStmts + [ Assign([AssName(var_name, 'OP_ASSIGN')], aExpr)]
		elif isinstance(ast.nodes[0],Subscript):
			#This is the case like 'x[1] = 4'
			usr_var_name = ast.nodes[0].expr.name

			if isinstance(ast.nodes[0].subs[0],CallFunc):
				sExpr, sStmts =ast.nodes[0].subs[0] , []
			else:
				sExpr, sStmts = flatten_code(ast.nodes[0].subs[0],flat_stmts)
			if isinstance(ast.expr,CallFunc):
				aExpr, aStmts = ast.expr , []
			else:
				aExpr, aStmts = flatten_code(ast.expr,flat_stmts)
			var_name = generator(usr_var_name)
			return sStmts + aStmts  + [Assign([Subscript(Name(var_name), 'OP_ASSIGN', [sExpr])], aExpr)]
		else:
			raise Exception("something is wrong assign.nodes[0] = " + str(ast.nodes[0]))
	elif isinstance (ast, Add):
		lExpr, lStmts = flatten_code(ast.left, flat_stmts)
		rExpr, rStmts = flatten_code(ast.right, flat_stmts)
		new_var = generator()
		return  Name(new_var), lStmts + rStmts + [Assign([AssName(new_var, 'OP_ASSIGN')],Add([lExpr,rExpr]))]
	elif isinstance (ast, UnarySub):
		aexpr , aStmts = flatten_code(ast.expr,flat_stmts)
		new_var = generator()
		new_node = Name(new_var)
		return new_node, aStmts + [Assign([AssName(new_var, 'OP_ASSIGN')], UnarySub(aexpr))]
	elif isinstance(ast, Const):
		return ast, []
	elif isinstance(ast, Name):
		if ast.name in usr_var_map:
			return 	Name(usr_var_map[ast.name]) , []
		else:
			return ast, []
	#elif isinstance(ast,CallFunc):
	#	if isinstance(ast.node,Name):
	#		#this should be an input
	#		if ast.node.name != 'input': raise Exception("Callfunc name was not input")
	#	elif isinstance(ast.node,Lambda):
	#		tne_closed_var = generator()
	#				new_node = InjectFrom('big',create_closure(new_name, free_var_list))
	#
	#		the_closure = create_closures(ast.node)
	#		
	#		ass_the_closure = [Assign([AssName(tne_closed_var, 'OP_ASSIGN')], the_closure)]
						
	elif isinstance(ast,CallFunc):
		new_var = generator()
		return  Name(new_var), [Assign([AssName(new_var, 'OP_ASSIGN')],ast)]
	elif isinstance(ast,Let):
		#Let(var,rhs,body)
		rExp,rAssign = flatten_code(ast.rhs,flat_stmts)
		varTorExpAssign = [Assign([AssName(ast.var.name, 'OP_ASSIGN')],rExp)]
		bodyExpr, bodyAssign = flatten_code(ast.body,flat_stmts)
		return bodyExpr, rAssign + varTorExpAssign + bodyAssign

	elif isinstance(ast,set_attr):
		cExpr,cStmts = flatten_code(ast.c,flat_stmts)
		vExpr,vStmts = flatten_code(ast.val,flat_stmts)
		
		return cStmts + vStmts+[set_attr(cExpr,ast.attr,vExpr)]

	elif isinstance(ast,is_unbound_method):
		new_var = generator()
		aExpr,aStmt = flatten_code(ast.val,flat_stmts)
		return Name(new_var), aStmt + [Assign([AssName(new_var, 'OP_ASSIGN')],is_unbound_method(aExpr))]
	elif isinstance(ast,is_bound_method):
		new_var = generator()
		aExpr,aStmt = flatten_code(ast.val,flat_stmts)
		return Name(new_var), aStmt + [Assign([AssName(new_var, 'OP_ASSIGN')],is_bound_method(aExpr))]
	elif isinstance(ast,get_receiver):
		new_var = generator()
		aExpr,aStmt = flatten_code(ast.o,flat_stmts)
		return Name(new_var), aStmt + [Assign([AssName(new_var, 'OP_ASSIGN')],get_receiver(aExpr))]	
	elif isinstance(ast,get_attr):
		new_var = generator()
		aExpr,aStmt = flatten_code(ast.c,flat_stmts)
		return Name(new_var), aStmt + [Assign([AssName(new_var, 'OP_ASSIGN')],get_attr(aExpr,ast.attr))]
	elif isinstance(ast,get_function):
		new_var = generator()
		fExpr,fStmt = flatten_code(ast.o,flat_stmts)
		return Name(new_var), fStmt + [Assign([AssName(new_var, 'OP_ASSIGN')],get_function(fExpr))]
	elif isinstance(ast,is_class):
		new_var = generator()
		cExpr,cStmt = flatten_code(ast.c,flat_stmts)
		return Name(new_var), cStmt +  [Assign([AssName(new_var, 'OP_ASSIGN')],is_class(cExpr))]
	elif isinstance(ast,create_object):
		new_var = generator()
		cExpr,cStmt = flatten_code(ast.c,flat_stmts)
		return Name(new_var), cStmt +  [Assign([AssName(new_var, 'OP_ASSIGN')],create_object(cExpr))]
	elif isinstance(ast,has_attr):
		new_var = generator()
		aExpr,aStmt = flatten_code(ast.o,flat_stmts)
		return Name(new_var), aStmt + [Assign([AssName(new_var, 'OP_ASSIGN')],has_attr(aExpr,ast.attr))]
	elif isinstance(ast,InjectFrom):
		#InjectFrom(typ,arg)
		new_var = generator()
		aexpr,astmt = flatten_code(ast.arg,flat_stmts)
		return  Name(new_var), astmt + [Assign([AssName(new_var, 'OP_ASSIGN')],InjectFrom(ast.typ,aexpr))] 
	elif isinstance(ast,ProjectTo):
		#ProjectTo(typ,arg)
		new_var = generator()
		aexpr,astmt = flatten_code(ast.arg,flat_stmts)
		return  Name(new_var), astmt + [Assign([AssName(new_var, 'OP_ASSIGN')],ProjectTo(ast.typ,aexpr))] 
	elif isinstance(ast,GetTag):
		new_var = generator()
		aexpr,astmt = flatten_code(ast.arg,flat_stmts)
		return  Name(new_var), astmt +  [Assign([AssName(new_var, 'OP_ASSIGN')],GetTag(aexpr))]

	elif isinstance(ast,IfExp):
		new_var = generator()
		testExpr, testStmts = flatten_code(ast.test,flat_stmts)
		thenExpr, thenStmt = flatten_code(ast.then,flat_stmts)
		elseExpr, elseStmt = flatten_code(ast.else_,flat_stmts)
		if isinstance(thenExpr,ERROREXIT):
			thenAssign = [thenExpr]
		else:
			thenAssign = [Assign([AssName(new_var, 'OP_ASSIGN')],thenExpr)]
		if isinstance(elseExpr,ERROREXIT):
			elseAssign = [elseExpr]
		else:
			elseAssign = [Assign([AssName(new_var, 'OP_ASSIGN')],elseExpr)]
		return Name(new_var) , testStmts + [If([(testExpr, Stmt(thenStmt+ thenAssign))], Stmt(elseStmt+ elseAssign))]
	elif isinstance(ast,While):
		testExpr,testStmts = flatten_code(ast.test,flat_stmts)
		bodyStmts = flatten_code(ast.body,flat_stmts)
		bodyStmts.nodes = bodyStmts.nodes + testStmts
		return testStmts  + [While(testExpr,bodyStmts,None)]
	elif isinstance(ast,If):
		testExpr, testStmts = flatten_code(ast.tests[0][0],flat_stmts)
		return testStmts + [If([(testExpr, flatten_code(ast.tests[0][1],flat_stmts))], flatten_code(ast.else_,flat_stmts))]
			
	elif isinstance(ast,Compare):
		lExpr, lStmts = flatten_code(ast.expr, flat_stmts)
		rExpr, rStmts = flatten_code(ast.ops[0][1], flat_stmts)
		new_var = generator()
		return  Name(new_var), lStmts + rStmts + [Assign([AssName(new_var, 'OP_ASSIGN')], Compare(lExpr, [(ast.ops[0][0],rExpr)]))]
	elif isinstance(ast,Subscript):
		lExpr, lStmts = flatten_code(ast.expr, flat_stmts)
		rExpr, rStmts = flatten_code(ast.subs[0], flat_stmts)
		new_var = generator()
		return Name(new_var), lStmts+rStmts + [Assign([AssName(new_var, 'OP_ASSIGN')], Subscript(lExpr, ast.flags, [rExpr]))]
	elif isinstance(ast,And):
		'''
		IfExp(test,then,else_)
		 We want to translate
		 new_var = then if test else else_
		 To If test
		       new_var = then
		    else
		       new_var = else_
		'''
		new_var = generator()
		testExpr, testStmts =  flatten_code(ast.nodes[0], flat_stmts)
		thenExpr, thenStmt = flatten_code(ast.nodes[1], flat_stmts)
		thenAssign = [Assign([AssName(new_var, 'OP_ASSIGN')],thenExpr)]
		testAssign = [Assign([AssName(new_var, 'OP_ASSIGN')],testExpr)]
		return Name(new_var) , testStmts + [If([(testExpr, Stmt(thenStmt+ thenAssign))], Stmt(testAssign))]

	elif isinstance(ast,Or):
		'''
		IfExp(test,then,else_)
		 We want to translate
		 new_var = then if test else else_
		 To If test
		       new_var = then
		    else
		       new_var = else_
		'''
		new_var = generator()
		testExpr, testStmts =  flatten_code(ast.nodes[0], flat_stmts)
		thenExpr, thenStmt = flatten_code(ast.nodes[1], flat_stmts)
		thenAssign = [Assign([AssName(new_var, 'OP_ASSIGN')],thenExpr)]
		testAssign = [Assign([AssName(new_var, 'OP_ASSIGN')],testExpr)]
		return Name(new_var) , testStmts + [If([(testExpr, Stmt(testAssign))], Stmt(thenStmt+ thenAssign))]

		
	elif isinstance(ast,Not):
		aexpr , aStmts = flatten_code(ast.expr,flat_stmts)
		new_var = generator()
		new_node = Name(new_var)
		return new_node, aStmts + [Assign([AssName(new_var, 'OP_ASSIGN')], Not(aexpr))]
	elif isinstance(ast,CreateList):
		'''class CreateList(Node):
		def __init__(self,length,list_name,listItems)
			self.length = length
			self.list_name = list_name
			self.listItems = listItems
		'''
		'''
		big_pyobj* create_list(pyobj length) {
			list l;
			l.len = project_int(length); /* this should be checked */
			l.data = (pyobj*)malloc(sizeof(pyobj) * l.len);
			return list_to_big(l);
			}
		'''
		lExpr, lenStmt = flatten_code(ast.length,flat_stmts)
		listVar = ast.list_name
		listCREATIONASSIGN = [Assign([AssName(listVar, 'OP_ASSIGN')],CreateListCall(lExpr,listVar))]
				      #Now we want to retrieve each subscript in ast.listItems and flatten the expr
		items = []
		for item in ast.listItems:
			#Each item is an unflattenend SubScript node.
			iExpr,iStmt = flatten_code(item,flat_stmts)
			items = items + iStmt + [iExpr]
		return Name(listVar), lenStmt + listCREATIONASSIGN + items

	elif isinstance(ast,CreateDict):
		dictVar = ast.dict_name
		dictCREATIONASSIGN = [Assign([AssName(dictVar, 'OP_ASSIGN')],CreateDictCall(dictVar))]
		items = []
		for item in (ast.dictItems):
			#Each item is an unflattenend SubScript node.
			iExpr,iStmt = flatten_code(item,flat_stmts)
			items = items + iStmt + [iExpr]#here iExpr is a Subscript node

		return Name(dictVar), dictCREATIONASSIGN + items
	elif isinstance(ast,SetSubScript):
		vExpr, vStmts = flatten_code(ast.val,flat_stmts)
		kExpr, kStmts = flatten_code(ast.key,flat_stmts)
		return SetSubScript(ast.c,kExpr,vExpr),  kStmts + vStmts

	elif isinstance(ast,GetSubScript):
		vExpr, vStmts = flatten_code(ast.c,flat_stmts)
		kExpr, kStmts = flatten_code(ast.key,flat_stmts)
		new_var = generator()
		return Name(new_var),  kStmts + vStmts + [Assign([AssName(new_var, 'OP_ASSIGN')],GetSubScript(vExpr,kExpr))]
	elif isinstance(ast,create_class):
		new_var = generator()
		bExpr,bStmts = flatten_code(ast.bases,flat_stmts)
		return Name(new_var), bStmts +  [Assign([AssName(new_var, 'OP_ASSIGN')],create_class(bExpr))]
	elif isinstance(ast,get_attr):
		new_var = generator()
		return Name(new_var), [Assign([AssName(new_var, 'OP_ASSIGN')],ast)]
	elif isinstance(ast,is_true):
		new_var = generator()
		return Name(new_var), [Assign([AssName(new_var, 'OP_ASSIGN')],is_true(ast.name))]
	elif isinstance(ast,addBig):
		new_var = generator()
		lExpr,lStmt = flatten_code(ast.left_name,flat_stmts)
		rExpr,rStmt = flatten_code(ast.right_name,flat_stmts)
		
		if not( isinstance(lExpr,Name) and isinstance(rExpr,Name)):
			raise Exception("big add is attmpting to add something other than a name probably a broken ProjectTo")
		
		assAdd = [Assign([AssName(new_var, 'OP_ASSIGN')],addBig(lExpr,rExpr))] #here lExpr and rExpr better be Names this returns a bigobj* into new_var which will be Injected
		return Name(new_var), lStmt + rStmt + assAdd
	elif isinstance(ast,ERROREXIT):
		return ast, []
	elif isinstance(ast,equalBig):
		new_var = generator()
		lExpr,lStmt = flatten_code(ast.left_name,flat_stmts)
		rExpr,rStmt = flatten_code(ast.right_name,flat_stmts)
		if not( isinstance(lExpr,Name) and isinstance(rExpr,Name)):
			raise Exception("big equal is attempting to add something other than a name probably a broken ProjectTo")
		
		assCheck = [Assign([AssName(new_var, 'OP_ASSIGN')],equalBig(lExpr,rExpr))]
		#here lExpr and rExpr better be Names this returns a bigobj* into new_var which will be Injected
		return Name(new_var), lStmt + rStmt + assCheck
	
	elif isinstance(ast,nequalBig):
		new_var = generator()
		lExpr,lStmt = flatten_code(ast.left_name,flat_stmts)
		rExpr,rStmt = flatten_code(ast.right_name,flat_stmts)
		if not( isinstance(lExpr,Name) and isinstance(rExpr,Name)):
			raise Exception("big not equal is attmpting to add something other than a name probably a broken ProjectTo")
		
		assCheck = [Assign([AssName(new_var, 'OP_ASSIGN')],nequalBig(lExpr,rExpr))]
		#here lExpr and rExpr better be Names this returns a bigobj* into new_var which will be Injected
		return Name(new_var), lStmt + rStmt + assCheck
	elif (ast in ('int','bool','big','==','!=','is')):
		return ast , []
	elif isinstance(ast,Return):
		rExpr,rStmt = flatten_code(ast.value,flat_stmts)
		return rStmt + [Return(rExpr)]
	elif isinstance(ast,Lambda):
		raise Exception('There should be no lambdas getting passed into flatten.')
	elif isinstance(ast,create_closure):
		#here we have the name and the params, so we might need to flatten the function in the global_functions
		#exprList = []
		#envStmts = []
		new_var = generator()
		expr,estmt = flatten_code(ast.enviroment,flat_stmts)
		nexpr,nstmt = flatten_code(Name(ast.name),flat_stmts)
		ass = [Assign([AssName(new_var, 'OP_ASSIGN')],create_closure(nexpr,expr))]
		return Name(new_var), estmt +nstmt + ass
		
	elif isinstance(ast,get_free_vars):
#####We want to faltten the code name portion here as it may be a getsubscript
		fexpr,fstmt = flatten_code(ast.name,flat_stmts)
		#if ast.name.name in usr_var_map:
		#	func_name = usr_var_map[ast.name]
		#else:
		#	func_name = ast.name
		
		return get_free_vars(fexpr), fstmt
	elif isinstance(ast,get_fun_ptr):
		exprList = []
		eStmts = []
		for var in ast.params[1]:
			expr,estmt = flatten_code(var,flat_stmts)
			exprList = exprList + [expr]
			eStmts = eStmts + estmt
		new_var = generator()
		nexpr,nstmt = flatten_code(ast.name,flat_stmts)
		fexpr,fstmt = flatten_code(ast.params[0],flat_stmts)
		#if ast.name.name in usr_var_map:
		#	func_name = usr_var_map[ast.name.name]
		#else:
		#	func_name = ast.name.name
		ass = [Assign([AssName(new_var, 'OP_ASSIGN')],get_fun_ptr(nexpr,[fexpr,exprList]))]
		return Name(new_var), eStmts + nstmt + fstmt + ass

	else:
		raise Exception("Error "+ str(ast))

def generate_x86_ir(flat_ast_stmts):
	IR = []
	#add the move base_pointer to each input_params
	#also add the move base to free_vars list so that we use that again
	for stmt in flat_ast_stmts:
		if isinstance(stmt,Assign) and isinstance(stmt.nodes[0],AssName):
			if isinstance(stmt.expr,CallFunc):

				#this is something like ... f1 = f(1) or x = input()
				#first we need to push each arg increment the index
				#index = 0
				#for arg in reversed(stmt.args):
				#	#new_x86_stmt=x86_ir_push(arg)
				#	index = index+4
				#	IR = IR + [x86_ir_push(arg)]
				if stmt.expr.node.name == 'input':
					new_x86_stmt=x86_ir_call('input')
					IR = IR + [new_x86_stmt]
					new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #move the return to %eax
					IR = IR + [new_x86_stmt]
				else:
					raise Exception("for some reason generate_x86_ir got a CallFunc that was not input it was ..." + str(stmt.expr.node.name))
				
					#move the stack pointer back in place
					#index_s = "$"+str(index)
					#new_x86_stmt=x86_ir_add(index_s,"%esp")
					#IR = IR + [new_x86_stmt]

			elif isinstance(stmt.expr,Const):
				new_x86_stmt = x86_ir_move("$"+str(stmt.expr.value), stmt.nodes[0].name)
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,UnarySub):
				if isinstance(stmt.expr.expr,Name):
					src = stmt.expr.expr.name
				elif isinstance(stmt.expr.expr,Const):
					c_src = "$" + str(stmt.expr.expr.value)
					src = generator()
					new_x86_stmt = x86_ir_move(c_src,src)
					IR = IR + [new_x86_stmt]
				else:
					raise Exception("Unary Sub took something other than a const or name as input")
				
				dest = stmt.nodes[0].name
				new_x86_stmt = x86_ir_move(src,dest)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt = x86_ir_neg(dest)
				IR = IR + [new_x86_stmt]
				
			elif isinstance(stmt.expr,Add):
				dest = stmt.nodes[0].name
				left_operand = stmt.expr.left
				right_operand = stmt.expr.right
				if isinstance(left_operand,Name):
					left_add = left_operand.name
				elif isinstance(left_operand,Const):
					left_add = "$" + str(left_operand.value)
				else:
					raise Exception ("Error left_operand was not a constant or a name" + str(left_operand))
				if isinstance(right_operand,Name):
					right = right_operand.name
					right_add = generator()
					new_x86_stmt = x86_ir_move(right,right_add)
					IR = IR + [new_x86_stmt]
				elif isinstance(right_operand,Const):
					#If the right_operand is a Const we want to stick it in a variable, since the add
					#treats the right as the destination as well as the right_operand
					r_value = "$" + str(right_operand.value)
					right_add = generator()
					new_x86_stmt = x86_ir_move(r_value,right_add)
					IR = IR + [new_x86_stmt]
				else:
					raise Exception( "Error right_operand was not a constant or a name:" + str(right_operand))
				new_x86_stmt = x86_ir_add(left_add,right_add)
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move(right_add,dest)
				IR = IR + [new_x86_stmt]

					
			elif isinstance(stmt.expr,Name):
				#This is something like x = tmp10
				src = stmt.expr.name
				dest = stmt.nodes[0].name
				new_x86_stmt = x86_ir_move(src,dest)
				IR = IR + [new_x86_stmt]
		

			elif isinstance(stmt.expr,ProjectTo):
				
				'''
				sarl A, B     B >> A -> B (where A is a constant)
				
				This one preserves the sign
				/*
				Projecting from pyobj.
				*/
				'''
				if(stmt.expr.typ == 'int' or stmt.expr.typ == 'bool'):
					'''
					int project_int(pyobj val) {
						assert((val & MASK) == INT_TAG);
						return val >> SHIFT;
					'''
					if isinstance(stmt.expr.arg,Name):
						val = stmt.expr.arg.name
					elif isinstance(stmt.expr.arg,Const):
						val = '$' + str(stmt.expr.arg.value)
					else:
						raise Exception('In the ProjectTo AST -> IR Conversion stmt.expr.arg was neither a Name or a Const it was a' + str(stmt.expr.arg))
					dest = stmt.nodes[0].name
					new_x86_stmt = x86_ir_move(val,dest)
					IR = IR + [new_x86_stmt]
					new_x86_stmt = x86_ir_sar(dest)
					IR = IR + [new_x86_stmt]
				elif(stmt.expr.typ == 'big'):
					new_x86_stmt=x86_ir_push(stmt.expr.arg.name)
					IR = IR + [new_x86_stmt]
					new_x86_stmt=x86_ir_call("project_big")
					IR = IR + [new_x86_stmt]
					new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name)
					IR = IR + [new_x86_stmt]
					new_x86_stmt=x86_ir_add("$4","%esp")
					IR = IR + [new_x86_stmt]
				else:
					raise Exception("Something is broken in ProjectTo " + str(stmt.exp.typ) + " was not a (int,bool,big)")
			elif isinstance(stmt.expr,InjectFrom):
				'''
				This one preserves the sign
				sall A, B B << A -> B (where A is a constant)
				pyobj inject_int(int i) {
				return (i << SHIFT) | INT_TAG;
				}
				pyobj inject_bool(int b) {
				return (b << SHIFT) | BOOL_TAG;
				}
			
				pyobj inject_big(big_pyobj* p) {
				assert((((long)p) & MASK) == 0); 
				return ((long)p) | BIG_TAG;
				}
				'''
				if(stmt.expr.typ == 'int' or stmt.expr.typ == 'bool'):
					'''
					pyobj inject_bool(int b) {
					return (b << SHIFT) | BOOL_TAG;
					}
					'''
					
					#orl A, B A|B -> B (bitwise-or)
					if stmt.expr.typ == 'int':
						tag = INT_TAG
					elif stmt.expr.typ == 'bool':
						tag = BOOL_TAG
						
					if isinstance(stmt.expr.arg,Name):
						val = stmt.expr.arg.name
					elif isinstance(stmt.expr.arg,Const):
						val = '$' + str(stmt.expr.arg.value)
					else:
						raise Exception('In the InjectFrom AST -> IR stage Conversion stmt.expr.arg was neither a Name or a Const it was a' + str(stmt.expr.arg))
					dest = stmt.nodes[0].name
					new_x86_stmt = x86_ir_move(val,dest)
					IR = IR + [new_x86_stmt]
					new_x86_stmt = x86_ir_sal(dest)
					IR = IR + [new_x86_stmt]
					new_x86_stmt = x86_ir_or(tag,dest)
					IR = IR + [new_x86_stmt]
				elif(stmt.expr.typ == 'big'):
					theBig = stmt.expr.arg.name
					new_x86_stmt=x86_ir_push(theBig)
					IR = IR + [new_x86_stmt]
					new_x86_stmt=x86_ir_call("inject_big")
					IR = IR + [new_x86_stmt]
					new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name)
					IR = IR + [new_x86_stmt]
					new_x86_stmt=x86_ir_add("$4","%esp")
					IR = IR + [new_x86_stmt]
				else:
					raise Exception("Something is broken in InjectFrom " + str(stmt.exp.typ) + " was not a (int,bool,big)")
			elif isinstance(stmt.expr,GetTag):
				if isinstance(stmt.expr.arg,Name):
					src = stmt.expr.arg.name
				else:
					raise Exception("The argument of GetTag in ast->IR conversion was not a Name")
				dest = stmt.nodes[0].name
				B = generator()
				#movl src, B
				new_x86_stmt = x86_ir_move(src,B)
				IR = IR + [new_x86_stmt]

				#andl MASK,B
				new_x86_stmt = x86_ir_and(MASK,B)
				IR = IR + [new_x86_stmt]

				#movl B, dest

				new_x86_stmt = x86_ir_move(B,dest)
				IR = IR + [new_x86_stmt]

			elif isinstance(stmt.expr,Compare):
				#cmpl A, B compare A and B and set flag
				#cmpl A, B compare A and B and set flag
				#je L If the flag is set to "equal", jump to label L
				dest = stmt.nodes[0].name
				left = stmt.expr.expr.name
				right = stmt.expr.ops[0][1]
				if right == 'int':
					right = str(INT_TAG)
				elif right == 'bool':
					right =  str(BOOL_TAG)
				elif right == 'big':
					right =   str(BIG_TAG)
				else:
					right = right.name
				if stmt.expr.ops[0][0] == 'is':
					IR = IR + [x86_ir_cmp(right,left)] #this swap was made so that the $... appears on the left
					IR = IR + [x86_ir_sete(1)]   #here al is being set so eax is busy
					IR = IR + [x86_ir_movzbl('%al','%eax')]
					IR = IR + [x86_ir_move('%eax',dest)] 
				elif stmt.expr.ops[0][0] == '==':
					IR = IR + [x86_ir_cmp(right,left)] #this swap was made so that the $... appears on the left
					IR = IR + [x86_ir_sete(1)]   #here al is being set so eax is busy
					IR = IR + [x86_ir_movzbl('%al','%eax')]
					IR = IR + [x86_ir_move('%eax',dest)]
				elif stmt.expr.ops[0][0] == '!=':
					IR = IR + [x86_ir_cmp(right,left)]
					IR = IR + [x86_ir_setne(1)] #here al is being set so eax is busy
					IR = IR + [x86_ir_movzbl('%al','%eax')] 	
					IR = IR + [x86_ir_move('%eax',dest)]	
			elif isinstance(stmt.expr,Subscript):
				#Subscript(Name('a'), 'OP_ASSIGN', [Const(1)])  =(.expr,.flags,.subs)
				#So this is a get  call
				#pyobj get_subscript(pyobj c, pyobj key);

				theBig = stmt.expr.expr.name
				key = stmt.expr.subs[0].name

				new_x86_stmt=x86_ir_push(key)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_push(theBig)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_call("get_subscript")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,SetSubScript):
				theBigName = stmt.expr.c.name
				#Assign([AssName('jtg_tmp23', 'OP_ASSIGN')], SetSubScript(Name('jtg_tmp5'), Name('jtg_tmp6'), Name('jtg_tmp5')))
				if isinstance(stmt.expr.key,Name):
					key = stmt.expr.key.name
				else:
					raise Exception("A Setsubscript key was a "+str(stmt.expr.key)+" expected a name, otherwise it wasn't injected")
				if isinstance(stmt.expr.val,Name):
					val = stmt.expr.val.name
				else:
					raise Exception("A Setsubscript val was a "+str(stmt.expr.key)+" expected a name, otherwise it wasn't injected")
				
				dest = stmt.nodes[0].name
				new_x86_stmt=x86_ir_push(val)
				IR = IR + [new_x86_stmt]

				new_x86_stmt=x86_ir_push(key)
				IR = IR + [new_x86_stmt]

				new_x86_stmt=x86_ir_push(theBigName)
				IR = IR + [new_x86_stmt]

				new_x86_stmt=x86_ir_call("set_subscript")
				IR = IR + [new_x86_stmt]


				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$12","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,GetSubScript):
				theBigName = stmt.expr.c.name
				
				if isinstance(stmt.expr.key,Const):
					raise Exception('the key must be a pyobj so it cant be a const')#key = "$" + str(stmt.expr.key.value)
				elif isinstance(stmt.expr.key,Name):
					key = stmt.expr.key.name
				else:
					raise Exception("A Setsubscript key was a "+str(stmt.expr.key)+" expected a name or a const")
				dest = stmt.nodes[0].name

				new_x86_stmt=x86_ir_push(key)
				IR = IR + [new_x86_stmt]

				new_x86_stmt=x86_ir_push(theBigName)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_call("get_subscript")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$8","%esp")
				IR = IR + [new_x86_stmt]
				
			elif isinstance(stmt.expr,CreateListCall):
				if isinstance(stmt.expr.length,Name):
					length = stmt.expr.length.name
				else:
					raise Exception("the length of the new list is not being Injected properly")

				new_x86_stmt=x86_ir_push(length)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_call("make_list")
				IR = IR + [new_x86_stmt]

				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is done the list will be stored in stmt.nodes[0].name as a pyobj
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]


			elif isinstance(stmt.expr,CreateDictCall):
				
				new_x86_stmt=x86_ir_call("make_dict")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is done the list will be stored in stmt.nodes[0].name as a pyobj
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,is_true):
				#This is a call to the is_true function
				if isinstance(stmt.expr.name,Name):
					varToCheck = stmt.expr.name.name
				else:
					raise Exception("is_true is trying to push a stmt.expr.name that is not a Name ...."+ str(stmt.expr.name))
				new_x86_stmt=x86_ir_push(varToCheck)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_call("is_true")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is done the list will be stored in stmt.nodes[0].name as a pyobj
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,addBig):
				if isinstance(stmt.expr.left_name,Name) and isinstance(stmt.expr.right_name,Name):
					lToPush = stmt.expr.left_name.name
					rToPush = stmt.expr.right_name.name
				else:
					raise Exception("addBig is trying to push a left or right name that is not a Name")
				new_x86_stmt=x86_ir_push(rToPush)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_push(lToPush)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_call("add")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is done the list will be stored in stmt.nodes[0].name as a pyobj
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$8","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,equalBig):
				if isinstance(stmt.expr.left_name,Name) and isinstance(stmt.expr.right_name,Name):
					lToPush = stmt.expr.left_name.name
					rToPush = stmt.expr.right_name.name
				else:
					raise Exception("equalBig is trying to push a left or right name that is not a Name")
				new_x86_stmt=x86_ir_push(rToPush)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_push(lToPush)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_call("equal")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is done the list will be stored in stmt.nodes[0].name as a pyobj
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$8","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,nequalBig):
				if isinstance(stmt.expr.left_name,Name) and isinstance(stmt.expr.right_name,Name):
					lToPush = stmt.expr.left_name.name
					rToPush = stmt.expr.right_name.name
				else:
					raise Exception("nequalBig is trying to push a left or right name that is not a Name")
				new_x86_stmt=x86_ir_push(rToPush)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_push(lToPush)
				IR = IR + [new_x86_stmt]
				
				new_x86_stmt=x86_ir_call("not_equal")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is done the list will be stored in stmt.nodes[0].name as a pyobj
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$8","%esp")
				IR = IR + [new_x86_stmt]

			elif isinstance(stmt.expr,create_closure):
				#name and enviroment
				if isinstance(stmt.expr.name,Name):
					fun_ptr = "$" + str(stmt.expr.name.name) 
				else:
					raise exception("create_closure had something other than a Name node for its name")
				if isinstance(stmt.expr.enviroment,Name):
					free_vars =  str(stmt.expr.enviroment.name) 
				else:
					raise exception("create_closure had something other than a Name node for its enviroment")
				new_x86_stmt=x86_ir_push(free_vars)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_push(fun_ptr)
				IR = IR + [new_x86_stmt]
				#for the function pointer we just pass the label I guess.
				#so we want to push the free_vars then push the label
				new_x86_stmt=x86_ir_call("create_closure")
				IR = IR + [new_x86_stmt]
				#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is the function closure will be stored in the lhs var
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$8","%esp")
				IR = IR + [new_x86_stmt]

			elif isinstance(stmt.expr,get_attr):
				#name and enviroment
				if isinstance(stmt.expr.c,Name):
					classname =  stmt.expr.c.name
				else:
					raise exception("get_attr had something other than a Name node for its class name")
				attr =  "$" + str(string_label_map[stmt.expr.attr]) 
				
				new_x86_stmt=x86_ir_push(attr)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_push(classname)
				IR = IR + [new_x86_stmt]
				#for the function pointer we just pass the label I guess.
				#so we want to push the free_vars then push the label
				new_x86_stmt=x86_ir_call("get_attr")
				IR = IR + [new_x86_stmt]
				#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #the class attr
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$8","%esp")
				IR = IR + [new_x86_stmt]



			elif isinstance(stmt.expr,is_bound_method):
				#name and enviroment
				if isinstance(stmt.expr.val,Name):
					func_name =  stmt.expr.val.name
				else:
					raise exception("is_bound_method had something other than a Name node for its class name")
				
				new_x86_stmt=x86_ir_push(func_name)
				IR = IR + [new_x86_stmt]
				#for the function pointer we just pass the label I guess.
				#so we want to push the free_vars then push the label
				new_x86_stmt=x86_ir_call("is_bound_method")
				IR = IR + [new_x86_stmt]
				#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #the class attr
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			
			elif isinstance(stmt.expr,is_unbound_method):
				#name and enviroment
				if isinstance(stmt.expr.val,Name):
					func_name =  stmt.expr.val.name
				else:
					raise exception("is_unbound_method had something other than a Name node for its class name")
				
				new_x86_stmt=x86_ir_push(func_name)
				IR = IR + [new_x86_stmt]
				#for the function pointer we just pass the label I guess.
				#so we want to push the free_vars then push the label
				new_x86_stmt=x86_ir_call("is_unbound_method")
				IR = IR + [new_x86_stmt]
				#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #the class attr
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			
			elif isinstance(stmt.expr,get_receiver):
				#name and enviroment
				if isinstance(stmt.expr.o,Name):
					rec_name =  stmt.expr.o.name
				else:
					raise exception("get_receiver had something other than a Name node for its class name")
				
				new_x86_stmt=x86_ir_push(rec_name)
				IR = IR + [new_x86_stmt]
				#for the function pointer we just pass the label I guess.
				#so we want to push the free_vars then push the label
				new_x86_stmt=x86_ir_call("get_receiver")
				IR = IR + [new_x86_stmt]
				#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #the class attr
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			

			
			elif isinstance(stmt.expr,has_attr):
				#name and enviroment
				if isinstance(stmt.expr.o,Name):
					classname =  stmt.expr.o.name
				else:
					raise exception("has_attr had something other than a Name node for its class name")
				attr =  "$" + str(string_label_map[stmt.expr.attr]) 
				
				new_x86_stmt=x86_ir_push(attr)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_push(classname)
				IR = IR + [new_x86_stmt]
				#for the function pointer we just pass the label I guess.
				#so we want to push the free_vars then push the label
				new_x86_stmt=x86_ir_call("has_attr")
				IR = IR + [new_x86_stmt]
				#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #whether it has that attr
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$8","%esp")
				IR = IR + [new_x86_stmt]	
			elif isinstance(stmt.expr,create_class):
				#big_pyobj* create_class(pyobj bases)
				if isinstance(stmt.expr.bases,Name):
					bases_name = stmt.expr.bases.name
				else:
					raise exception("Bases is not a name to a list something is broken.")
				new_x86_stmt=x86_ir_push(bases_name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_call("create_class")
				IR = IR + [new_x86_stmt]
				#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is the function closure will be stored in the lhs var
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,create_object):
				if isinstance(stmt.expr.c,Name):
					obj_name = str(stmt.expr.c.name)
				else:
					raise Exception("create_object didn't have a name in its object")
				new_x86_stmt=x86_ir_push(obj_name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_call("create_object")
				IR = IR + [new_x86_stmt]
				#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is the function closure will be stored in the lhs var
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,is_class):
				if isinstance(stmt.expr.c,Name):
					obj_name = str(stmt.expr.c.name)
				else:
					raise Exception("is_class didn't have a name in its object")
				new_x86_stmt=x86_ir_push(obj_name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_call("is_class")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) 
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,get_function):
				if isinstance(stmt.expr.o,Name):
					obj_name = str(stmt.expr.o.name)
				else:
					raise Exception("is_class didn't have a name in its object")
				new_x86_stmt=x86_ir_push(obj_name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_call("get_function")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) 
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
			elif isinstance(stmt.expr,get_fun_ptr):
				#this needs to take into account both get_fun_ptr AND get_free_vars (which is params[0])
				#get_fun_ptr still needs to be called...
				if isinstance(stmt.expr.name,Name):
					fun_name =str(stmt.expr.name.name) 
				else:
					raise Exception("get_fun_ptr had something other than a Name node for its name"+ str(stmt.expr.name))
				#want to get the function pointer

				#now i need to push the params....(need to make sure that params are lists so we need to do createlists just like create_closure)
				#if isinstance(stmt.expr.params[1],Name):
				
				#	fun_inputs =str(stmt.expr.params[1].name) 
				#else:
				#	raise exception("get_fun_ptr params[1] had something other than a Name node for its name"+ str(stmt.expr.params[1]))

				#we now need to change it so that fun_inputs is a list of inputs... we just want to push each element of the list.
				to_add_index = 4 #this takes into account the free_vars
				for var in reversed(stmt.expr.params[1]):
					if isinstance(var,Name):
						to_push = var.name
					#elif isinstance(var,Const):
					#	to_push = "$" + str(var.value)
					else:
						raise Exception("something other than a name was passed to a function..")
					new_x86_stmt=x86_ir_push(to_push)
					to_add_index = to_add_index +4
					IR = IR + [new_x86_stmt]
				#Now all the inputs have been pushed on the stack. 
				#the next param is actually a get_free_vars function call

				if isinstance(stmt.expr.params[0].name,Name):
					free_name = stmt.expr.params[0].name.name
				else:
					raise Exception("get_free_vars node had something other than a name node in it..." + str(stmt.expr.params[0]))
				new_x86_stmt=x86_ir_push(free_name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_call("get_free_vars")
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_push('%eax')
				IR = IR + [new_x86_stmt]
				
				
				#now we want to call the fun_ptr 

				new_x86_stmt=x86_ir_push(fun_name)
				IR = IR + [new_x86_stmt]
				new_x86_stmt=x86_ir_call("get_fun_ptr")
				IR = IR + [new_x86_stmt]
				#after this the %eax register will have the fun_ptr....i don't know what to do with this...

				new_x86_stmt=x86_ir_add("$4","%esp")
				IR = IR + [new_x86_stmt]

				new_x86_stmt=x86_ir_call_star("%eax") #make sure not to put parenthesis around the register
				IR = IR + [new_x86_stmt]
				
				
				
				new_x86_stmt=x86_ir_add("$"+str(to_add_index),"%esp")
				IR = IR + [new_x86_stmt]
				new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #now the var should store the result of the function evaluation
				IR = IR + [new_x86_stmt]
				
				
			else:
				raise Exception("Error: missed" + str(stmt.expr) + "in assign asm_ir_translate")
				
		elif isinstance(stmt,Discard):
			if isinstance(stmt.expr,Name):
				pass
			elif isinstance(stmt.expr,Const):
				pass
			elif isinstance(stmt.expr,CallFunc):
				new_x86_stmt=x86_ir_call("input")
				IR = IR + [new_x86_stmt]
			else:
				raise Exception( "Error right_operand was not a constant or a name:" + str(stmt.expr))
		elif isinstance(stmt,Assign) and isinstance(stmt.nodes[0],Subscript):
			if isinstance(stmt.nodes[0].expr,Name):
				theBigName = stmt.nodes[0].expr.name
			else:
				raise Exception("This should be a name node... instead it was a " + str(stmt.nodes[0].expr))

			if isinstance(stmt.nodes[0].subs[0],Name):
				key = stmt.nodes[0].subs[0].name
			elif isinstance(stmt.nodes[0].subs[0],Const):
				key = '$' + str(stmt.nodes[0].subs[0].value)

			else:
				raise Exception("This should be a name/const node... instead it was a " + str(stmt.nodes[0].expr))
			
			if isinstance(stmt.expr,Const):
				val = "$" + str(stmt.expr.value)
			elif isinstance(stmt.expr,Name):
				val = stmt.expr.name
			else:
				raise Exception("A setsubscript key was a "+str(stmt.expr.key)+" expected a name or a const")
	
			new_x86_stmt=x86_ir_push(val)
			IR = IR + [new_x86_stmt]
				
			new_x86_stmt=x86_ir_push(key)
			IR = IR + [new_x86_stmt]
			new_x86_stmt=x86_ir_push(theBigName)
			IR = IR + [new_x86_stmt]

			new_x86_stmt=x86_ir_call("set_subscript")
			IR = IR + [new_x86_stmt]
			
			new_x86_stmt=x86_ir_add("$12","%esp")
			IR = IR + [new_x86_stmt]
		elif isinstance(stmt,set_attr):
			attribute = "$" + str(string_label_map[stmt.attr])
			
			class_name = stmt.c.name
			if isinstance(stmt.val,Const):
				val = "$" + str(stmt.val.value)
			elif isinstance(stmt.val,Name):
				val = stmt.val.name
			else:
				raise Exception("A setsubscript key was a "+str(stmt.expr.key)+" expected a name or a const")
			#pyobj set_attr(pyobj obj, char* attr, pyobj val);
			#so we want to push the expr then push the attribute then the class_name but the char* is weird
			new_x86_stmt=x86_ir_push(val)
			IR = IR + [new_x86_stmt]
			new_x86_stmt=x86_ir_push(attribute)
			IR = IR + [new_x86_stmt]
			new_x86_stmt=x86_ir_push(class_name)
			IR = IR + [new_x86_stmt]

			new_x86_stmt=x86_ir_call("set_attr")
			IR = IR + [new_x86_stmt]
			#this moves the final big_pyobj* into eax which will then be Injected into a pyobj
			#new_x86_stmt = x86_ir_move("%eax", stmt.nodes[0].name) #when this is the function closure will be stored in the lhs var
			#IR = IR + [new_x86_stmt]
			new_x86_stmt=x86_ir_add("$12","%esp")
			IR = IR + [new_x86_stmt]
			
			
		elif isinstance(stmt,Printnl):
			# print tmp2
			#movl -12(%ebp), %eax
			#$pushl %eax
			#call print_int_nl
			#addl $4, %esp
			#there are two options here either you are printing a variable or a constant

			#need to change this....
			if isinstance(stmt.nodes,Name):
				print_input = stmt.nodes.name
			#elif isinstance(stmt.nodes,Const):
			#	print_input = '$' + str(stmt.nodes.value)
			#	pass
			else:
					raise Exception( "Error right_operand was not a name:" + str(right_operand))
			new_x86_stmt=x86_ir_push(print_input)  #this input better be a pyopj or shit will get crazy
			IR = IR + [new_x86_stmt]

			new_x86_stmt=x86_ir_call("print_any")
			IR = IR + [new_x86_stmt]
		
			new_x86_stmt=x86_ir_add("$4","%esp")
			IR = IR + [new_x86_stmt]
		elif isinstance(stmt,If):
			IR = IR + [If([(stmt.tests[0][0], Stmt(generate_x86_ir(stmt.tests[0][1])))], Stmt(generate_x86_ir(stmt.else_)))]
		elif isinstance(stmt,While):
			IR = IR + [While(stmt.test,Stmt(generate_x86_ir(stmt.body)),None)]
		elif isinstance(stmt, SetSubScript):
			if isinstance(stmt.c,Name):
				theBigName = stmt.c.name
			else:
				theBigName = stmt.c
			if isinstance(stmt.key,Name):
				key = stmt.key.name
			else:
				raise Exception("A Setsubscript key was a "+str(stmt.key)+" expected a name, otherwise it wasn't injected")
			if isinstance(stmt.val,Name):
				val = stmt.val.name
			else:
				raise Exception("A Setsubscript val was a "+str(stmt.key)+" expected a name, otherwise it wasn't injected")
	
			new_x86_stmt=x86_ir_push(val)
			IR = IR + [new_x86_stmt]
				
			new_x86_stmt=x86_ir_push(key)
			IR = IR + [new_x86_stmt]
	
			new_x86_stmt=x86_ir_push(theBigName)
			IR = IR + [new_x86_stmt]

			new_x86_stmt=x86_ir_call("set_subscript")
			IR = IR + [new_x86_stmt]

			new_x86_stmt=x86_ir_add("$12","%esp")
			IR = IR + [new_x86_stmt]
		elif isinstance(stmt,ERROREXIT):
			IR = IR + [x86_ir_move('$3000','%eax')] #if this is reached then 750's will be introduced into the output
			IR = IR + [x86_ir_leave(-1)]
			IR = IR + [x86_ir_ret(-1)]
		elif isinstance(stmt,Return):
			if isinstance(stmt.value,Name):
				to_return = stmt.value.name
			elif isinstance(stmt.value,Const):
				to_return = "$" + str(stmt.value.value)
			else:
				raise Exception("Tried to generate x86 for a return value that was not a const or a name..." + str(stmt.value))
			IR = IR + [x86_ir_move(to_return,'%eax')]

		else: raise Exception("Forgot " + str(stmt) +  " in generate x86 ir")
	return IR




def build_i_graph(x86_IR,L_after):
	'''
	The liveness rules
	          This is the base case      :L_after(n) = empty
	          This must be true          :L_after(k) = L_before(k+1)
	          This is the recursion rule :L_before(k) = (L_after(k)-W(k)) \union R(K)
	'''
	i_graph = {}
	i_graph["%eax"] = set()
	i_graph["%ecx"] = set()
	i_graph["%edx"] = set()
	
	for  x in var_colors:
		i_graph[x] = set()
		
	#So in each step we want to add to the graph based on the new liveness
	L_before = set()
	for ind in reversed(range(0,len(x86_IR))):
		stmt = x86_IR[ind]
		L_before = set([])
		W = set([])
		R = set([])
		if isinstance(stmt,x86_ir_move):		
			#ghetto fix....				
			if stmt.dest_name == '%eax' and not stmt.src_name == '%al':
				L_after = L_after | set(['%eax']) #this should only occur in a return 
			#end of ghetto fix.....	
		        if False: # not stmt.dest_name in L_after: #this is to kill a dead add
			       L_before = L_after
			       x86_IR[ind:ind+1] = []	
			else:
				if (stmt.src_name[0] != '$' and stmt.src_name[0] != '%' and not stmt.src_name[0].isdigit()):
					R = set([stmt.src_name])
				W =  set([stmt.dest_name])
				L_before = (L_after - W) | R
				   #build graph too
				   #This statemetn puts an edge from (dest_name -> each live variable except for stmt.src_name,stmt.dest_name
				if stmt.dest_name in L_after:
					i_graph[stmt.dest_name] = i_graph[stmt.dest_name] | (L_after - set([stmt.src_name,stmt.dest_name]))
					#Now we need to add the other direction so we have symmetry
					for x in  (L_after - set([stmt.src_name,stmt.dest_name])):
						i_graph[x] = i_graph[x] | set([stmt.dest_name])
			
		elif isinstance(stmt,x86_ir_add):
			if False:#((not stmt.right_name in L_after) and stmt.right_name[0] != '%') :
				L_before = L_after
				x86_IR[ind:ind+1] = [] #this is to kill a dead add
			else:
				W = set([stmt.right_name])
				if (stmt.left_name[0] != '$'):
					R = set([stmt.left_name])
				if(stmt.right_name[0] != '%'):
					R = R | set([stmt.right_name])
				L_before = (L_after - W) | R
				
			#update graph
				if stmt.right_name in L_after:
					
					i_graph[stmt.right_name] = i_graph[stmt.right_name] |  (L_after - set([stmt.right_name]))
					for x in  (L_after - set([stmt.right_name])):
						i_graph[x] = i_graph[x] | set([stmt.right_name])
		elif isinstance(stmt,x86_ir_sete) or isinstance(stmt,x86_ir_setne):
			L_before = (L_after - W) | R
			i_graph["%eax"] = i_graph["%eax"] | L_after
		elif isinstance(stmt,x86_ir_sar) or isinstance(stmt,x86_ir_sal) or isinstance(stmt,x86_ir_neg) or isinstance(stmt,x86_ir_not):
		        W = set([stmt.src_name])
			R = set([stmt.src_name])
			L_before = (L_after - W) | R
			if stmt.src_name in L_after:
				i_graph[stmt.src_name] = i_graph[stmt.src_name] | (L_after - set([stmt.src_name]))
				for x in  (L_after - set([stmt.src_name])):
					i_graph[x] = i_graph[x] | set([stmt.src_name])
		elif isinstance(stmt,x86_ir_and):
			W = set([stmt.right_name])
			R = set([stmt.right_name])
			L_before = (L_after - W) | R
			#update graph
			if stmt.right_name in L_after:

				i_graph[stmt.right_name] = i_graph[stmt.right_name] |  (L_after - set([stmt.right_name]))
				for x in  (L_after - set([stmt.right_name])):
					i_graph[x] = i_graph[x] | set([stmt.right_name])
		elif isinstance(stmt,x86_ir_or):
			W = set([stmt.right_name])
			R = set([stmt.right_name])
			L_before = (L_after - W) | R
			#update graph
			if stmt.right_name in L_after:
				i_graph[stmt.right_name] = i_graph[stmt.right_name] |  (L_after - set([stmt.right_name]))
				for x in  (L_after - set([stmt.right_name])):
					i_graph[x] = i_graph[x] | set([stmt.right_name])
		elif isinstance(stmt, x86_ir_call):
			L_before = (L_after - W) | R
			#update graph
			i_graph["%eax"] = i_graph["%eax"] | L_after
			i_graph["%ecx"] = i_graph["%ecx"] | L_after
			i_graph["%edx"] = i_graph["%edx"] | L_after
		elif isinstance(stmt,x86_ir_call_star):
			L_before = (L_after - W) | R
			#update graph
			i_graph["%eax"] = i_graph["%eax"] | L_after
			i_graph["%ecx"] = i_graph["%ecx"] | L_after
			i_graph["%edx"] = i_graph["%edx"] | L_after
		elif isinstance(stmt,x86_ir_movzbl):
			#Here the left register is the first byte of eax
			L_before = (L_after - W) | R
			i_graph["%eax"] = i_graph["%eax"] | L_after

		elif isinstance(stmt,x86_ir_push):
			if stmt.to_push[0] != '$' and stmt.to_push[0] != '%': #don't want to say we are reading from a const or a reg
				R = set([stmt.to_push])
			L_before = (L_after - W) | R
			#nothing is written to so no change to i_graph
		elif isinstance(stmt,x86_ir_cmp):
			if (stmt.left_name[0] != '$'):
				R = set([stmt.left_name])
			if(stmt.right_name[0] != '$'):
				R = R | set([stmt.right_name])
			L_before = (L_after - W) | R
			#There is no write it just changes the flag register
		elif isinstance(stmt,If):
			lb1,g1  = build_i_graph(stmt.tests[0][1].nodes, L_after)
			lb2,g2 = build_i_graph(stmt.else_.nodes, L_after)
			if isinstance(stmt.tests[0][0],Name):
				testVar = stmt.tests[0][0].name
			else:
				raise Exception ("In the If the testVar was not a Name" + str(stmt.tests[0][0]))
			L_before = set([stmt.tests[0][0].name]) | lb1 | lb2 
			for x in g1.keys():
				i_graph[x] = i_graph[x] | g1[x]
			for x in g2.keys():
				i_graph[x] = i_graph[x] | g2[x]
		elif isinstance(stmt,While):
			lbefore = set()
			while True:
				lb,g1 = build_i_graph(stmt.body.nodes,lbefore | L_after)
				if lb != lbefore:
					lbefore = lb
				else:
					break
			L_before = set([stmt.test.name]) | lb
			for x in g1.keys():
				i_graph[x] = i_graph[x] | g1[x]
		elif isinstance(stmt,x86_ir_leave):
			L_before = L_after
		elif isinstance(stmt,x86_ir_ret):
			L_before = L_after
		else:
			raise Exception( "Something is not being acconted for in the build i_graph " + str(stmt))
		L_after = L_before
	return L_before , i_graph




'''
Algorithm: DSATUR
Input: the inference graph G
Output: an assignment color(v) for each node v \in G

W  <- vertices(G)
while W != \empty do
pick a node u from W with the highest saturation,
    breaking ties randomly
find the lowest color c that is not in {color(v) | v \in Adj(v)}
color(u) = c
W <- W - {u}
'''
def DSATURV2(i_graph):
	global unspillable
	#we could also remove from W each of the variables we have already assinged to the stack.
	overflowIndex = 0
	all_colors = set(['%eax','%ebx','%ecx','%edx','%esi','%edi'])
	# Now initialize W which we will call saturation and maintian both in the same place
	#saturtation maps var -> set of the neighbors colors
	saturation = {}
	for node in i_graph.keys():
		saturation[node] = set([])
	del saturation['%eax']
	del saturation['%ecx']
	del saturation['%edx']
	#need to remove colors (registers) that interfere with each node in the W due to caller-save stuff
	for node in i_graph['%eax']:
		saturation[node] = saturation[node] | set(['%eax'])
	for node in i_graph['%ecx']:
		saturation[node] = saturation[node] | set(['%ecx'])	
	for node in i_graph['%edx']:
		saturation[node] = saturation[node] | set(['%edx'])
	#while W != \empty do
	#Saturation[node] are the colors of all the neighbor nodes... this is the same as not_ok_colors in the original implementation
	#think W can just be saturation as those are the nodes that need to be colored		
	while(saturation):
		
		maxsat = max(saturation.items(), key=lambda x:len(x[1]))
		maxsatvars =[key for key in saturation if len(saturation[key])==len(maxsat[1])]
		unspill_maxsatvars = [key for key in maxsatvars if key in unspillable]
		if (unspill_maxsatvars != []):
			maxsatvars = unspill_maxsatvars
		#pick a node u from W with the highest saturation...breaking ties based on degree of each node
		if len(maxsatvars) > 1:

			foo = {}
			for x in maxsatvars:
				foo[x] = len(i_graph[x])
			max_value =  max(foo.iteritems(),key=operator.itemgetter(1))[1]
			u_list = [key for key in foo.keys() if foo[key]==max_value]
			u = u_list[0]
		else:
			u = maxsatvars[0]
		# find the lowest color c that is not in {color(v) | v \in Adj(u)}
		colors_available = list(all_colors-saturation[u])
		if colors_available:
			c = colors_available[0]
		else:
			overflowIndex = overflowIndex + 1
			c = str(-4*(overflowIndex)) + "(%ebp)"
		var_colors[u] = c

		#Now I need to update all the neighbors
		if c[0] != '-':
			for v in i_graph[u]:
				if v in saturation:
					saturation[v] = saturation[v] | set([c])
				
		#W<- W - {u}
		del saturation[u]
	return overflowIndex
		
def rename_var(ast,local_vars):
	global vIndex
	if isinstance(ast,Module):
		return (Module(None,rename_var(ast.node,local_vars)))
	elif isinstance(ast,Stmt):
		stmtList = []
		for x in  ast.nodes:
			stmtList = stmtList +  [rename_var(x,local_vars)]
		return Stmt(stmtList)
	elif isinstance(ast,Printnl):
		return  Printnl([rename_var(ast.nodes[0],local_vars)],ast.dest)
	elif isinstance(ast,Discard):
		return Discard(rename_var(ast.expr,local_vars))
	elif isinstance(ast,Assign):
		if isinstance(ast.nodes[0],AssName):
			aExpr = rename_var(ast.expr,local_vars)
			usr_var_name = ast.nodes[0].name
			#if not usr_var_name in usr_var_map.values():
			var_name  =  local_vars[usr_var_name]
			#else:
			#var_name = usr_var_name
				
			return Assign([AssName(var_name, 'OP_ASSIGN')], aExpr)
		elif isinstance(ast.nodes[0],Subscript):
			sExpr = rename_var(ast.nodes[0].subs[0],local_vars)
			aExpr = rename_var(ast.expr,local_vars)
			usr_var_name = ast.nodes[0].expr.name
			#if not usr_var_name in usr_var_map.values():
			var_name  =  local_vars[usr_var_name]
			#else:
			#	var_name = usr_var_name
			return Assign([Subscript(Name(var_name), 'OP_ASSIGN', [sExpr])], aExpr)
		else:
			raise Exception("something is wrong assign.nodes[0] = " + str(ast.nodes[0]))
	elif isinstance(ast,set_attr):
		cExpr = rename_var(ast.c,local_vars)
		vExpr = rename_var(ast.val,local_vars)
		generateStringLabel(ast.attr)
		return set_attr(cExpr,ast.attr,vExpr)
	elif isinstance (ast, Add):
		lExpr = rename_var(ast.left, local_vars)
		rExpr = rename_var(ast.right, local_vars)
		return  Add([lExpr,rExpr])
	elif isinstance (ast, UnarySub):
		aexpr = rename_var(ast.expr,local_vars)
		return UnarySub(aexpr)
	elif isinstance(ast, Let):
		#vexpr = rename_var(ast.var,local_vars)
		lexpr = rename_var(ast.rhs,local_vars)
		bexpr = rename_var(ast.body,local_vars)
		return Let(ast.var,lexpr,bexpr)
	elif isinstance(ast, Const):
		return ast
	elif isinstance(ast,Dict):
		renamedItems = []
		for pair in ast.items:
			newPair = [(rename_var(pair[0],local_vars),rename_var(pair[1],local_vars))]
			renamedItems = renamedItems + newPair
		return Dict(renamedItems)
	elif isinstance(ast,List):
		return List([rename_var(s,local_vars) for s in ast.nodes])
	elif isinstance(ast, Name):
		if ast.name == 'True' or ast.name == 'False':
			return ast
		else:
			if ast.name in  local_vars:
				return Name(local_vars[ast.name])
			else:
				return Name(ast.name)
	elif isinstance(ast,CallFunc):
		if isinstance(ast.node,Name):
			if ast.node.name == 'input':
			     return ast
			else:
				ast.node.name = local_vars[ast.node.name]
				renamed_args = [rename_var(s,local_vars) for s in ast.args]
				ast.args = renamed_args
			        return  ast
		
		elif isinstance(ast.node,Lambda):
			local_scope = copy.copy(local_vars)
			new_args = []
			for var in ast.node.argnames:
				newVar = map_a_local(var)
				local_scope[var] = newVar
				new_args = new_args + [newVar]
			expr = rename_var(ast.node.code,local_scope)
			ast.node =  Lambda(new_args, [], 0, expr)
			return ast
		elif isinstance(ast.node,CallFunc):
			return CallFunc(CallFunc(rename_var(ast.node.node,local_vars), [rename_var(s,local_vars) for s in ast.node.args], None, None), [rename_var(s,local_vars) for s in ast.args], None, None)
		elif isinstance(ast.node,get_attr):
			renamed_args = [rename_var(s,local_vars) for s in ast.args]
			ast.args = renamed_args
			ast.node.c = rename_var(ast.node.c,local_vars)
			return  ast
		elif isinstance(ast.node,IfExp):
			ast.args = [rename_var(s,local_vars) for s in ast.args]
			ast.node = rename_var(ast.node,local_vars)
			return ast
	elif isinstance(ast,IfExp):
		testExpr = rename_var(ast.test,local_vars)
		thenExpr = rename_var(ast.then,local_vars)
		elseExpr = rename_var(ast.else_,local_vars)
		return IfExp(testExpr,thenExpr,elseExpr)
	elif isinstance(ast,If):
		testExpr = rename_var(ast.tests[0][0],local_vars)
		thenExpr = rename_var(ast.tests[0][1],local_vars)
		elseExpr = rename_var(ast.else_,local_vars)
		return If([(testExpr,thenExpr)],elseExpr)
	elif isinstance(ast,While):
		testExpr = rename_var(ast.test,local_vars)
		bodyExpr = rename_var(ast.body,local_vars)
		return While(testExpr, bodyExpr, None)
	elif isinstance(ast,Compare):
		lExpr = rename_var(ast.expr, local_vars)
		rExpr = rename_var(ast.ops[0][1], local_vars)
		return Compare(lExpr, [(ast.ops[0][0],rExpr)])
	elif isinstance(ast,Subscript):
		lExpr = rename_var(ast.expr, local_vars)
		rExpr = rename_var(ast.subs[0], local_vars)
		return Subscript(lExpr, ast.flags, [rExpr])
	elif isinstance(ast,And):
		lExpr =  rename_var(ast.nodes[0], local_vars)
		rExpr = rename_var(ast.nodes[1], local_vars)
		return And([lExpr,rExpr])
	elif isinstance(ast,Or):
		lExpr =  rename_var(ast.nodes[0], local_vars)
		rExpr = rename_var(ast.nodes[1], local_vars)
		return Or([lExpr,rExpr])
		
	elif isinstance(ast,Not):
		aexpr = rename_var(ast.expr,local_vars)
		return Not(aexpr)
	elif (ast in ('==','!=','is')):
		return ast
	elif isinstance(ast,Function):
		new_func_name = local_vars[ast.name]
		ast.name = new_func_name
		return ast
	elif isinstance(ast, get_attr):
		#print ast
		generateStringLabel(ast.attr)
		ast.c = rename_var(ast.c,local_vars)
		return ast
	elif isinstance(ast,has_attr):
		ast.o = rename_var(ast.o,local_vars)
		return ast
	elif isinstance(ast,Lambda):
		local_scope = copy.copy(local_vars)
		new_args = []
		for var in ast.argnames:
			newVar = map_a_local(var)
			local_scope[var] = newVar
			new_args = new_args + [newVar]
		expr = rename_var(ast.code,local_scope)
		return Lambda(new_args, [], 0, expr)
	elif isinstance(ast,create_class):
		new_bases = []
		for base in ast.bases.nodes:
			new_bases = new_bases + [Name(local_vars[base.name])]
		ast.bases = List(new_bases)
		return ast
	elif isinstance(ast,Return):
		return Return(rename_var(ast.value,local_vars))
	else:
		raise Exception("Error "+ str(ast))

def walk_to_rename(stmt_list,vars_to_inherit):
	#get the locals for this scope
	local_vars = get_locals(stmt_list)
	#now rename locals
	current_var_map = copy.copy(vars_to_inherit)
	for vars in local_vars:
		current_var_map[vars] = map_a_local(vars)	
	for stmt in stmt_list:
		if isinstance(stmt,Function):
			func_locals = copy.copy(current_var_map)
			for var in stmt.argnames:
				func_locals[var] = map_a_local(var)
			localsF = walk_to_rename(stmt.code.nodes,func_locals)
			newArgs = []
			for var in stmt.argnames:
				newArgs = newArgs + [localsF[var]]
			stmt.argnames = newArgs
			stmt.code = rename_var(stmt.code,localsF)
	return current_var_map




def map_a_local(var):
	global uni_index
	uni_index = uni_index +1
	newVar = str(var) +"_"+ str(uni_index)
	#if var in usr_var_map:
	var_colors[newVar] = ""
	return newVar
def get_locals(ast):
	local_vars = set([])
	#Always want to pass this Stmts
	for stmt in ast:
		if isinstance(stmt,Assign):
			if isinstance(stmt.nodes[0],AssName):
				var = stmt.nodes[0].name
				#if not var in usr_var_map.values():
				local_vars = local_vars | set([var])
		if isinstance(stmt,While):
			local_vars = local_vars | get_locals(stmt.body)
		if isinstance(stmt,If):
			local_vars = local_vars | get_locals(stmt.tests[0][1]) | get_locals(stmt.else_)
		elif isinstance(stmt,Function):
			func_name = stmt.name
			local_vars = local_vars | set([func_name]) | set(stmt.argnames)
	return local_vars
def uniquify_variables(ast):
	localVars = walk_to_rename(ast.node.nodes,{})
	return  rename_var(ast,localVars)
def create_closures(ast):
	global top_level_functions
	if isinstance(ast,Module):
		return (Module(None,create_closures(ast.node)))
	elif isinstance(ast,Stmt):
		stmtList = []
		for x in  ast.nodes:
			stmtList = stmtList +  [create_closures(x)]
		return Stmt(stmtList)
	elif isinstance(ast,Printnl):
		return  Printnl([create_closures(ast.nodes[0])],ast.dest)
	elif isinstance(ast,Discard):
		return Discard(create_closures(ast.expr))
	elif isinstance(ast,Assign):
		if isinstance(ast.nodes[0],AssName):
			rhs = create_closures(ast.expr)
			if ast.nodes[0].name in vars_to_heapify:
				return Assign([Subscript(Name(ast.nodes[0].name), 'OP_ASSIGN', [InjectFrom('int', Const(0))])], rhs )
			else: return Assign([AssName(ast.nodes[0].name, 'OP_ASSIGN')], rhs)
		elif isinstance(ast.nodes[0],Subscript):
			#This is the case like 'x[1] = 4'
			sExpr = create_closures(ast.nodes[0].subs[0])
			aExpr = create_closures(ast.expr)
			usr_var_name = ast.nodes[0].expr.name
			var_name = usr_var_name
			return Assign([Subscript(Name(var_name), 'OP_ASSIGN', [sExpr])], aExpr)
		else:
			raise Exception("something is wrong assign.nodes[0] = " + str(ast.nodes[0]))
	elif isinstance (ast, Add):
		lExpr = create_closures(ast.left)
		rExpr = create_closures(ast.right)
		return  Add([lExpr,rExpr])
	elif isinstance(ast,get_attr):
		ast.expr = create_closures(ast.c)
		return ast
			
	elif isinstance(ast,is_unbound_method):
		ast.val = create_closures(ast.val)
		return ast
	elif isinstance(ast,is_bound_method):
		ast.val = create_closures(ast.val)
		return ast
	elif isinstance(ast,get_receiver):
		ast.o = create_closures(ast.o)
		return ast
			
	elif isinstance (ast, UnarySub):
		aexpr = create_closures(ast.expr)
		return UnarySub(aexpr)
	elif isinstance(ast, Const):
		return ast 
	elif isinstance(ast, Name):
		if ast.name in vars_to_heapify:
			return  GetSubScript(ast, InjectFrom('int', Const(0))) 
		else:
			return ast
	elif isinstance(ast,CallFunc):
		if isinstance(ast.node,Name):
			if (ast.node.name == 'input'):
			      return  ast
			else:
				input_list = [create_closures(s) for s in ast.args]
			return get_fun_ptr(create_closures(Name(ast.node.name)),[get_free_vars(create_closures(Name(ast.node.name))),input_list])
		elif isinstance(ast.node,Lambda):
			v1 = generator()
			v2 = generator()
			the_lambda = ast.node
			ast.node = Name(v1)
			return Let(Name(v1),create_closures(the_lambda),create_closures(ast))
		elif isinstance(ast.node,CallFunc):
			#so this version is only if you have somthing like (f(1))(2)
			input1 = [create_closures(s) for s in ast.node.args]
			input2 = [create_closures(s) for s in ast.args]
			result1 = generator()
			#let result1 = get_fun_ptr(Name(ast.node.name),[get_free_vars(ast.node.name),input1]) in  get_fun_ptr(Name(result1),[get_free_vars(result1),input2])
			newNode = Let(Name(result1),get_fun_ptr(create_closures(ast.node.node),[get_free_vars(create_closures(Name(ast.node.node.name))),input1]), get_fun_ptr(Name(result1),[get_free_vars(Name(result1)),input2]))
			return newNode
		else: raise Exception ("Something is going crazy in the  node...." + str(ast))
	elif isinstance(ast,IfExp):
		testExpr = create_closures(ast.test)
		thenExpr = create_closures(ast.then)
		elseExpr = create_closures(ast.else_)
		return IfExp(testExpr,thenExpr,elseExpr)
	elif isinstance(ast,If):
		testExpr = create_closures(ast.tests[0][0])
		thenExpr = create_closures(ast.tests[0][1])
		elseExpr = create_closures(ast.else_)
		return If([(testExpr,thenExpr)],elseExpr)
	elif isinstance(ast,While):
		testExpr = create_closures(ast.test)
		bodyExpr = create_closures(ast.body)
		return While(testExpr,bodyExpr,None)

	elif isinstance(ast,Compare):
		lExpr = create_closures(ast.expr)
		rExpr = create_closures(ast.ops[0][1])
		return Compare(lExpr, [(ast.ops[0][0],rExpr)])
	elif isinstance(ast,Subscript):
		lExpr = create_closures(ast.expr)
		rExpr = create_closures(ast.subs[0])
		return Subscript(lExpr, ast.flags, [rExpr])
	elif isinstance(ast,GetSubScript):
		c = create_closures(ast.c)
		key = create_closures(ast.key)
		return GetSubScript(c,key)
	elif isinstance(ast,SetSubScript):
		c = create_closures(ast.c)
		key = create_closures(ast.key)
		val = create_closures(ast.val)
		return SetSubScript(c,key,val)
	elif isinstance(ast,And):
		lExpr =  create_closures(ast.nodes[0])
		rExpr = create_closures(ast.nodes[1])
		return And([lExpr,rExpr])
	elif isinstance(ast,Or):
		lExpr =  create_closures(ast.nodes[0])
		rExpr = create_closures(ast.nodes[1])
		return Or([lExpr,rExpr])
		
	elif isinstance(ast,Not):
		aexpr = create_closures(ast.expr)
		return Not(aexpr)
	elif (ast in ('==','!=','is')):
		return ast
	elif isinstance(ast,Function):
		raise Exception("functions should no longer exist at this point....(in the closure)")
	elif isinstance(ast,Lambda):
		#so here we want to create a new lambda name
		new_name = generate_lambda_name()
		new_list = "free_vars_" + str(new_name)
		var_colors[new_list] = ""
		free_vars_list = free_vars(ast) - get_locals(ast.code)# - func_names # not sure that removing func_names is a good plan
		if debug_flag:
			print ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
			print "the free_vars were"
			print free_vars_list
			print "for the function"
			print new_name
			print " and the locals were"
			print get_locals(ast.code)
			print "if we add the params to the locals...."
			print get_locals(ast.code) | set(ast.argnames)
		my_locals = get_locals(ast.code)
		heapify_assigns = []
		#So this does not change with renaming at all
		for var in my_locals:
			if var in vars_to_heapify:
				new_var = generator()
				new_assign = Assign([AssName(var, 'OP_ASSIGN')], CreateList(InjectFrom('int', Const(1)), new_var, [SetSubScript(Name(new_var), InjectFrom('int', Const(0)), InjectFrom('int', Const(0)))]))
				heapify_assigns = heapify_assigns + [new_assign]
		for var in  set(ast.argnames):
			if var in vars_to_heapify:
				new_var = generator()
				new_assign = Assign([AssName(var, 'OP_ASSIGN')], CreateList(InjectFrom('int', Const(1)), new_var, [SetSubScript(Name(new_var), InjectFrom('int', Const(0)), Name(var))]))
				heapify_assigns = heapify_assigns + [new_assign]



		#this is for y_0 = [0]
		#Assign([AssName('y_0', 'OP_ASSIGN')], CreateList(InjectFrom('int', Const(1)), 'jtg_tmp0', [SetSubScript(Name('jtg_tmp0'), InjectFrom('int', Const(0)), InjectFrom('int', Const(0)))]))
				
		#this is for y_0 = [y_0]
		#Assign([AssName('y_0', 'OP_ASSIGN')], CreateList(InjectFrom('int', Const(1)), 'jtg_tmp0', [SetSubScript(Name('jtg_tmp0'), InjectFrom('int', Const(0)), Name('y_0'))]))

		
		length = InjectFrom('int',Const(len(free_vars_list)))
		if debug_flag:
			print "so we expect freevars to have "+ str(length.arg.value) + " element(s)"
		freeList = []
		free_assigns =[]
		free_assigns2 = []
		
		#### HERE IS WHERE WE CREATE THE freeList AND MAKE freeList A NICE pyobj
		#this will also add all of the x = free_vars[...] stuff
		for i,s in list(enumerate(free_vars_list)):
			freeList[len(freeList):] = [SetSubScript(Name(new_list),InjectFrom('int',Const(i)),Name(s))]
			free_vars_let_name = generator()
			free_vars_tag = generator()
			subscript_let = generator()
			free_assigns = free_assigns + [Assign([AssName(s, 'OP_ASSIGN')], Let(Name(free_vars_let_name), Name(new_list), Let(Name(free_vars_tag), GetTag(Name(free_vars_let_name)), IfExp(Or([Compare(Name(free_vars_tag), [('==', 'int')]), Compare(Name(free_vars_tag), [('==', 'bool')])]), ERROREXIT('Type Error'), Let(Name(subscript_let), InjectFrom('int', Const(i)), GetSubScript(Name(free_vars_let_name), Name(subscript_let)))))))]
		if debug_flag:
			print "so we are adding the following free assigns to the body"
			print free_assigns
			print "but we use to add....instead where .... = "
			print free_assigns2
			print "and the following heapify stmts"
			print heapify_assigns
			print ';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
		#call this function on the body of lambda
		body = create_closures(ast.code)
		body.nodes = free_assigns + heapify_assigns + body.nodes
		if debug_flag:
			print "so the final body for "+ new_name + " is ....."
			print body.nodes
			print "88888888888888888888888888888888888888888888888888888"
		#add a Function Node to top functions
		#want to add to the body all the free_vars.... stuff
		###########defaults holds the free_var list....this so it is available in ir_translation ############
		newFunction = Function(None, new_name, ast.argnames,new_list, 0, None, body)
		top_level_functions = top_level_functions + [newFunction]
		final_free_list = generator()
		#let final_free_list = CreateList(length,new_list,freeList) in InjectFrom('big',create_closure(new_name, final_free_list))
		#I am not sure if this should be final_free_lis in the let or if it should be the new_list name....
		new_node = Let(Name(final_free_list),CreateList(length,new_list,freeList), InjectFrom('big',create_closure(new_name, Name(final_free_list))))
		#new_node = InjectFrom('big',create_closure(new_name, final_free_list))
		return new_node
	elif isinstance(ast,CreateList):
		list_name = ast.list_name
		closed_list_items = [create_closures(e) for e in ast.listItems]
		return CreateList(ast.length,list_name,closed_list_items)
	elif isinstance(ast,CreateDict):
		dictName = ast.dict_name
		closed_dict_items = [create_closures(e) for e in ast.dictItems]
		return CreateDict(dictName,closed_dict_items)
	elif isinstance(ast,Return):
		return Return(create_closures(ast.value))
	elif isinstance(ast,Let):
		body = create_closures(ast.body)
		rhs = create_closures(ast.rhs)
		var = create_closures(ast.var)
		return Let(var,rhs,body)
	elif isinstance(ast,GetTag):
		return GetTag(create_closures(ast.arg))
	elif isinstance(ast,ERROREXIT):
		return ast
	elif isinstance(ast,ProjectTo):
		return ProjectTo(ast.typ,create_closures(ast.arg))
	elif isinstance(ast,InjectFrom):
		return InjectFrom(ast.typ,create_closures(ast.arg))
	elif isinstance(ast,addBig):
		return addBig(create_closures(ast.left_name),create_closures(ast.right_name))
	elif isinstance(ast,is_true):
		return is_true(create_closures(ast.name))
	elif isinstance(ast,equalBig):
		return equalBig(create_closures(ast.left_name),create_closures(ast.right_name))
	elif isinstance(ast,create_class):
		return ast
	elif isinstance(ast,create_object):
		return ast
	elif isinstance(ast,get_function):
		return get_function(create_closures(ast.o))
	elif isinstance(ast,is_class):
		return is_class(create_closures(ast.c))
	elif isinstance(ast,nequalBig):
		return nequalBig(create_closures(ast.left_name),create_closures(ast.right_name))
	elif isinstance(ast,set_attr):
		return set_attr(create_closures(ast.c),ast.attr,create_closures(ast.val))
	elif isinstance(ast,get_attr):
		return get_attr(create_closures(ast.c),ast.attr)
	elif isinstance(ast,has_attr):
		return has_attr(create_closures(ast.o),ast.attr)
	elif (ast in ('int','bool','big','==','!=','is')):
		return ast		
	else:
		raise Exception("Error "+ str(ast))


def free_vars(n):
	if isinstance(n,Module):
		return free_vars(n.node)
	elif isinstance(n,Stmt):
		free_in_stmt = set([])
		
		for foo in n.nodes:
			free_in_stmt = free_in_stmt | free_vars(foo)
		return free_in_stmt
	elif isinstance(n,Const):
		return set([])
	elif isinstance(n,Name):
		if n.name == 'True' or n.name == 'False' or n.name in usr_var_map.values():
			return set([])
		else:
			return set([n.name])
	elif isinstance(n,Add):
		return free_vars(n.left) | free_vars(n.right)
	elif isinstance(n,And):
		return free_vars(n.nodes[0]) | free_vars(n.nodes[1])
	elif isinstance(n,Or):
		return free_vars(n.nodes[0]) | free_vars(n.nodes[1])
	elif isinstance(n,Not):
		return free_vars(n.expr) 
	elif isinstance(n,UnarySub):
		return free_vars(n.expr) 
	elif isinstance(n,IfExp):
		return free_vars(n.test) | free_vars(n.then) | free_vars(n.else_)
	elif isinstance(n,If):
		return free_vars(n.tests[0][0]) | free_vars(n.tests[0][1]) | free_vars(n.else_)
	elif isinstance(n,While):
		return free_vars(n.test) | free_vars(n.body)
	elif isinstance(n,CallFunc):
		fv_args = [free_vars(e) for e in n.args]
		free_in_args = reduce(lambda a,b: a | b, fv_args, set([]))
		return free_vars(n.node) | free_in_args
	elif isinstance (n,Lambda):
		return free_vars(n.code) - set(n.argnames) - get_locals(n.code)
	elif isinstance (n,create_class):
		return set([]) #this may change with bases
	elif isinstance (n,create_object):
		return set([])
	elif isinstance (n,get_function):
		return free_vars(n.o)
	elif isinstance(n,is_unbound_method):
		return free_vars(n.val)
	elif isinstance(n,is_bound_method):
		return free_vars(n.val)
	elif isinstance(n,get_receiver):
		return free_vars(n.o)
	elif isinstance (n,is_class):
		return free_vars(n.c)
	elif isinstance(n,CreateList):
		#Each item in listItems is a setSubscript
		free_list = set([])
		for e in n.listItems:
			free_list = free_list | free_vars(e) 
		return free_list
	elif isinstance(n,CreateDict):
		free_list = set([])
		for e in n.dictItems:
			free_list = free_list | free_vars(e)
		return free_list
	elif isinstance(n,SetSubScript):
		#I think that right here we should be removing n.c same with GetSubScript...actually maybe not with get subscript
		return  free_vars(n.key) | free_vars(n.val) # | free_vars(n.c) 
	elif isinstance(n,GetSubScript):
		return  free_vars(n.key) #|  free_vars(n.c) 		
	elif isinstance(n,Compare):
		return free_vars(n.expr) | free_vars(n.ops[0][1])
	elif isinstance(n,Subscript):
		#i think this is a subscript occuring on the rhs
		return free_vars(n.expr) | free_vars(n.subs)
	elif isinstance(n,Assign):
		if isinstance(n.nodes[0],AssName):
			return free_vars(n.expr)
		elif isinstance(n.nodes[0],Subscript):
			return (free_vars(n.expr) | free_vars(n.nodes[0].subs[0]))
	elif isinstance(n,Let):
		return (free_vars(n.body) | free_vars(n.rhs)) - set([n.var.name])
	elif isinstance(n,GetTag):
		return free_vars(n.arg)
	elif isinstance(n,Return):
		return free_vars(n.value)
	elif isinstance(n,get_attr):
		return free_vars(n.c) 
	elif isinstance(n,ERROREXIT):
		return set([])
	elif isinstance(n,Printnl):
		return free_vars(n.nodes[0])
	elif isinstance(n,Discard):
		return free_vars(n.expr)
	elif isinstance(n,ProjectTo):
		return free_vars(n.arg)
	elif isinstance(n,InjectFrom):
		return free_vars(n.arg)
	elif isinstance(n,addBig):
		return free_vars(n.right_name) | free_vars(n.left_name)
	elif isinstance(n,is_true):
		return free_vars(n.name)
	elif isinstance(n,equalBig):
		return free_vars(n.right_name) | free_vars(n.left_name)
	elif isinstance(n,nequalBig):
		return free_vars(n.right_name) | free_vars(n.left_name)
	elif isinstance(n,set_attr):
		return free_vars(n.c) | free_vars(n.val)
	elif isinstance(n,get_attr):
		return free_vars(n.c)
	elif isinstance(n,has_attr):
		return free_vars(n.o)
	elif (n in ('int','bool','big','==','!=','is')):
		return set([])
	else:
		raise Exception("In free_vars a case was missed" + str(n))


def to_heapify(n):
	if isinstance(n,Module):
		return to_heapify(n.node)
	elif isinstance(n,Stmt):
		node_heapify =set([])
		for foo in n.nodes:
			node_heapify = node_heapify | to_heapify(foo)
		return node_heapify
	elif isinstance(n,Lambda):
		return to_heapify(n.code) | (free_vars(n)-get_locals(n.code))
	elif isinstance(n,Const):
		return set([])
	elif isinstance(n,Name):
		return set([])
	elif isinstance(n,Add):
		return to_heapify(n.left) | to_heapify(n.right)
	elif isinstance(n,And):
		return to_heapify(n.nodes[0]) | to_heapify(n.nodes[1])
	elif isinstance(n,Or):
		return to_heapify(n.nodes[0]) | to_heapify(n.nodes[1])
	elif isinstance(n,Not):
		return to_heapify(n.expr) 
	elif isinstance(n,UnarySub):
		return to_heapify(n.expr) 
	elif isinstance(n,IfExp):
		return to_heapify(n.test) | to_heapify(n.then) | to_heapify(n.else_)
	elif isinstance(n,If):
		return to_heapify(n.tests[0][0]) | to_heapify(n.tests[0][1]) | to_heapify(n.else_)
	elif isinstance(n,While):
		return to_heapify(n.test) | to_heapify(n.body)
	elif isinstance(n,CallFunc):
		return set([])
	elif isinstance(n,create_class):
		return set([])
	elif isinstance(n,create_object):
		return to_heapify(n.c)
	elif isinstance(n,CreateList):
		temp = set([])
		for each in  n.listItems:
			temp = temp | to_heapify(each)
		return temp
		#Each item in listItems is a setSubscript
	elif isinstance(n,CreateDict):
		temp = set([])
		for each  in n.dictItems:
			temp = temp | to_heapify(each)
		return temp
		#[to_heapify(e) for e in n.dictItems]
	elif isinstance(n,SetSubScript):
		return to_heapify(n.c) | to_heapify(n.key) | to_heapify(n.val)
	elif isinstance(n,GetSubScript):
		return to_heapify(n.c) | to_heapify(n.key)		
	elif isinstance(n,Compare):
		return to_heapify(n.expr) | to_heapify(n.ops[0][1])
	elif isinstance(n,Subscript):
		#i think this is a subscript occuring on the rhs
		return to_heapify(n.expr) | to_heapify(n.subs)
	elif isinstance(n,Assign):
		if isinstance(n.nodes[0],AssName):
			return to_heapify(n.expr)
		elif isinstance(n.nodes[0],Subscript):
			return to_heapify(n.expr) | to_heapify(n.nodes[0].subs[0]) | to_heapify(n.nodes[0].expr)
		'''elif isinstance(n.nodes[0],AssAttr):
			return to_heapify(n.nodes[0].expr) | to_heapify(n.expr) #do we need to heapify the attr?
		'''
	elif isinstance(n,Let):
		return to_heapify(n.body) | to_heapify(n.rhs)
	elif isinstance(n,get_attr):
		return to_heapify(n.c)
	elif isinstance(n,is_unbound_method):
		return to_heapify(n.val)
	elif isinstance(n,is_bound_method):
		return to_heapify(n.val)
	elif isinstance(n,get_receiver):
		return to_heapify(n.o)
	elif isinstance(n,set_attr):
		return to_heapify(n.c) | to_heapify(n.val)
	elif isinstance(n,has_attr):
		return to_heapify(n.o)
	elif isinstance(n,GetTag):
		return to_heapify(n.arg)
	elif isinstance(n,Return):
		return to_heapify(n.value)
	elif isinstance(n,ERROREXIT):
		return set([])
	elif isinstance(n,Printnl):
		return to_heapify(n.nodes[0])
	elif isinstance(n,Discard):
		return to_heapify(n.expr)
	elif isinstance(n,ProjectTo):
		return to_heapify(n.arg)
	elif isinstance(n,InjectFrom):
		return to_heapify(n.arg)
	elif isinstance(n,addBig):
		return to_heapify(n.right_name) | to_heapify(n.left_name)
	elif isinstance(n,is_true):
		return to_heapify(n.name)
	elif isinstance(n,is_class):
		return to_heapify(n.c)
	elif isinstance(n,get_function):
		return to_heapify(n.o)
	elif isinstance(n,equalBig):
		return to_heapify(n.right_name) | to_heapify(n.left_name)
	elif isinstance(n,nequalBig):
		return to_heapify(n.right_name) | to_heapify(n.left_name)
	elif (n in ('int','bool','big','==','!=','is')):
		return set([])
	else:
		raise Exception("In to_heapify a case was missed" + str(n))


def detectSpillCollision(x86_IR):
	spillCollision = False
	global unspillable
	for  i, stmt in  enumerate(x86_IR):
		if isinstance(stmt,x86_ir_move):
			#the isdigit case is for something like 8(%ebp)
			if (stmt.src_name[0] == '$' or  stmt.src_name[0] == '%'):
				continue
			else:
				if stmt.src_name[0].isdigit():
					src = stmt.src_name[0]
				else:
					src = var_colors[stmt.src_name]
			if (stmt.dest_name[0] == '%'):
				continue
			else:
				dest = var_colors[stmt.dest_name]	
			if (src[0] == '-' or src[0].isdigit()) and dest[0]=='-':
				spillCollision = True
				new_tmp = generator()
				var_colors[new_tmp] = "u"
				unspillable = unspillable + [new_tmp]
				new_x86_stmt = x86_ir_move(new_tmp, stmt.dest_name)
				stmt.dest_name = new_tmp
				x86_IR.insert(i+1, new_x86_stmt)
		elif isinstance(stmt,x86_ir_add):
			if (stmt.left_name[0] == '$' or  stmt.left_name[0] == '%'):
				left = stmt.left_name
			else:
				left = var_colors[stmt.left_name]
			if (stmt.right_name[0] == '$' or  stmt.right_name[0] == '%'):
				right = stmt.right_name
			else:	
				right = var_colors[stmt.right_name]
			if left[0] == '-' and right[0] == '-':
				spillCollision = True
				var_colors[stmt.right_name] = "u"
				unspillable = unspillable + [stmt.right_name]
		elif isinstance(stmt,x86_ir_neg):
			pass
		elif isinstance(stmt, x86_ir_call):
			pass
		elif isinstance(stmt,x86_ir_call_star):
			pass
		elif isinstance(stmt,x86_ir_push):
			pass
		elif isinstance(stmt,x86_ir_or):
			pass
		elif isinstance(stmt,x86_ir_not):
			pass
		elif isinstance(stmt,x86_ir_leave):
			pass
		elif isinstance(stmt,x86_ir_ret):
			pass
		elif isinstance(stmt,x86_ir_and):
			pass
		elif isinstance(stmt,x86_ir_sar):
			pass
		elif isinstance(stmt,x86_ir_sal):
			pass
		elif isinstance(stmt,x86_ir_cmp):
			if (stmt.left_name[0] == '$' or  stmt.left_name[0] == '%'):
				left = stmt.left_name
			else:
				left = var_colors[stmt.left_name]
			if (stmt.right_name[0] == '$' or  stmt.right_name[0] == '%'):
				right = stmt.right_name
			else:	
				right = var_colors[stmt.right_name]
			if left[0] == '-' and right[0] == '-':
				spillCollision = True
				var_colors[stmt.right_name] = "u"
				unspillable = unspillable + [stmt.right_name]
		elif isinstance(stmt,x86_ir_movzbl):
			pass
		elif isinstance(stmt,x86_ir_sete):
			pass 
		elif isinstance(stmt,x86_ir_setne):
			pass
		elif isinstance(stmt,If):
			s1  = detectSpillCollision(stmt.tests[0][1].nodes)
			s2 = detectSpillCollision(stmt.else_.nodes)
			if(s1 or s2):
				spillCollision = True
		elif isinstance(stmt,While):
			s1  = detectSpillCollision(stmt.body.nodes)
			if s1:
				spillCollision = True
			
		else:
			raise Exception("Something is not being accounted for in the detection of spillCollisions")
			
	return spillCollision

def coloring(x86_IR,func_name):
	global overIndex_dict
	#liveness and build are done at the same time now
	junk, i_graph = build_i_graph(x86_IR,set([]))
	overIndex_dict[func_name] =  DSATURV2(i_graph)

	return detectSpillCollision(x86_IR)

def x86_to_asm_chunk_translate(x86_IR_chunk):

	for stmt in  x86_IR_chunk:
		if isinstance(stmt,x86_ir_move):
			if stmt.src_name != stmt.dest_name :
				f.write("movl " + str(stmt.src_name) + ", " + str(stmt.dest_name) + "\n")
		elif isinstance(stmt,x86_ir_add):
			f.write("addl " + str(stmt.left_name) + ", " + str(stmt.right_name) + "\n")
		elif isinstance(stmt,x86_ir_neg):
			f.write("negl " + str(stmt.src_name)+'\n')
		elif isinstance(stmt, x86_ir_call):
			f.write("call " + stmt.name + "\n")
		elif isinstance(stmt,x86_ir_call_star):
			f.write("call *" +stmt.pointer + "\n")
		elif isinstance(stmt,x86_ir_push):
			f.write("pushl " + str(stmt.to_push) + '\n')
		elif isinstance(stmt,x86_ir_not):
			f.write("notl " + str(stmt.src_name)+'\n')
		elif isinstance(stmt,x86_ir_leave):
			f.write("leave\n")
		elif isinstance(stmt,x86_ir_ret):
			f.write("ret\n")
		elif isinstance(stmt,x86_ir_and):
			f.write("andl " + str(stmt.left_name) + ", " + str(stmt.right_name) + "\n")
		elif isinstance(stmt,x86_ir_or):
			f.write("orl " + str(stmt.left_name) + ", " + str(stmt.right_name) + "\n")
		elif isinstance(stmt,x86_ir_sar):
			f.write("sarl " + str(SHIFT) + ", " + str(stmt.src_name) + "\n")
		elif isinstance(stmt,x86_ir_sal):
			f.write("sall " + str(SHIFT) + ", " + str(stmt.src_name) + "\n")
		elif isinstance(stmt,x86_ir_cmp):
			f.write("cmpl " + str(stmt.left_name) + ", " + str(stmt.right_name) + "\n")
		elif isinstance(stmt,x86_ir_movzbl):
			f.write("movzbl " + '%al' + ", " + str(stmt.right_name) + "\n")
		elif isinstance(stmt,x86_ir_sete):
			f.write("sete %al\n")
		elif isinstance(stmt,x86_ir_setne):
			f.write("setne %al\n")
		elif isinstance(stmt,If):
			elseLabel = generateLabel()
			endLabel = generateLabel()			
			x86_to_asm_chunk_translate([x86_ir_cmp('$0',var_colors[stmt.tests[0][0].name])])
			x86_to_asm_chunk_translate([x86_ir_je(elseLabel)])
			x86_to_asm_chunk_translate(stmt.tests[0][1].nodes)
			x86_to_asm_chunk_translate([x86_ir_jmp(endLabel)])
			x86_to_asm_chunk_translate([x86_ir_label(elseLabel)])
			x86_to_asm_chunk_translate(stmt.else_.nodes)
			x86_to_asm_chunk_translate([x86_ir_label(endLabel)])

		elif isinstance(stmt,While):
			'''
			        test = n.test
				body = self.dispatch(n.body)
				start_label = generate_name('while_start')
				end_label = generate_name('while_end')
		       return [Label(start_label),
			       CMPLInstr(None, [Const(0), test]),
			       JumpEqInstr(end_label)] + \
			       [body] + \
		       [Goto(start_label)] + \
			[Label(end_label)]
			'''
			startlabel = generateLabel()
			endlabel = generateLabel()
			x86_to_asm_chunk_translate([x86_ir_label(startlabel)])
			x86_to_asm_chunk_translate([x86_ir_cmp('$0',var_colors[stmt.test.name])])
			x86_to_asm_chunk_translate([x86_ir_je(endlabel)])
			x86_to_asm_chunk_translate(stmt.body.nodes)
			x86_to_asm_chunk_translate([x86_ir_jmp(startlabel)])
			x86_to_asm_chunk_translate([x86_ir_label(endlabel)])
		elif isinstance(stmt,x86_ir_label):
			f.write(str(stmt.label) + ":\n")
		elif isinstance(stmt,x86_ir_je):
			f.write("je " +str(stmt.label) + "\n")
		elif isinstance(stmt,x86_ir_jmp):
			f.write("jmp " +str(stmt.label) + "\n")
		else:
			raise Exception("Case missed in x86IR -> asm")



def x86ir_to_asm(top_funcs):
	for string in string_label_map:
		f.write(str(string_label_map[string]) + ":\n")
		f.write("         .string "+'"'+ str(string) + '"\n')
	f.write("         .text\n")

	for t_func in top_funcs:
		f.write(".globl "+t_func.name+"\n")
		f.write(t_func.name + ":\n")
		#now I need all the intro crap like saving the calleesave registers
		f.write("pushl %ebp\n")
		f.write("movl %esp, %ebp\n")
		#then each function should have its own "overIndex" i need to set up this dict
		tot_index = (overIndex_dict[t_func.name]+1)*4
		
		s = "subl $" + str(tot_index) + ", %esp #This is to make room for all the variables we will need \n"
		f.write(s)
		f.write("\n")

		if t_func.name != 'main':
			f.write("pushl %ebx\n")
			f.write("pushl %esi\n")
			f.write("pushl %edi\n")
		f.write('#Starting body\n')
		x86_to_asm_chunk_translate(t_func.code)

		f.write("\n")
		#now put the calle_save back
		f.write('#Starting Outro\n')
		if t_func.name != 'main':

			f.write("popl %edi\n")
			f.write("popl %esi\n")
			f.write("popl %ebx\n")
		
		f.write('\n')
		s = "addl $" + str(tot_index) + ", %esp #This is to make room for all the variables we will need \n"
		f.write(s)
		if t_func.name == 'main':
			f.write ("movl $0, %eax # put return value in eax\n")

		f.write("leave\n")
		f.write("ret\n")
		f.write("\n\n")
def x86ir_assign_homes(x86_IR):
	for  i, stmt in  enumerate(x86_IR):
		if isinstance(stmt,x86_ir_move):
			if (stmt.src_name[0] == '$' or  stmt.src_name[0] == '%'or stmt.src_name[0].isdigit()):
				src = stmt.src_name
			else:
				src = var_colors[stmt.src_name] 
			if (stmt.dest_name[0] == '%'):
				dest = stmt.dest_name
			else:
				dest = var_colors[stmt.dest_name]
			stmt.src_name = src
			stmt.dest_name = dest
		elif isinstance(stmt,x86_ir_add):
			if (stmt.left_name[0] == '$' or  stmt.left_name[0] == '%'):
				left = stmt.left_name
			else:
				left = var_colors[stmt.left_name]
			if (stmt.right_name[0] == '$' or  stmt.right_name[0] == '%'):
				right = stmt.right_name
			else:	
				right = var_colors[stmt.right_name]
			stmt.right_name = right
			stmt.left_name = left
		elif isinstance(stmt,x86_ir_neg):
			stmt.src_name =  var_colors[stmt.src_name]
		elif isinstance(stmt, x86_ir_call):
			pass
		elif isinstance(stmt,x86_ir_call_star):
			pass
		elif isinstance(stmt,x86_ir_push):
			if stmt.to_push[0] != '$' and  stmt.to_push[0] != '%':
				stmt.to_push = var_colors[stmt.to_push]
		elif isinstance(stmt,x86_ir_not):
			stmt.src_name =  var_colors[stmt.src_name]
		elif isinstance(stmt,x86_ir_leave):
			pass
		elif isinstance(stmt,x86_ir_ret):
			pass
		elif isinstance(stmt,x86_ir_and):
			stmt.right_name =  var_colors[stmt.right_name]
		elif isinstance(stmt,x86_ir_or):
			stmt.right_name =  var_colors[stmt.right_name]
		elif isinstance(stmt,x86_ir_sar):
			stmt.src_name = var_colors[stmt.src_name]
		elif isinstance(stmt,x86_ir_sal):
			stmt.src_name = var_colors[stmt.src_name]
		elif isinstance(stmt,x86_ir_cmp):
			if (stmt.left_name[0] == '$' or  stmt.left_name[0] == '%'):
				left = stmt.left_name
			else:
				left = var_colors[stmt.left_name]
			if (stmt.right_name[0] == '$' or  stmt.right_name[0] == '%'):
				right = stmt.right_name
			else:	
				right = var_colors[stmt.right_name]
			stmt.right_name = right
			stmt.left_name = left
		elif isinstance(stmt,x86_ir_movzbl):
			pass#stmt.right_name =  var_colors[stmt.right_name]
		elif isinstance(stmt,x86_ir_sete):
			pass #not sure if i can just pass here .... eax is being blocked and that is all i need
		elif isinstance(stmt,x86_ir_setne):
			pass #not sure if i can just pass here .... eax is being blocked and that is all i need
		elif isinstance(stmt,If):
			x86ir_assign_homes(stmt.tests[0][1].nodes)
			x86ir_assign_homes(stmt.else_.nodes)
		elif isinstance(stmt,While):
			x86ir_assign_homes(stmt.body.nodes)
		else:
			raise Exception("Home assignment is missing something:" + str(stmt))


			
def expl_ops(ast):
	global func_names
	if isinstance(ast,Module):
		return (Module(None,expl_ops(ast.node)))
	elif isinstance(ast,Stmt):
		return (Stmt([expl_ops(s) for s in ast.nodes]))
	elif isinstance(ast,Printnl):
		return Printnl([expl_ops(ast.nodes[0])],ast.dest)
	elif isinstance(ast,Discard):
		return Discard(expl_ops(ast.expr))
	elif isinstance(ast,Assign):
		#Assign([Subscript(Name('ls'), 'OP_ASSIGN', [Const(0)])], Const(42))
		if isinstance(ast.nodes[0],Subscript):
			return Assign([Subscript(expl_ops(ast.nodes[0].expr), 'OP_ASSIGN', [expl_ops(ast.nodes[0].subs[0])])], expl_ops(ast.expr))
		elif isinstance(ast.nodes[0],AssName):
		        return Assign([AssName(expl_ops(ast.nodes[0].name), 'OP_ASSIGN')], expl_ops(ast.expr))
		else:
			raise exception("Something was missed in the assign portion of expl_ops " + str(ast))
	elif isinstance(ast, Const):
		return InjectFrom('int', ast)
	elif isinstance(ast, Name):
		#We just assume Names are of type pyobj so we don't need to InjectFrom as we don't know what will be stored in this Name.
		if (ast.name == 'True'):
			return InjectFrom('bool',Const(1))
		elif (ast.name == 'False'):
			return InjectFrom('bool',Const(0))
		else:
			return ast#InjectFrom(type(ast.name).__name__, ast)
	elif isinstance(ast,CallFunc):
		if isinstance(ast.node,Name):
			if ast.node.name == 'input':
			      return  InjectFrom('int',ast) #this will return the input from input() as a pyobj with Tag 'int'
			else:
				'''
					e0(e1,: : :,en)
					=>
					let f = e0 in                           outside let
				     if is_class(f) then                               outerIfExp
					      let o = create_object(f) in                    firstInnerLet
					      if has_attr(f, '__init__') then                secondIFExp 
						   let ini = get_function(get_attr(f, '__init__')) in   secondInnerLet
						   let _ = ini(o, a1,: : :,an) in               thirdInnerLet
						   o 
					      else o      
				     else
				         if is_bound_method(f) then                              thirdIfExp
					        let bm = get_function(f) in                      boundLet
						let br = get_reciever(f) in                      boundLet2
						     CallFunc(bm, [br,a1,...,an]                       
                                                #get_function(f)(get_receiver(f), a1,: : :,an)
                                         else
                                            if is_unbound_method(f) then                        unboundIF
					          let ubm = get_function(f) in                  unboundLet
						       CallFunc(ubm,[])
					           get_function(f)(a1,: : :,an)
					    else
					        f(a1,: : :,an) # normal function call
				    
				'''
				f = Name(generator())
				ini = Name(generator())
				o = Name(generator())
				_ = Name(generator())
				bm = Name(generator())
				br = Name(generator())
				ubm = Name(generator())
				generateStringLabel('__init__')
				thirdInnerLet = Let(_,CallFunc(ini,[o] + [expl_ops(s) for s in ast.args], None, None), o)
				secondInnerLet = Let(ini,expl_ops(get_function(get_attr(f,'__init__'))),thirdInnerLet)
				secondIfExp = IfExp(expl_ops(has_attr(f,'__init__')),secondInnerLet,o)
				boundLet2 = Let(br,expl_ops(get_receiver(f)),CallFunc(bm, [br]+[expl_ops(s) for s in ast.args], None, None))
				boundLet = Let(bm,expl_ops(get_function(f)),boundLet2)
				unboundLet = Let(ubm,expl_ops(get_function(f)),CallFunc(ubm, [expl_ops(s) for s in ast.args], None, None))
				unboundIF = IfExp(is_unbound_method(f),unboundLet,CallFunc(ast.node, [expl_ops(s) for s in ast.args], None, None))
				thirdIfExp = IfExp(is_bound_method(f),boundLet,unboundIF)
				firstInnerLet = Let(o, expl_ops(create_object(f)),secondIfExp)
				outerIfExp = IfExp(expl_ops(is_class(f)),firstInnerLet,thirdIfExp)#CallFunc(ast.node, [expl_ops(s) for s in ast.args], None, None))
				outsideLet = Let(f,expl_ops(ast.node),outerIfExp)
				
				return  outsideLet
			
			        #return CallFunc(ast.node, [expl_ops(s) for s in ast.args], None, None)
		elif isinstance(ast.node,Lambda):
			args = ast.node.argnames
			body = ast.node.code
			return CallFunc(Lambda(ast.node.argnames, [], 0, Stmt([Return(expl_ops(body))])), [expl_ops(s) for s in ast.args], None, None)
		elif isinstance(ast.node,CallFunc):
			#return CallFunc(CallFunc(Name('f'), [Const(3)], None, None), [Const(4)], None, None)
			return CallFunc(CallFunc(ast.node.node, [expl_ops(s) for s in ast.node.args], None, None), [expl_ops(s) for s in ast.args], None, None)
		elif isinstance(ast.node,get_attr):
			f = Name(generator())
			return Let(f,expl_ops(ast.node),expl_ops(CallFunc(f, [expl_ops(s) for s in ast.args], None, None)))
		elif isinstance(ast.node,IfExp):
			f = Name(generator())
			return Let(f,expl_ops(ast.node),expl_ops(CallFunc(f, [expl_ops(s) for s in ast.args], None, None)))
	elif isinstance(ast,is_unbound_method):
		return is_unbound_method(expl_ops(ast.val))
	elif isinstance(ast,is_bound_method):
		return is_bound_method(expl_ops(ast.val))
	elif isinstance(ast,get_receiver):
		return InjectFrom('big',get_receiver(expl_ops(ast.o)))
	elif isinstance(ast,get_function):
		return InjectFrom('big',get_function(expl_ops(ast.o)))
	elif isinstance(ast,create_object):
		return InjectFrom('big',create_object(expl_ops(ast.c)))
	elif isinstance(ast,is_class):
		return is_class(expl_ops(ast.c))
	elif isinstance(ast,List):
		new_list = generator()
		listItems = []
		length = '$'+ str(len(ast.nodes))
		length = InjectFrom('int',Const(len(ast.nodes)))
		#new_list needs to be a pointer to a 'big'
		for i,s in list(enumerate(ast.nodes)):
                       #think here i might need something like newVar = generator then newvar = expl_ops(s) then in the last stmt have  a expl_ops(s)
			listItems[len(listItems):] = [SetSubScript(Name(new_list),InjectFrom('int',Const(i)),expl_ops(s))]
		newListNode = CreateList(length,new_list,listItems)
		
		#return InjectFrom('big',[expl_ops(s) for s in ast.nodes]) #this will make the 'big' into a pyobj
		#I think we can remove the InjectFrom here as long as we use make_list isntead of create_list										
		#return InjectFrom('big',newListNode) #this will make the 'big' into a pyobj
		return newListNode
	elif isinstance(ast,Dict):
		dictItems = []
		new_dict = generator()
		for i,s in list(enumerate(ast.items)):
			key =expl_ops(s[0])
			value = expl_ops(s[1])
			dictItems[len(dictItems):] = [SetSubScript(Name(new_dict),key,value)]
		newDictNode = CreateDict(new_dict,dictItems)
		return newDictNode #this will make the 'big' into a pyobj
	elif isinstance(ast, IfExp):
		'''
		let x1 = expl_ops(p) in
		  let Tx1 = GetTag(x1) in
		     if Tx1 == 'int' or Tx1 == 'bool'    #OUTERIF
			if x1                             #OUTERIFPARAT
			   expl_ops(ast.then)
			else
			   expl_ops(ast.else_)
		     else 
                         if is_true(x1)                  #OUTERELSEPART
			      expl_ops(ast.then)
		        else
		              expl_ops(ast.else_)

		'''
		#Make a Name Node that contais the variable we will store the x1 tag in 
		Tx1 = Name(generator())
		x1 = Name(generator())
		outerIfCond =Or([Compare(Tx1, [('==', 'int')]), Compare(Tx1, [('==', 'bool')])])
		outerIfPart  = IfExp(ProjectTo('int',x1),expl_ops(ast.then), expl_ops(ast.else_))
		outerElsePart = IfExp(is_true(x1),expl_ops(ast.then), expl_ops(ast.else_))
		outerIf = IfExp(outerIfCond,outerIfPart,outerElsePart)

		secondLet= Let(Tx1,GetTag(x1), outerIf)
		firstLet = Let(x1, expl_ops(ast.test), secondLet)		
		return firstLet


	elif isinstance(ast, If):
		#to fix the let part we will just do
		x1 = Name(generator())
		LetNode = Let(x1,expl_ops(ast.tests[0][0]),is_true(x1))
		return If([(LetNode,expl_ops(ast.tests[0][1]))], expl_ops(ast.else_))
	elif isinstance(ast,While):
		'''
		let x1 = expl_ops(p) in
		  let Tx1 = GetTag(x1) in
		     if Tx1 == 'int' or Tx1 == 'bool'    #OUTERIF
			while x1:                             #OUTERIFPARAT
			   expl_ops(ast.body)
		     else 
                         while is_true(x1)                  #OUTERELSEPART
			      expl_ops(ast.body)
		'''
		x1 = Name(generator())
		LetNode = Let(x1,expl_ops(ast.test),is_true(x1))
		return While(LetNode,expl_ops(ast.body), None)
		#Tx1 = Name(generator())
		#x1 = Name(generator())
		#outerIfCond =Or([Compare(Tx1, [('==', 'int')]), Compare(Tx1, [('==', 'bool')])])
		#outerIfPart  = While(ProjectTo('int',x1),expl_ops(ast.body), None)
		#outerElsePart = While(is_true(x1),expl_ops(ast.body), None)
		#outerIf = IfExp(outerIfCond,outerIfPart,outerElsePart)

		#secondLet = Let(Tx1,GetTag(x1), outerIf)
		#firstLet = Let(x1, expl_ops(ast.test), secondLet)
		#return firstLet	
	
	
	elif isinstance (ast, Add):
	
		'''
		let left = expl_ops(ast.left) in    
		    let right = expl_ops(ast.right) in     #RIGHT PART
		       let LeftTag = GetTag(left) in       #LEFT TAG PART
		          let RightTag = GetTag(right) in  #RIGHT TAG PART
			       If (LeftTag == 'int' or LeftTag == 'bool' and RightTag == 'int' or RightTag == 'bool')  IFPART
			                    InjectFrom('int',Add(ProjectTo('int',left),ProjectTo('int',right))              
				else
				    if (LeftTag == 'big' and RightTag == 'big')                                       INNERIF                           
                                            InjectFrom('big',CallFunc(Name('add'), [ProjectTo('big',left),ProjectTo('big',left)], None, None))
				     else
				         exit(-1)
		'''
		left = Name(generator())
		right = Name(generator())
		leftTag = Name(generator())
		rightTag = Name(generator())
	


		listCompare =And([Compare(leftTag, [('==', 'big')]), Compare(rightTag, [('==', 'big')])])
		listAdd =InjectFrom('big',addBig(ProjectTo('big',left),ProjectTo('big',right)))  #call add with bigobj then inject from big to pyobj



		leftTagChecks = Or([Compare(leftTag, [('==','int')]), Compare(leftTag, [('==', 'bool')])])
		rightTagChecks = Or([Compare(rightTag, [('==','int')]), Compare(rightTag, [('==','bool')])])

		innerIF = IfExp(listCompare,listAdd,ERROREXIT(-1))
		intBoolCompare = And([leftTagChecks, rightTagChecks])
		intBoolAdd = InjectFrom('int',Add([ProjectTo('int',left),ProjectTo('int',right)])) #return an object which is of type pyobj
		IFPART = IfExp(intBoolCompare,intBoolAdd,innerIF)		
	
		rightTagLet = Let(rightTag,GetTag(right),IFPART)
		leftTagLet = Let(leftTag,GetTag(left), rightTagLet)
		rightLet = Let(right,expl_ops(ast.right),leftTagLet)
		leftLet =Let(left,expl_ops(ast.left),rightLet)

		return leftLet

	elif isinstance(ast, And):
		'''
		let x1 = expl_ops(e1) in
		   let Tx1 = GetTag(x1) in
		    if Tx1 == 'int' or Tx1 == 'bool'    #OUTERIF
                            if x1 then                  #OUTERIFPART
		                 expl_ops(e2)
		            else
		                 x1
		   else                                #OUTERELSEPART
		             if  is_true(x1)
		                  expl_ops(e2)
		             else
		                 x1
				 
		'''
		Tx1 = Name(generator())
		x1 = Name(generator())
		outerElsePart = IfExp(is_true(x1),expl_ops(ast.nodes[1]),x1)
		outerIfPart = IfExp(ProjectTo('int',x1),expl_ops(ast.nodes[1]),x1)
		outerIfCond =Or([Compare(Tx1, [('==', 'int')]), Compare(Tx1, [('==', 'bool')])])
		outerIf = IfExp(outerIfCond, outerIfPart, outerElsePart)
		secondLet = Let(Tx1,GetTag(x1),outerIf)#CallFunc(Name('is_true'), [x1], None, None),IfPART)
		firstLet = Let(x1,expl_ops(ast.nodes[0]),secondLet)

		return firstLet

	
	elif isinstance(ast,Or):
	
		'''
		let x1 = expl_ops(e1) in
		   let Tx1 = GetTag(x1) in
		    if Tx1 == 'int' or Tx1 == 'bool'    #OUTERIF

                            if x1 then                   #OUTERIFPART
		                 x1
		            else
		              expl_ops(e2)

		   else                                #OUTERELSEPART
		             if  is_true(x1)
		                 x1
		             else
		                 expl_ops(e2)
				 
		'''
		Tx1 = Name(generator())
		x1 = Name(generator())
		outerElsePart = IfExp(is_true(x1),x1,expl_ops(ast.nodes[1]))
		outerIfPart = IfExp(ProjectTo('int',x1),x1,expl_ops(ast.nodes[1]))
		outerIfCond =Or([Compare(Tx1, [('==', 'int')]), Compare(Tx1, [('==', 'bool')])])
		outerIf = IfExp(outerIfCond, outerIfPart, outerElsePart)
		secondLet = Let(Tx1,GetTag(x1),outerIf)#CallFunc(Name('is_true'), [x1], None, None),IfPART)
		firstLet = Let(x1,expl_ops(ast.nodes[0]),secondLet)

		return firstLet


	elif isinstance(ast,UnarySub):
	
	        '''
		let x1 = expl_ops(ast.expr) in
		    let Tx1 = GetTag(x1) in
		       If (OrPart)
		           InjectFrom('int',UnarySub(ProjectTo('int',x1))
		       else
		           exit(-1)
		'''
		Tx1 = Name(generator())
		x1 = Name(generator())
	        OrPart = Or([Compare(Tx1, [('==', 'bool')]), Compare(Tx1, [('==', 'int')])])
		intBoolStmt = InjectFrom('int',UnarySub(ProjectTo('int',x1)))
		IfPart = IfExp(OrPart,intBoolStmt,ERROREXIT(-1))
		secondLet = Let(Tx1,GetTag(x1),IfPart)
		firstLet = Let(x1, expl_ops(ast.expr),secondLet)
		return firstLet
	
	elif isinstance(ast,Not):
		#'''
		#let x1 = expl_ops(ast.expr) in
		#     let Tx1 = GetTag(x1) in
		#         if Tx1 = 'int' or Tx1 = 'bool #outerIf
		#	     if ProjectTo('int',x1)                     #innerIf1
		#	         InjectFrom('bool',0)
		#	      else
		#	         InjectFrom('bool',1)
		#	  else   
		#             if is_true(x1)           innerIf2
		#		InjectFrom('bool',0)
		#	     else
		#		InjectFrom('bool',1)
		#'''
	
		
		Tx1 = Name(generator())
		x1 = Name(generator())
		
		innerIf1 = IfExp(ProjectTo('int',x1), InjectFrom('bool',Const(0)),InjectFrom('bool',Const(1)))
		innerIf2 =  IfExp(is_true(x1), InjectFrom('bool',Const(0)),InjectFrom('bool',Const(1)))
		orPart =  Or([Compare(Tx1, [('==', 'bool')]), Compare(Tx1, [('==', 'int')])])
		outerIf = IfExp(orPart,innerIf1,innerIf2)
		secondLet = Let(Tx1,GetTag(x1),outerIf)#CallFunc(Name('is_true'), [x1], None, None),IfPART)
		firstLet = Let(x1,expl_ops(ast.expr),secondLet)
		return firstLet

	elif isinstance(ast,Compare) and ast.ops[0][0] == 'is':
	
		return InjectFrom('bool',Compare(expl_ops(ast.expr), [('is', expl_ops(ast.ops[0][1]))]))
	elif isinstance(ast,Compare) and (ast.ops[0][0] == '==' or ast.ops[0][0] == '!='):	
		
		'''
		Algorithm Outline for Compare '==' and '!='
		let left = expl_ops(ast.expr) in    
		    let right = expl_ops(ast.ops[0][1]) in     #RIGHT PART
		       let LeftTag = GetTag(left) in       #LEFT TAG PART
		          let RightTag = GetTag(right) in  #RIGHT TAG PART
			       If (LeftTag == 'int' or LeftTag == 'bool' and RightTag == 'int' or RightTag == 'bool')  IFPART
			                    InjectFrom('bool',Compare(ProjectTo('int',left),[(ast.ops[0][0],ProjectTo('int',right))] )                         
				else
				       if (LeftTag == 'big' and RightTag == 'big')                                     bigIf
						if ast.ops[0][0] == '=='                                              bigIfEqualTypeCheck
						      InjFr('int'.CallFunc('equal',[left, right],None,None)
					        else
					              InjFr('int',CallFunc('not_equal',[left, right],None,None)
				       else
				            exit(-1)
		'''
		left = Name(generator())
		right = Name(generator())
		leftTag = Name(generator())
		rightTag = Name(generator())

		listDictCheck = And([Compare(leftTag, [('==', 'big')]), Compare(rightTag, [('==','big')])])
		if(ast.ops[0][0] == '=='):
		     bigIfEqualTypeCheck =  InjectFrom('bool',equalBig(ProjectTo('big',left),ProjectTo('big',right))) 
		else:
		     bigIfEqualTypeCheck =  InjectFrom('bool',nequalBig(ProjectTo('big',left),ProjectTo('big',right)))  
		bigIf  = IfExp(listDictCheck,bigIfEqualTypeCheck,ERROREXIT(-1))
		
		leftTagChecks = Or([Compare(leftTag, [('==', 'int')]), Compare(leftTag, [('==', 'bool')])])
		rightTagChecks = Or([Compare(rightTag, [('==', 'int')]), Compare(rightTag, [('==', 'bool')])])

		intBoolCheck = And([leftTagChecks, rightTagChecks])
		intBoolCompare = InjectFrom('bool',Compare(ProjectTo('int',left),[(ast.ops[0][0],ProjectTo('int',right))]))
		IFPART = IfExp(intBoolCheck,intBoolCompare,bigIf)

		rightTagLet = Let(rightTag,GetTag(right),IFPART)
		leftTagLet = Let(leftTag,GetTag(left), rightTagLet)
		rightLet = Let(right,expl_ops(ast.ops[0][1]),leftTagLet)
		leftLet =Let(left,expl_ops(ast.expr),rightLet)
		
		return leftLet
	elif isinstance(ast,Subscript) and (ast.flags == 'OP_APPLY'):
		#This is happening when y = x[1]
		#So we want to switch this for a GetSubScript(x,1) = GetSubScript(.expr,.subs[0]) node
		#e1(=.expr)[e2(=.subs[0])]
		'''
		let x1 = expl_ops(e1) in
		       let  Tx1 = GetTag(x1) in
		           if tagX1 == 'int' or tagX1 == 'bool'
				exit(-1)
			   else
			     let x2 = expl_ops(e2) in 
			     
			         GetSubScript(x1,x2)
				      
                '''
		
		x1 = Name(generator())
		x2 = Name(generator())
		Tx1 = Name(generator())
		errorCheck =  Or([Compare(Tx1, [('==', 'int')]), Compare(Tx1, [('==', 'bool')])])
		thirdLet = Let(x2,expl_ops(ast.subs[0]),GetSubScript(x1,x2))
		IfPart = IfExp(errorCheck,ERROREXIT(-1),thirdLet)
		secondLet = Let(Tx1, GetTag(x1),IfPart)
		firstLet = Let(x1,expl_ops(ast.expr),secondLet)
		return firstLet

	elif isinstance(ast,Subscript) and (ast.flags == 'OP_ASSIGN'):
		raise Exception("an OP_ASSIGN SubScript is being explicated this doesn't make sense")
	elif isinstance(ast,Function):
		#want to make this name = lambda args:  body
		func_names = func_names | set([ast.name])
		rhs =  Lambda(ast.argnames, [], 0, expl_ops(ast.code))
		if isinstance(ast.code,Stmt):
			pass
		else:
			raise Exception("the code in a function is not a stmt")
		return Assign([AssName(ast.name, 'OP_ASSIGN')], rhs)


	elif isinstance(ast,Lambda):
		args = ast.argnames
		body = ast.code
		return Lambda(ast.argnames, [], 0, Stmt([Return(expl_ops(ast.code))]))
	elif isinstance(ast,Return):
		return Return(expl_ops(ast.value))
	elif isinstance(ast,create_class):
		return InjectFrom('big',create_class(expl_ops(ast.bases)))
	elif isinstance(ast,set_attr):
		return set_attr(expl_ops(ast.c),ast.attr,expl_ops(ast.val))
	elif isinstance(ast,get_attr):
		
		return get_attr(expl_ops(ast.c),ast.attr)
	elif isinstance(ast,has_attr):
		return InjectFrom('int',has_attr(expl_ops(ast.o),ast.attr))
	else:
		return ast
		
def declassify(ast,cls):
	if isinstance(ast,Module):
		return (Module(None,declassify(ast.node,None)))
	elif isinstance(ast,Stmt):
		stmtList = []
		for x in  ast.nodes:
			stmtList = stmtList +  declassify(x,cls)
		return Stmt(stmtList)
	elif isinstance(ast,Printnl):
		return  [Printnl([declassify(ast.nodes[0],cls)],ast.dest)]
	elif isinstance(ast,Discard):
		return [Discard(declassify(ast.expr,cls))]
	elif isinstance(ast,Assign):
		aExpr = declassify(ast.expr,cls)
		if isinstance(ast.nodes[0],AssName):
			if cls == None:
			        return [Assign([AssName(ast.nodes[0].name, 'OP_ASSIGN')], aExpr)]
			else:
				return [set_attr(Name(cls),ast.nodes[0].name,aExpr)]
			        #return [Assign([AssAttr(Name(cls),lhs.name, 'OP_ASSIGN')], aExpr)]
		elif isinstance(ast.nodes[0],Subscript):
			if cls == None:
			        return [Assign([Subscript(declassify(ast.nodes[0].expr,cls), 'OP_ASSIGN', [declassify(ast.nodes[0].subs[0],cls)])], aExpr)]
			else:
				#this is wrong!!!!!!!!!!!!!!
				return [set_attr(Name(cls),ast.nodes[0].expr.name,aExpr)]
		elif isinstance(ast.nodes[0],AssAttr):
			return [set_attr(declassify(ast.nodes[0].expr,cls),ast.nodes[0].attrname,aExpr)]
			#this shouuld not be doing this we should be doing set_attr not Assign(set_attr)
			#return [Assign([declassify(lhs,cls)],aExpr)]
		'''	

		elif isinstance(ast.nodes[0],Subscript):
			sExpr = declassify(ast.nodes[0].subs[0])
			aExpr = declassify(ast.expr)
			usr_var_name = declassify(ast.nodes[0].expr.name)
			return [Assign([Subscript(Name(usr_var_name), 'OP_ASSIGN', [sExpr])], aExpr)]
		elif isinstance(ast.nodes[0],AssAttr):
			
		else:
			raise Exception("something is wrong assign.nodes[0] = " + str(ast.nodes[0]))
		'''
	elif isinstance(ast,Class):
		if not ast.name in usr_var_map:
			t = generator(ast.name)
			#t = generator()
			#####################################
			ncls = ast.name
		else:
			ncls = ast.name + "optimus_prime"
			t = generator(ncls)
		stmt = declassify(ast.code,t)
		#this doesn't make sense it shoudl be tmp= create_class(bases) then the stmt.nodes then the ncls = t so the first one should be ass(t to create_class
		#return [Class(t,[b.name for b in ast.bases], None, Discard(Const(0)))] + stmt.nodes + ([Assign([AssName(ncls, 'OP_ASSIGN')], Name(t))] if cls == None else [Assign([AssAttr(Name(cls),ncls,'OP_ASSIGN')], Name(t))])
		renamed_bases = []
		for base in ast.bases:
			renamed_bases = renamed_bases + [Name(base.name)]
		ast.bases = renamed_bases
		return [Assign([AssName(t, 'OP_ASSIGN')], create_class(List(ast.bases)))] + stmt.nodes + ([Assign([AssName(ncls, 'OP_ASSIGN')], Name(t))] if cls == None else [set_attr(Name(cls),ncls, Name(t))])

	elif isinstance(ast,If):
		testExpr = declassify(ast.tests[0][0],cls)
		thenExpr = declassify(ast.tests[0][1],cls)
		elseExpr = declassify(ast.else_,cls)
		return [If([(testExpr,thenExpr)],elseExpr)]
	elif isinstance(ast,While):
		testExpr = declassify(ast.test,cls)
		bodyExpr = declassify(ast.body,cls)
		return [While(testExpr, bodyExpr, None)]
	elif isinstance(ast,Return):
		return [Return(declassify(ast.value,cls))]

	elif isinstance (ast, Add):
		lExpr = declassify(ast.left,cls)
		rExpr = declassify(ast.right,cls)
		return  Add([lExpr,rExpr])
	elif isinstance (ast, UnarySub):
		aexpr = declassify(ast.expr,cls)
		return UnarySub(aexpr)
	elif isinstance(ast, Const):
		return ast
	elif isinstance(ast,Dict):
		renamedItems = []
		for pair in ast.items:
			newPair = [(declassify(pair[0],cls),declassify(pair[1],cls))]
			renamedItems = renamedItems + newPair
		return Dict(renamedItems)
	elif isinstance(ast,List):
		return List([declassify(s,cls) for s in ast.nodes])
	elif isinstance(ast, Name):
		# i think this should be get_attr(tmp,ast.name)
		if cls == None:
		      return ast  
		else:
		      var_colors[ast.name] = ""
		      return IfExp(has_attr(Name(cls),ast.name),get_attr(Name(cls),ast.name),Name(ast.name))
	elif isinstance(ast,CallFunc):
		if isinstance(ast.node,Name):
			if ast.node.name == 'input':
			     return ast
			else:
				
				declassified_args = [declassify(s,cls) for s in ast.args]
				ast.args = declassified_args
				ast.node = declassify(ast.node,cls)
				return ast
		elif isinstance(ast.node,Lambda):
			return ast
		elif isinstance(ast.node,CallFunc):
			return ast
		elif isinstance(ast.node,Getattr):
			ast.node = declassify(ast.node,cls)
			return ast
	elif isinstance(ast,IfExp):
		testExpr = declassify(ast.test,cls)
		thenExpr = declassify(ast.then,cls)
		elseExpr = declassify(ast.else_,cls)
		return IfExp(testExpr,thenExpr,elseExpr)

	elif isinstance(ast,Compare):
		lExpr = declassify(ast.expr,cls)
		rExpr = declassify(ast.ops[0][1],cls)
		return Compare(lExpr, [(ast.ops[0][0],rExpr)])
	elif isinstance(ast,Subscript):
		lExpr = declassify(ast.expr,cls)
		rExpr = declassify(ast.subs[0],cls)
		return Subscript(lExpr, ast.flags, [rExpr])
	elif isinstance(ast,AssAttr):
		return set_attr(declassify(ast.expr,cls),ast.attrname,ast.flags)#AssAttr(declassify(ast.expr,cls),ast.attrname,ast.flags)
	elif isinstance(ast,And):
		lExpr =  declassify(ast.nodes[0],cls)
		rExpr = declassify(ast.nodes[1],cls)
		return And([lExpr,rExpr])
	elif isinstance(ast,Or):
		lExpr =  declassify(ast.nodes[0],cls)
		rExpr = declassify(ast.nodes[1],cls)
		return Or([lExpr,rExpr])
	elif isinstance(ast,Not):
		aexpr = declassify(ast.expr,cls)
		return Not(aexpr)
	elif (ast in ('==','!=','is')):
		return ast
	elif isinstance(ast,Function):
		#ast.body = declassify(ast.code,cls)
		ast.code =declassify(ast.code,None)
		if cls == None:
		        return [ast]
		else:
			new_var = generator(ast.name)
			old_name = ast.name
			ast.name = new_var
		        return [ast] + [set_attr(Name(cls),old_name,Name(new_var))]
	elif isinstance(ast,Lambda):
		#print ast
		ast.code = declassify(ast.code,None)
		#print ast.code
		#most likely also need to handle the args
		return ast

	elif isinstance(ast,Getattr):
		#Getattr(Name('o'), 'x'))
		#I should just make these Name nodes that way everything is consistent
		return get_attr(declassify(ast.expr,cls),ast.attrname)#Getattr(declassify(ast.expr,cls),ast.attrname)
	else:
		raise Exception("Error "+ str(ast))



ast = compiler.parse(data)
#print ast
#print "original ast"
ast = declassify(ast,None)
#print "after declassify"
#print ast
#print usr_var_map
ast = uniquify_variables(ast)
#print "after uniquify"
#print ast
#print usr_var_map
ex_ast = expl_ops(ast)
#print "after expl"
#print ex_ast
#print usr_var_map
vars_to_heapify = to_heapify(ex_ast)
if debug_flag:
	print 'so we need to heapify.....'
	print vars_to_heapify

main_locals = get_locals(ex_ast.node.nodes)
mains_free = free_vars(ex_ast) - main_locals
if debug_flag:
	print "The explicit_ast:------------------"
	print ex_ast.node.nodes
	print "mains locals are = " +str(main_locals)
	print "-----------------------------------\n"

	
closed_ast = create_closures(ex_ast)

if debug_flag:
	print "******"
	print "this is the closed ast"
	print closed_ast
	print "******"
	print usr_var_map
	print "******"
if debug_flag:
	print "\nstarting the heapification analysis of main...\n"
	print "the locals for main are"
	print main_locals
	print "the free_vars for main are "
	print mains_free
	print "\n"
main_heapify_assigns = []
for var in main_locals:
	if var in vars_to_heapify:
		new_var = generator()
		new_assign = Assign([AssName(var, 'OP_ASSIGN')], CreateList(InjectFrom('int', Const(1)), new_var, [SetSubScript(Name(new_var), InjectFrom('int', Const(0)), InjectFrom('int', Const(0)))]))
		main_heapify_assigns = main_heapify_assigns + [new_assign]
if debug_flag:
	print '+++++++++++++++++++++++++++++++++++++++++++++++'

if debug_flag:
	print '$$$$$$$$$$$$$$$$$$$$$$$$printing the closed/heapified functions'
	for t_func in top_level_functions:
		print t_func.name
		print t_func
		print "\n"
new_main_stmts = main_heapify_assigns + closed_ast.node.nodes
closed_ast.node.nodes = new_main_stmts
if debug_flag:
	print "\n so the new main is"
	print closed_ast.node.nodes
	print vars_to_heapify
	print '---------------------- finished printing the closed/heapified functions'
	print vars_to_heapify


#now it is time for flattening
flat_ast = flatten_code(closed_ast,flat_stmts)
for t_func in top_level_functions:
	flat_stmts = []
	flat_code = flatten_code(t_func.code,flat_stmts)
	t_func.code = flat_code
#now we want to add the "main" function at the end of the top_level_functions

newFunction = Function(None, 'main', [] , [], 0, None, flat_ast.node.nodes)
top_level_functions = top_level_functions + [newFunction]
if debug_flag:
	for t_func in top_level_functions:
		print '-----------------------------'
		print t_func.name
		for s in t_func.code:
			print s
		print '-----------------------------'
	print usr_var_map
for t_func in top_level_functions:
	inputIR = []
	#move the free_vars off the_stack
	if t_func.defaults != []:
		free_var_list_name = t_func.defaults
		inputIR = inputIR + [x86_ir_move("8(%ebp)",free_var_list_name)]
	#add the move base_pointer to each input_params
	input_bp_index = 8
	for input_data in t_func.argnames:
		input_bp_index = input_bp_index + 4
		if input_data in usr_var_map:
			inputIR = inputIR + [x86_ir_move(str(input_bp_index) + "(%ebp)",usr_var_map[input_data])]
		else:
			inputIR = inputIR + [x86_ir_move(str(input_bp_index) + "(%ebp)",input_data)]

	t_func_IR = generate_x86_ir(t_func.code)
	t_func_IR = inputIR + t_func_IR
	t_func.code = t_func_IR
	if debug_flag:
		print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + t_func.name
		for s in t_func.code:
			print s
		print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"+ t_func.name
for t_func in top_level_functions:
	while (coloring(t_func.code,t_func.name)):
	     pass
	x86ir_assign_homes(t_func.code)	
x86ir_to_asm(top_level_functions)
if debug_flag:
	print "the usr_var_map was :",usr_var_map
	print "finished"



