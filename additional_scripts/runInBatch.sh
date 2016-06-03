# todo: we need to check this bash script
# mkdir if they don't exist 
mkdir data
mkdir data/categories
mkdir data/features
mkdir data/final_words
mkdir data/pages
mkdir data/raw_words
mkdir data/words

#input: topicnames.txt, rebuild_taxonomyGraph.txt, catToPageGraph.txt, wiki.json.*
python successorNodes.py
python pages.py
python raw_words.py

python total_words.py
python normalizeTotalWords.py
python chi2.py
python finalWords.py
#output: data/final_words/*_final_words.txt
