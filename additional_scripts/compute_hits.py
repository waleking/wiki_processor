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
hubscores,authoriescores=nx.hits(g)
fWriter=open("hub_score.txt","w")
for page in hubscores:
    score=hubscores[page]
    if("cat_" in page):
        page=page.split("cat_")[-1]
        fWriter.write("%s\t%s\n" % (page,score))
fWriter.close()

fWriter2=open("authority_score.txt","w")
for page in authoriescores:
    score=authoriescores[page]
    if("page_" in page):
        page=page.split("page_")[-1]
        fWriter2.write("%s\t%s\n" %(page,score))
fWriter2.close()
