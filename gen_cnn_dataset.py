import wrapper as w
from multiprocessing import Process
import atexit
import time

NUM_FILES = 8 # Should also be equal to the number of cores for max efficency
workerList = [] # Worker processes

class Worker(Process): # Need multiple threads or else it takes forever
	def __init__(self, fileNum): # filNum is the id of the file to extract from
		super().__init__()
		self.fileNum = fileNum

	def run(self):
		count = 0
		src =  open("data/equals/all_news" + self.fileNum + ".txt", "r")
		tgt = open("data/equals/tgt/all_news_tgt" + self.fileNum + ".txt", "w")
		for sentence in src:
			ex = w.GrapheneExtract(sentence)
			ex = ex.linearize()
			tgt.write(ex + "\n")
			count += 1
			print("Process" + self.fileNum + "done " + str(count))
		src.close()
		tgt.close()

for i in range(2):
	worker = Worker(str(i))
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