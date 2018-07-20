import wrapper as w
import json

outFile = open("data/tgt/linear/test.txt", "w")

with open("data/tgt/giant_news0tgt0.txt", "r") as inFile:
	for line in inFile:
		serialized = json.loads(line[line.index("\t"):])
		ex = w.GrapheneExtract(serialized)
		linear = ex.linearize()
		if linear != "":
			outFile.write(line[:line.index("\t")] + "\t" + linear + "\n")

outFile.close()