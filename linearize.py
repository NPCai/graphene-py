import wrapper as w
import json

inFile = open("data/tgt/giant_news_tgt_all.txt", "r")

srcFile = open("data/tgt/plain/src_graphene.txt", "w")
tgtFile = open("data/tgt/plain/tgt_graphene.txt", "w")


for line in inFile:
	a = line.split("\t")
	extract = w.GrapheneExtract(json.loads(a[1].strip()))
	arr = extract.extractList()
	for tup in arr:
		if len(tup) > 25 and 
		srcFile.write(a[0].strip() + "\n")
		tgtFile.write(tup + "\n")

inFile.close()
srcFile.close()
tgtFile.close()