#encoding=utf-8
import networkx

def load(lines):
    '''treat cat,subCat as target, source
        treat cat, page as target, source in catToPageGraph.txt
    '''
    g=nx.DiGraph()
    for line in lines:
        source,target=line.strip().split(" ")
        g.add_edges_from([("cat_"+source,"page_"+target)])
        return g

load("catToPageGraph.txt")
