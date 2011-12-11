from ir2 import *
from ir_x86_3 import *

def countStmt(stmt,varz):
	for node in stmt.nodes:
		varz = countNode(node,varz)
	return varz

def countNode(node,varz):
	if isinstance(node,If):
		varz = countNode(node.tests[0][0],varz)
		varz = countStmt(node.tests[0][1],varz)
		varz = countStmt(node.else_,varz)
	if isinstance(node,While):
		varz = countNode(node.test,varz)
		varz = countStmt(node.body,varz)
	if isinstance(node,IntMoveInstr):
		if node.lhs.name not in varz:
			varz[node.lhs.name] = 1
		else:
			varz[node.lhs.name] += 1
		if isinstance(node.rhs[0],Name):
			if node.rhs[0].name not in varz:
				varz[node.rhs[0].name] = 1
			else:
				varz[node.rhs[0].name] += 1
	if isinstance(node,Push):
		if isinstance(node.arg,Name):
			if node.arg.name not in varz:
				varz[node.arg.name] = 1
			else:
				varz[node.arg.name] += 1
	return varz

def varCount(funs):
	varz = {}
	for fun in funs:
		varz = countStmt(fun.code,varz)

	ofile = open('varz.txt','w')
	for var in varz:
		ofile.write(var+':'+str(varz[var])+'\n')
	ofile.close()
