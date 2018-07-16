import requests
import re

URL = "http://localhost:8080/relationExtraction/text"


class GrapheneExtract(object):

	def __init__(self, span):
		payload = {
		 "text": span,
		 "doCoreference": "true", 
		 "isolateSentences": "false", 
		 "format": "FLAT_RESOLVED"
		 }
		r = requests.post(URL, json=payload)
		self.json = {i['id']:i for i in r.json()['extractions']}
		self.visited = {e:False for e in self.json} # (hash_id, bool is_used)

	def linearize(self):
		''' Depth-first search and append on the extracts '''
		# TODO: reorder simple and linked contexts based on position in the origional sentence
		self.strbuild = ""
		for hashId in self.json:
			self.visit(hashId)
		self.strbuild =  self.strbuild.replace(".", "")
		self.strbuild = re.sub(r"\s+", ' ', self.strbuild)
		return self.strbuild.strip()

	def visit(self, hashId):
		if self.visited[hashId]:
			return
		self.visited[hashId] = True
		self.strbuild += " ( " + self.json[hashId]['arg1'] + " <> " + self.json[hashId]['relation'] + " <> " + self.json[hashId]['arg2']
		for simple in self.json[hashId]['simpleContexts']:
			if simple['classification'] != "NOUN_BASED": # These tend to be duplicated in complex extractions
				if simple['classification'] == "TEMPORAL_BEFORE":
					if simple['text'].lower().startswith("after"): # remove after tokens
						simple['text'] = simple['text'][len("after"):]
				if simple['classification'] == "TEMPORAL_AFTER":
					if simple['text'].lower().startswith("before"):
							simple['text'] = simple['text'][len("before"):]
				self.strbuild += " " + simple['classification'] + " " + simple['text']
		for child in self.json[hashId]['linkedContexts']:
			if not self.visited[child['targetID']]:
				self.strbuild += " " + child['classification'] + " "
				self.visit(child['targetID'])
		self.strbuild += " ) "


