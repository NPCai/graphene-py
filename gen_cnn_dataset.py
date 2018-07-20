import wrapper as w
from multiprocessing import Process
import atexit
import time
from queue import Queue

''' 8 Processes, 24 threads per process = 192 threads '''

NUM_PROCESSES =  8
workerList = [] # Worker processes

class Worker(Process): # Need multiple threads or else it takes forever
	def __init__(self, queue): # filNum is the id of the file to extract from
		super().__init__()
		self.queue = queue
		self.outQueue = Queue()

	def run(self):
		with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
			executor.submit(loadUrl())

	def loadUrl():
		while not self.queue.empty():
			sentence = self.queue.get()
			ex = w.GrapheneExtract(sentence)
			self.outQueue.put(sentence.strip() + "\t" + str(ex.json) + "\n")

queues = [] # Use seperate queues to avoid waiting for locks
with open("data/all_news.txt", "r") as news:
	for line in news[::len(news) / NUM_PROCESSES]:
		queue = Queue()
		queue.put(line.strip())

print("Queue populated")

for i in range(NUM_PROCESSES):
	worker = Worker(queues[i])
	worker.daemon = True
	worker.start()
	workerList.append(worker)

def close_running_threads():
	for thread in workerList:
		thread.join()

atexit.register(close_running_threads)
print("All threads registered and working.")

while True:
	print(queue.qsize() " sentences remaining to be requested")
	time.sleep(2) # Print every two seconds