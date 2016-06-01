#encoding=utf-8
import networkx as nx

def load(filename):
    '''treat cat,subCat as target, source
    '''
    g=nx.DiGraph()
    for line in open(filename,"r"):
        target,source=line.strip().split("\t")
        g.add_edges_from([(source,target)])
    return g

def getPersonlization(filename):
    personaliedVec=dict()
    for line in open(filename,"r"):
        cat,score=line.strip().split("\t")
        personaliedVec[cat]=float(score)
    return personaliedVec

g=load("taxonomyGraph.txt")
personalizedVec=getPersonlization("hub_score.txt")
missing = set(g) - set(personalizedVec)
for node in missing:
    personalizedVec[node]=0.0
pr = nx.pagerank(g, alpha=0.85,personalization=personalizedVec)

fWriter=open("pagerank_score.txt","w")
for cat in pr.keys():
    fWriter.write("%s\t%s\n" %(cat,pr[cat]))
fWriter.close()
