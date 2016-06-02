#wiki processor
##Additional Scripts
Run with the following order: compute_hits.py, compute_pagerank.py

####compute_hits.py
Compute HITS score of categories according to the edges from categories to pages. And this HITS score are used as prior knowledge in page rank computing.

usage: python compute_hits.py

input: taxonomyGraph.txt (category->page)

output: hub_score.txt

####compute_pagerank.py
Compute page rank score of categories according to the edges from categories to their subcategories. The HITS score are used in personalized page rank algorithm.

usage: python compute_pagerank.py

input: catToPageGraph.txt (category->sub category)
    and hub_score.txt (used as the prior knowledge in personalized page rank algorithm)

output: pagerank_score.txt

####rebuildTaxonomy.py
Remove the edges that smaller pagerank-score nodes pointing to higer pagerank-score nodes. This step can make sure that the taxonomy graph is the directed acyclic graph. 

usage : python rebuildTaxonomy.py

input: pagerank_score.txt and taxonomyGraph.txt

output: rebuild_taxonomyGraph.txt

####successorNodes.py
Find out the successor nodes in a Directed Acyclic Graph (DAG) given a node.

usage: python successorNodes.py [node="Military"]

input: rebuild_taxonomyGraph.txt

output: ../data/category/[Military]_successor_nodes.txt

####pages.py
Find out the wiki article pages related to a specific topic such as Military, Baseball, Film and so on.  
And this will cost 6m28.876s and 20 GB memory on server.

usage: python pages.py [node="Military" | node ="All"]
    node="All" means to process all topics mentioned in ../data/categories/[node]_category_nodes.txt

input: catToPageGraph.txt ( with edges category to wiki article pages), ../data/categories/[node]_category_nodes.txt

output: ../data/pages/[node]_pages.txt

####raw_words.py
Find out the words related to a specific topic such as Military, Baseball, Film and so on.

usage: python raw_words.py [node="Military" | node ="All"]
    node="All" means to process all topics mentioned in ../data/pages/[node]_pages.txt

input: wiki.json (with wiki article content and words in the json file), ../data/pages/[node]_pages.txt

output: ../data/raw_words/[node]_raw_words.txt

####[todo] total_words.py, words.py
