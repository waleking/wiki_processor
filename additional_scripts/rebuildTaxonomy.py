#encoding=utf-8

dCatScore=dict()
for line in open("pagerank_score.txt","r"):
    cat,score=line.strip().split("\t")
    score=float(score)
    dCatScore[cat]=score
print("finished reading pagerank scores of categories")

fWriter=open("rebuild_taxonomyGraph.txt","w")
idx=0
for line in open("taxonomyGraph.txt","r"):
    cat,subCat=line.strip().split("\t")
    if(dCatScore[cat]>dCatScore[subCat]):
        fWriter.write("%s\t%s\n"% (cat,subCat))
    idx=idx+1
    if(idx%10000==0):
        print("processed %s lines in taxonomyGraph.txt" % idx)
fWriter.close()
print("finished reading pagerank scores of categories")
