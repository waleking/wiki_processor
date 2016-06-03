#encoding=utf-8

import sys
import os
import re
import json
from operator import itemgetter

def getWords(filename):
    topicVec=dict()
    for line in open(filename,"r"):
        wikipage=json.loads(line.strip())
        docVec=wikipage["sparseVec"]
        for word in docVec:
            if(word not in topicVec):
                topicVec[word]=docVec[word]
            else:
                topicVec[word]=topicVec[word]+docVec[word]
    fOutName="../data/raw_words/total_raw_words.txt"
    fOut=open(fOutName,"w")
    #sort topicVec by word frequencies in descending order
    sortedTopicVec=sorted(topicVec.items(),key=itemgetter(1),reverse=True)
    for t in sortedTopicVec:
        word,freq=t
        fOut.write("%s\t%s\n" % (word,freq))
        #print(word+"\t"+str(freq))
    fOut.close()
    print("Write to %s" % fOutName)


if __name__=="__main__":
        reload(sys)
        sys.setdefaultencoding('utf-8')

        getWords("wiki.json")
