#wiki processor
##Additional Scripts
Run with the following order: compute_hits.py, compute_pagerank.py

#### runInBatch.sh
Run all the python scripts from successorNodes.py to finalWords.py in batch.
This will cost 47min7sec on 51 topics on server.
The final result is stored in data/final_words/.*_final_words.txt

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
To accelerate the processing speed, we process the dataset by chunk.
And this will cost 16m28.517s and 14 GB memory on server.

usage: python raw_words.py [node="Military" | node ="All"]
    node="All" means to process all topics mentioned in ../data/pages/[node]_pages.txt

input: wiki.json (with wiki article content and words in the json file), ../data/pages/[node]_pages.txt

output: ../data/raw_words/[node]_raw_words.txt

#### total_words.py
Find out the word frequencies of the whole wikipedia corpus. And the code is similar to raw_words.py
And this will cost 10m15.843s (one pass on 5738260 lines, 17GB file, which cost wc -l command 0m3.629s on server) and 50MB memory on server.

usage: python total_words.py

input: wiki.json

output: ../data/raw_words/total_raw_words.txt and ../data/words/total_words.txt (normalized to 1)

#### normalizeTotalWords.py
Normalize ../data/raw_words/total_raw_words.txt and get ../data/words/total_words.txt

#### chi2.py
Do feature selection by chi square method.

usage: python chi2.py [node="Military" | node ="All"]
    node="All" means to process all topics mentioned in ../data/pages/[node]_pages.txt

input: ../data/raw_words/total_raw_words.txt (word frequencies from all wiki articles content and words in the json file), ../data/raw_words/[node]_raw_words.txt

output: ../data/features/[node]_features.txt (word \t chi2 statistics) and ../data/words/[node]_words.txt (word \t score, score=normaliztion of inner production(freq, chi2 statistics))

#### finalWords.py
Get the final words that are highly correlated to the topic.

usage: python finalWords.py [node="Military" | node = "All"]
    node="All" means to process all topics mentioned in ../data/pages/[node]_pages.txt

input: compare ../data/words/[node]_words.txt > ../data/words/total_words.txt, also read ../data/raw_words/[node]_raw_words.txt

output: ../data/final_words/[node]_final_words.txt (word \t normalized freq)
