#encoding=utf-8

import sys
import os
import re
import math
from operator import itemgetter


def loadWords(filename):
    '''{"football":0.25700,...}
    '''
    d=dict()
    totalNum=0
    for line in open(filename,"r"):
        word,freq=line.strip().split("\t")
        d[word]=float(freq)
    return d



def getHighlyCorrelatedFeatures(dAllWords,dTopicWords,topicName,dFreq):
    '''output dFreq[word] if dTopicWords[word]>dAllWords[word]
    '''
    topicFinalFilename="../data/final_words/"+topicName+"_final_words.txt"
    fOut=open(topicFinalFilename,"w")
    dOut=dict()
    sumFreq=0
    for word in dTopicWords:
        if(dTopicWords[word]>dAllWords[word]):
            freq=dFreq[word]
            dOut[word]=freq
            sumFreq=sumFreq+freq

    sortedOut=sorted(dOut.items(),key=itemgetter(1),reverse=True)
    for t in sortedOut:
        word,score=t
        fOut.write("%s\t%s\n" %(word,float(score)/sumFreq))
    fOut.close()
    print("Write to %s" % topicFinalFilename)


def loadFreq(topicName):
    '''load ../data/raw_words/[node]_raw_words.txt which contains the frequency
    of words
    '''
    d=dict()
    for line in open("../data/raw_words/%s_raw_words.txt" % topicName, "r"):
        word,freq=line.strip().split("\t")
        d[word]=int(freq)
    return d


def process(dAllWords,topicName):
    fileTopicRawWords="../data/words/%s_words.txt" % topicName

    dTopicWords=loadWords(fileTopicRawWords)
    dFreq=loadFreq(topicName)
    getHighlyCorrelatedFeatures(dAllWords,dTopicWords,topicName,dFreq)



if __name__=="__main__":
    if len(sys.argv) != 2:
        print("please input path")
        print("e.g. python .py [node='Military' | node ='All']")
        print("     Get the final words that are highly correlated to the topic."
              +" Comapre ../data/words/[node]_words.txt and ../data/words/total_"
              +"words.txt."
              +" Generate final words in ../data/final_words/[node]_final_words."
              +"txt")
    else:
        reload(sys)
        sys.setdefaultencoding('utf-8')

        node=sys.argv[1]
        allWordsFilename="../data/words/total_words.txt"
        dAllWords=loadWords(allWordsFilename)

        if(node != "All"):
            topicName=node
            process(dAllWords,topicName)
        else:
            files=[f for f in os.listdir("../data/pages/")
                   if re.match(r"(.*)_pages.txt",f) ]
            categoryNames=[f.split("_pages.txt")[0] for f in files]
            for topicName in categoryNames:
                process(dAllWords,topicName)
