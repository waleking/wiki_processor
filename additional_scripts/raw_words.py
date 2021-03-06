#encoding=utf-8

import sys
import os
import re
import json
from operator import itemgetter

def listFiles(folder):
    files=os.listdir(folder)
    return [folder+"/"+f for f in files]


def extractCategoryNames(files):
    categoryNames=[]
    for filename in files:
        matchObj=re.match(r"../data/pages/(.*)_pages.txt",filename)
        if matchObj:
            categoryName=matchObj.group(1).split("/")[-1]
            categoryNames.append(categoryName)
    return categoryNames


def listFileChunks():
    '''to known the file chunks of wiki.json.*
    return a list like [wiki.json.aa, wiki.json.ab,...]
    '''
    chunks=[]
    files=listFiles(".")
    for filename in files:
        matchObj=re.match(r"./wiki.json.(.*)",filename)
        if(matchObj):
            chunks.append(matchObj.group())
    return chunks



def loadPages(filename):
    s=set()
    for line in open(filename,"r"):
        page=line.strip()
        s.add(page)
    return s


def loadJsons(filename):
    '''treat cat,page as target, source
    '''
    l=[]
    for line in open(filename,"r"):
        wikipage=json.loads(line.strip())
        l.append(wikipage)
    return l


def initTopicVec(topicvecFilename):
    if(os.path.isfile(topicvecFilename)==False):
        return dict()
    else:
        topicVec=dict()
        f=open(topicvecFilename,"r")
        for line in f.readlines():
            word,freq=line.strip().split("\t")
            topicVec[word]=int(freq)
        return topicVec


def getWords(sPages,wikijsons,topicName):
    topicvecFilename="../data/raw_words/"+topicName+"_raw_words.txt"
    topicVec=initTopicVec(topicvecFilename)
    for wikijson in wikijsons:
        title="_".join(wikijson["title"].split(" "))
        if(title in sPages):
            docVec=wikijson["sparseVec"]
            for word in docVec:
                if(word not in topicVec):
                    topicVec[word]=docVec[word]
                else:
                    topicVec[word]=topicVec[word]+docVec[word]
    fOutName=topicvecFilename
    fOut=open(fOutName,"w")
    #sort topicVec by word frequencies in descending order
    sortedTopicVec=sorted(topicVec.items(),key=itemgetter(1),reverse=True)
    for t in sortedTopicVec:
        word,freq=t
        fOut.write("%s\t%s\n" % (word,freq))
        #print(word+"\t"+str(freq))
    fOut.close()
    print("Write to %s" % fOutName)


def process(wikijsons,categoryName):
    print("It's going to extract all the wiki words related to "+
              "%s" % categoryName)
    #get all wiki words from ../data/pages/[node]_pages.txt
    fileCategory="../data/pages/%s_pages.txt" % categoryName

    print("Read in %s " % fileCategory)
    sPages=loadPages(fileCategory)
    getWords(sPages,wikijsons,categoryName)


def delRawWordsTxt(files):
    '''delete the existed ../data/raw_words/[node]_raw_words.txt
    '''
    for filename in files:
        filename="../data/raw_words/%s_raw_words.txt" % filename
        if(os.path.isfile(filename)):
            os.remove(filename)


if __name__=="__main__":
    if len(sys.argv) != 2:
        print("please input path")
        print("e.g. python raw_words.py [node='Military' | node ='All']")
        print("     Find out the words related to a specific topic "
              +"such as Military, Baseball, Film and so on. node='All' means to"
              +" process all topics mentioned in ../data/pages/"
              +"[node]_pages.txt")
    else:
        reload(sys)
        sys.setdefaultencoding('utf-8')

        node=sys.argv[1]
        chunks=listFileChunks()
        print(chunks)

        if(node != "All"):
            #clean ../data/raw_words/[node]_raw_words.txt
            categoryName=node
            delRawWordsTxt([node])
            #update ../data/raw_words/[node]_raw_words.txt
            for chunk in chunks:
                #load wiki.json.**
                wikijsons=loadJsons(chunk)
                process(wikijsons,categoryName)
        else:
            files=listFiles("../data/pages/")
            #clean ../data/raw_words/[node]_raw_words.txt
            categoryNames=extractCategoryNames(files)
            delRawWordsTxt(categoryNames)
            #update ../data/raw_words/[node]_raw_words.txt
            for chunk in chunks:
                #load wiki.json.**
                wikijsons=loadJsons(chunk)
                for topicName in categoryNames:
                    process(wikijsons,topicName)
