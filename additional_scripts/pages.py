#encoding=utf-8

import sys
import networkx as nx
import os
import re

def listFiles(folder):
    files=os.listdir(folder)
    return [folder+"/"+f for f in files]


def extractCategoryNames(files):
    categoryNames=[]
    for filename in files:
        matchObj=re.match(r"../data/categories/(.*)_category_nodes.txt",filename)
        if matchObj:
            categoryName=matchObj.group(1).split("/")[-1]
            categoryNames.append(categoryName)
    return categoryNames


def loadCategories(filename):
    l=[]
    for line in open(filename,"r"):
        category=line.strip()
        l.append(category)
    return l


def loadGraph(filename):
    '''treat cat,page as target, source
    '''
    g=nx.DiGraph()
    for line in open(filename,"r"):
        source,target=line.strip().split("\t")
        g.add_edges_from([(source,target)])
    return g


def getPages(lCategories,g,topicName):
    pages=set()
    for category in lCategories:
        if g.has_node(category):
            neighbors=g.successors(category)
            for neighbor in neighbors:
                if(neighbor not in pages):
                    pages.add(neighbor)
    fOutName="../data/pages/"+topicName+"_pages.txt"
    fOut=open(fOutName,"w")
    for page in pages:
        fOut.write("%s\n" % page)
    fOut.close()
    print("Write to %s" % fOutName)


def process(g,categoryName):
    print("It's going to extract all the wiki article pages related to "+
              "%s" % categoryName)
    #get all category nodes from ../data/categories/[node]_category_nodes.txt
    fileCategory="../data/categories/%s_category_nodes.txt" % categoryName

    print("Read in %s " % fileCategory)
    lCategories=loadCategories(fileCategory)
    getPages(lCategories,g,categoryName)


if __name__=="__main__":
    if len(sys.argv) != 2:
        print("please input path")
        print("e.g. python pages.py [node='Military' | node ='All']")
        print("     Find out the wiki article pages related to a specific topic"
              +"such as Military, Baseball, Film and so on. node='All' means to"
              +" process all topics mentioned in ../data/categories/"
              +"[node]_category_nodes.txt")
    else:
        node=sys.argv[1]
        #load catToPageGraph.txt
        g=loadGraph("catToPageGraph.txt")

        if(node != "All"):
            categoryName=node
            process(g,categoryName)
        else:
            files=listFiles("../data/categories/")
            categoryNames=extractCategoryNames(files)
            for topicName in categoryNames:
                process(g,topicName)
