import gdb
import re
import os
import sys
import copy

filename = ""
temp_file = []
def processInput():
	global filename, temp_file
	filename = input("Enter The File Name : ")
	f = open(filename,'r')
	lines = f.readlines()
	temp_file = copy.deepcopy(lines)
	f.close()
	if("return" not in lines[-2]):
		lines = lines[:len(lines)-1] + ["\treturn 0;\n"] + lines[len(lines)-1:]
		with open(filename, 'w') as file1:
			file1.writelines(lines)
		file1.close()
	print(lines)
	os.system('gcc -g ' +filename)
	
		
#process the Input to generate a Executable file 	
processInput()
def revertChanges(filename):
	with open(filename, 'w') as file1:
			file1.writelines(temp_file)
	file1.close()
def print_it(x):
	for i in x:
		print(i)
def loadtxt(filename):
    "Load text file into a string. I let FILE exceptions to pass."
    f = open(filename)
    txt = ''.join(f.readlines())
    f.close()
    return txt

def getLineNumbers(filename):
	
	# regex group1, name group2, arguments group3
	rproc = r"((?<=[\s:~])(\w+)\s*\(([\w\s,<>\[\].=&':/*]*?)\)\s*(const)?\s*(?={))"
	code = loadtxt(filename)
	cppwords = ['if', 'while', 'do', 'for', 'switch']
	procs = [(i.group(2), i.group(3)) for i in re.finditer(rproc, code) \
	if i.group(2) not in cppwords]
	
	temp = []
	for i in procs:
		temp.append(i[0] + '(' + i[1] + ')')
		print (i[0] + '(' + i[1] + ')')
	
	print(temp)
	temp1 = []
	f = open(filename)
	c = 0
	for line in f:
		c = c+1
		for i in temp:
			if(i in line and line[-2] != ';'):
				temp1.append([i,c])
			
	
	temp1.append(["final",c-1])
	f.close()
	return temp1

lineNo = getLineNumbers(filename)

def getFuncName(f):
	temp = f[3 : f.index(')')+1]
	return temp
	

		
#-------------------------------------------------------------------------------------

gdb.execute('file a.out')

breakPoints = []
for i in lineNo:
	breakPoints.append(i[1])

rb = gdb.Breakpoint(str(breakPoints[-1]), type = gdb.BP_BREAKPOINT)
for i in range(len(breakPoints) -1):
	gdb.Breakpoint(str(breakPoints[i]), type = gdb.BP_BREAKPOINT)
temp = []
gdb.execute('r',to_string = True)
max1 = 0
while(rb.hit_count == 0):
	gdb.execute('c',to_string = True)
	o = gdb.execute('bt',to_string = True)
	temp.append([o])
	#print(o)

functions_called = []
relArr = []    
for i in temp:
	for k in i:
		temp1 = k.split('\n')
		parent = temp1[1]
		child = temp1[0]
		if("main" not in parent and len(parent) != 0):
			parent = parent[parent.index("in") + 3 : parent.index(')') +1]
		elif("main" in parent and len(parent) != 0):
			parent = "main ()"
		else:
			parent = "root"
		if("main" not in child and len(child) != 0):
			child = child[child.index("#") + 4 : child.index(')') +1]
		elif("main" in child and len(child) != 0):
			child = "main ()"
		#print(parent,"|" ,child)
		relArr.append([parent,child])
		if(child not in functions_called):
			functions_called.append(child)
	print(" --------------- ")

print("===================== FUNCTIONS CALLED =================\n\n")
print_it(functions_called)

callSeq = []

for i in functions_called:
	callSeq.append([i,[]])
print("======================= RELATIONSHIP ARRAY =============\n\n")
print(" PARENT  , CHILD ")
print_it(relArr)

print("======================== INIT CALL SEQ =================\n\n")
print_it(callSeq)


for i in relArr:
	curr_p = i[0]
	curr_c = i[1]
	for j in callSeq:
		if(curr_p == j[0]):
			j[1].append(curr_c)
#removing duplicacy
for i in callSeq:
	if(i[0] != "main"):
		if(len(i[1]) != 0):
			i[1] = set(i[1])
		else:
			i[1] = set([-1])

func= []

with open("funcalls.txt", "r") as fp:
    	func =fp.read().splitlines()

edges=[]
for line in func:
    edges.append(line.split("->"))
print(edges)
print("========================== ADDING STD CALLS=====================\n\n")
for i in callSeq:
	for j in edges:
		if j[0] in i[0]:
			if j[1] not in i[1]:
				i[1].add(j[1])
					
print("========================== OUTPUT=====================\n\n")
print_it(callSeq)

print(" =============== BreakPoints SET ============= \n\n")
print_it(lineNo)
o = gdb.execute("info breakpoints", to_string = True)
print(o)
revertChanges(filename)
gdb.execute('c',to_string = True)

graph =[]
for i in callSeq:
    for j in i[1]:
        graph.append([i[0],str(j)])
        #print(i[0]+"->"+str(j))

fp = open('callTree.txt','w')
for i in graph:
    fp.write(i[0]+'->'+i[1]+'\n')
fp.close()

gdb.execute('quit')

