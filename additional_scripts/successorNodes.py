#encoding=utf-8
import networkx as nx
import sys

def buildGraph():
    g=nx.DiGraph()

    for line in open("rebuild_taxonomyGraph.txt","r"):
        cat,subCat=line.strip().split("\t")
        g.add_edges_from([(cat,subCat)])
    return g

def getCategories(g,node):
    fWriter=open(node+"_successor_nodes.txt","w")
    l=[node]
    while(len(l)>0):
        head=l.pop()
        fWriter.write("%s\n" % head)
        print(head)

        successors=g.successors(head)
        for node in successors:
            l.append(node)
    fWriter.close()



if __name__=="__main__":
    if len(sys.argv) != 2:
        print("please input node")
        print("e.g. python successorNodes.py Military")
        print("     It will find out successors in DAG given the node")
    else:
        #node="Military"
        node=sys.argv[1]
        g=buildGraph()
        getCategories(g,node)
