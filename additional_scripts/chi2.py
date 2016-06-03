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



def getFeatures(dAllWords,dTopicWords,topicName):
    '''Use Chi2 statistics to get the features
    '''
    dChi2=dict()
    totalInTopic=dTopicWords["TOTAL"]
    totalInAll=dAllWords["TOTAL"]
    n=totalInTopic+totalInAll
    allChi2score=0.0
    for word in dTopicWords:
        #
        # |             | candidate word t | other words |
        # | class c     | a                | b           |
        # | class not c | c                | d           |
        # n = a+b+c+d
        # chi2(t)=n*(ad-bc)^2/(a+c)(b+d)(a+b)(c+d)
        try:
            a=dTopicWords[word]
            b=totalInTopic-a
            c=dAllWords[word]
            d=totalInAll-c
            dChi2[word]=n*math.pow(a*d-b*c,2)/( (a+c)*(b+d)*(a+b)*(c+d)  )
            allChi2score=allChi2score+dChi2[word]
        except Exception,e:
            print(word)
            print(e)

    topicFeatureFilename="../data/features/"+topicName+"_features.txt"

    fOut=open(topicFeatureFilename,"w")
    #sort dChi2 by chi2 statistics in descending order
    sortedChi2=sorted(dChi2.items(),key=itemgetter(1),reverse=True)
    for t in sortedChi2:
        word,chi2=t
        fOut.write("%s\t%s\n" % (word,chi2))
    fOut.close()
    print("Write to %s" % topicFeatureFilename)

    #also output the words with chi2 statistics>500
    wordFilename="../data/words/"+topicName+"_words.txt"
    fOutWord=open(wordFilename,"w")
    #dOutWord=inner production(dChi2,dTopicWords)
    dOutWord=dict()
    #todo only consider the words with chi2 statistics > 500
    for word in  dChi2:
        dOutWord[word]=dTopicWords[word]*dChi2[word]/allChi2score
    sortedOutWord=sorted(dOutWord.items(),key=itemgetter(1),reverse=True)
    for t in sortedOutWord:
        word,score=t
        fOutWord.write("%s\t%s\n" % (word,score) )
    fOutWord.close()
    print("Write to %s" % wordFilename)


def process(dAllWords,topicName):
    print("It's going to extract all the wiki words related to "+
              "%s" % topicName)
    fileTopicRawWords="../data/raw_words/%s_raw_words.txt" % topicName

    print("Read in %s " % fileTopicRawWords)
    dTopicWords=loadWords(fileTopicRawWords)
    getFeatures(dAllWords,dTopicWords,topicName)



if __name__=="__main__":
    if len(sys.argv) != 2:
        print("please input path")
        print("e.g. python chi2.py [node='Military' | node ='All']")
        print("     Find out the features correlated to a specific topic "
              +"such as Military, Baseball, Film and so on. node='All' means to"
              +" compare all words in ../data/raw_words/[node]_raw_words.txt with "
              +"../data/raw_words/total_raw_words.txt")
    else:
        reload(sys)
        sys.setdefaultencoding('utf-8')

        node=sys.argv[1]
        allWordsFilename="../data/raw_words/total_raw_words.txt"
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
