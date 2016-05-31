#encoding=utf-8
import networkx as nx

def load(filename):
    '''treat cat,subCat as target, source
        treat cat, page as target, source in catToPageGraph.txt
    '''
    g=nx.DiGraph()
    for line in open(filename,"r"):
        source,target=line.strip().split("\t")
        g.add_edges_from([("cat_"+source,"page_"+target)])
    return g

g=load("catToPageGraph.txt")
authoriescores,hubscores=nx.hits(g)
fWriter=open("hits_score.txt","w")
for page in hubscores:
    score=hubscores[page]
    page=page.split("cat_")[-1]
    fWriter.write("%s\t%s\n" % (page,score))
fWriter.close()
