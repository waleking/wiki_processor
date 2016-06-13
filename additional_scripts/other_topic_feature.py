#encoding=utf-8

import sys
import os
import re
import math
from operator import itemgetter


def loadWords(filename):
    '''{"football":25700,"TOTAL":sum(other words' freq)}
    '''
    d=dict()
    totalNum=0
    for line in open(filename,"r"):
        word,freq=line.strip().split("\t")
        freq=int(freq)
        totalNum=totalNum+freq
        d[word]=freq
        d["TOTAL"]=totalNum
    return d



def getFeatures(dAllWords,dAllTopicWords):
    '''Use Chi2 statistics to get the features
    '''
    dChi2=dict()
    totalInAll=dAllWords["TOTAL"]
    totalInAllTopics=dAllTopicWords["TOTAL"]
    n=totalInAllTopics+totalInAll
    for word in dAllWords:
        #
        # |             | candidate word t | other words |
        # | class c     | a                | b           |
        # | class not c | c                | d           |
        # n = a+b+c+d
        # chi2(t)=n*(ad-bc)^2/(a+c)(b+d)(a+b)(c+d)
        if(word!="TOTAL"):
            try:
                a=dAllWords[word]
                b=totalInAll-a
                c=dAllTopicWords[word]
                d=totalInAllTopics-c
                dChi2[word]=n*math.pow(a*d-b*c,2)/( (a+c)*(b+d)*(a+b)*(c+d)  )
            except Exception,e:
                print(word)
                print(e)

    otherFeatureFilename="../data/features/other_features.txt"

    fOut=open(otherFeatureFilename,"w")
    #sort dChi2 by chi2 statistics in descending order
    sortedChi2=sorted(dChi2.items(),key=itemgetter(1),reverse=True)
    for t in sortedChi2:
        word,chi2=t
        fOut.write("%s\t%s\n" % (word,chi2))
    fOut.close()
    print("Write to %s" % otherFeatureFilename)



def loadAllTopicWords(topicNames):
    d=dict()
    totalNum=0
    for topicName in topicNames:
        fileTopicRawWords="../data/raw_words/%s_raw_words.txt" % topicName
        for line in open(fileTopicRawWords,"r"):
            word,freq=line.strip().split("\t")
            freq=int(freq)
            totalNum=totalNum+freq
            if(word not in d):
                d[word]=freq
            else:
                d[word]=d[word]+freq
    d["TOTAL"]=totalNum
    return d


if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    allWordsFilename="../data/raw_words/total_raw_words.txt"
    dAllWords=loadWords(allWordsFilename)

    topicNames=[line.strip() for line in open("topicnames.txt") ]
    dAllTopicWords=loadAllTopicWords(topicNames)
    getFeatures(dAllWords,dAllTopicWords)
