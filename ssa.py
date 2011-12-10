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



def makeSSA(funs):
	#'vars' is a keyword in python so i spellled with a z
	varz = {}
	for fun in funs:
		if printIR == True:
			print PrintVisitor3().preorder(fun)
		else:
			for node in fun.code.nodes:
				if isinstance(node,If):
					pass
				if isinstance(node,IntMoveInstr):
					#if 'tmp' not in node.lhs.name and 'list' not in node.lhs.name and 'letify' not in node.lhs.name:
					if '_' not in node.lhs.name:
						if node.lhs.name not in varz:
							varz[node.lhs.name] = 1
						else:
							varz[node.lhs.name] += 1
						node.lhs = Name(node.lhs.name + '@' + str(varz[node.lhs.name]))
					if isinstance(node.rhs[0],Name):
						#if 'tmp' not in node.rhs[0].name and 'list' not in node.rhs[0].name and 'letify' not in node.rhs[0].name:
							#print varz,node.rhs[0].name
						if '_' not in node.rhs[0].name:
							varName = node.rhs[0].name.split('@')[0]
							z = ''.join([varName,'@',str(varz[varName])])
							node.rhs = [Name(z)]
					#print '!!!',node.lhs,node.rhs
				if isinstance(node,Push):
					#print '!!!',node.arg
					if isinstance(node.arg,Name):
						name = node.arg.name
						if name in varz:
							node.arg.name = name+'@'+str(varz[name])
					
		#for node in fun.code.nodes:
		#	print node
	return funs
