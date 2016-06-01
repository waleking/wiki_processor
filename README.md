#wiki processor
##Additional Scripts
Run with the following order: compute_hits.py, compute_pagerank.py

####compute_hits.py
usage: python compute_hits.py
input: taxonomyGraph.txt (category->page)
output: hub_score.txt

####compute_pagerank.py
usage: python compute_pagerank.py
input: catToPageGraph.txt (category->sub category)
    and hub_score.txt (used as the prior knowledge in personalized page rank algorithm)
output: pagerank_score.txt

