from graphviz import Digraph
print("=======================CALLGRAPH==========================\n")
graph= []

with open("callTree.txt", "r") as fp:
        graph =fp.read().splitlines()

edges=[]
for line in graph:
    edges.append(line.split("->"))

dot = Digraph(comment='Call graph tree')
for i in edges:
    if(i[1] != '-1'):
        dot.edge(i[0],i[1])
print(dot.source)
dot.render('seqTree1')
