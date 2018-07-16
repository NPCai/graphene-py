import spacy
import os
from pathlib import Path
import re
from multiprocessing import Process
import atexit
import time

class ParseWorker(Process):
	def __init__(self, file_list, numeral):
		super().__init__()
		self.nlp = spacy.load('en')
		self.file_list = file_list
		self.numeral = numeral
		self.count = 0

	def run(self):
		with open("data/giant_news" + self.numeral + ".txt", "w") as blob:
			for filename in self.file_list:
				self.count += 1
				contents = Path("./data/stories/" + filename).read_text()
				start = contents.find("(CNN) --")
				if start == -1:
					start = 0
				else:
					start += 8
				contents = contents[0 : contents.find("@highlight")].strip().replace("(CNN)", "")
				doc = self.nlp(contents)
				for sentence in list(doc.sents):
					if len(sentence.text) > 20:
						safe = re.sub(r'[^\x00-\x7f]',r'', sentence.text.replace("\n", "")) 
						blob.write(safe + "\n")
				print("Thread" + self.numeral + " filenum" + str(self.count))

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]

workerList = []

delegate = list(chunks(os.listdir("./data/stories/"), 15000)) # 10,000 stories per txt file

for i in range(len(delegate)):
	worker = ParseWorker(delegate[i], str(i))
	worker.daemon = True
	worker.start()

	workerList.append(worker)

def close_running_threads():
    for thread in workerList:
        thread.join()

atexit.register(close_running_threads)

print("registered")

while True:
    time.sleep(1)
