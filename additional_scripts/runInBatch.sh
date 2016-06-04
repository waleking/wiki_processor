# todo: we need to check this bash script
# mkdir if they don't exist 
mkdir ../data
mkdir ../data/categories
mkdir ../data/features
mkdir ../data/final_words
mkdir ../data/pages
mkdir ../data/raw_words
mkdir ../data/words

#input: topicnames.txt, taxonomyGraph.txt, catToPageGraph.txt, wiki.json.*
#All means all topics appeared in topicnames.txt should be processed
python rebuildTaxonomy.py 
python successorNodes.py All
python pages.py All
python raw_words.py All

python total_words.py
python normalizeTotalWords.py
python chi2.py All
python finalWords.py All
#output: data/final_words/*_final_words.txt
