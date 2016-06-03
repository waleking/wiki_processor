#encoding=utf-8
import sys
from operator import itemgetter

reload(sys)
sys.setdefaultencoding('utf-8')

dWordFreq=dict()
total_freq=0
for line in open("../data/raw_words/total_raw_words.txt","r"):
    word,freq=line.strip().split("\t")
    freq=int(freq)
    total_freq=total_freq+freq
    dWordFreq[word]=freq


dOut=dict()
for word in dWordFreq:
    dOut[word]=float(dWordFreq[word])/total_freq

fWriter=open("../data/words/total_words.txt","w")
sortedWordFreq=sorted(dOut.items(),key=itemgetter(1),reverse=True)
for t in sortedWordFreq:
    word,score=t
    fWriter.write("%s\t%s\n" %(word,score))

fWriter.close()
