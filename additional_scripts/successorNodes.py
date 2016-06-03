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
    fWriter=open("../data/categories/"+node+"_category_nodes.txt","w")
    l=[node]
    while(len(l)>0):
        head=l.pop()
        fWriter.write("%s\n" % head)
        print(head)

        successors=g.successors(head)
        for node in successors:
            l.append(node)
    fWriter.close()


def loadTopicNames(filename):
    l=[]
    for line in open(filename,"r"):
        l.append(line.strip())
    return l


if __name__=="__main__":
    if len(sys.argv) != 2:
        print("please input node")
        print("e.g. python successorNodes.py Military")
        print("     It will find out successors in DAG given the node")
    else:
        #node="Military"
        node=sys.argv[1]
        if(node!="All"):
            g=buildGraph()
            getCategories(g,node)
        else:
            g=buildGraph()
            #todo load topicnames.txt
            topicNames=loadTopicNames("topicnames.txt")
            for topicName in topicNames:
                getCategories(g,topicName)
