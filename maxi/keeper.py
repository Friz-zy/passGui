#!/usr/bin/env python2
# coding=utf-8 

import os
try:
	from keepass import kpdb
except:
	import json


class Keeper():
	def __init__(self, parent = None):
		try:
			self.db = kpdb.Database()
			self.isKdb = True
		except:
			self.isKdb = False
		self.urls = {}
		
	def load(self, file, password = ""):
		if os.path.exists(file):
			if self.isKdb:
				self.db = kpdb.Database(str(file), str(password))
				for entry in self.db.entries:
					self.urls[entry.url] = {entry.username:
						    [entry.password, entry.notes]}
			else:
				with open(file, "r") as f:
					self.urls = json.loads(f.read())
	
	def sync_entries(self):
		if self.isKdb:
			urls = {}
			for entry in self.db.entries:
				urls[entry.url] = {entry.username:
					    [entry.password, entry.notes]}
			# delete all entries than not in urls:pass
			for url in urls.keys():
				for name in urls[url].keys():
					try:
						if name not in self.urls[url].keys(): 
							self.db.remove_entry(name,url)
					except:
						self.db.remove_entry(name,url)
			# add all urls:pass that not in entries
			for url in self.urls.keys():
				for name in self.urls[url].keys():
					try:
						if name not in urls[url].keys(): 
							self.db.add_entry(
							  "Internet",
							  " on ".join((name, url)),
							  name,
							  self.urls[url][name][0],
							  url,
							  self.urls[url][name][1],
							  imageid=1,
							  append=True)
						else:
							self.db.update_entry(
							  " : ".join((url, name)),
							  name,
							  url,
							  new_title=None,
							  new_username=None,
							  new_password=self.urls[url][name][0],
							  new_url=None,
							  new_notes=self.urls[url][name][1])
					except:
						self.db.add_entry(
						  "Internet",
						  " on ".join((name, url)),
						  name,
						  self.urls[url][name][0],
						  url,
						  self.urls[url][name][1],
						  imageid=1,
						  append=True)
		else:
			for url in self.urls.keys():
				for name in self.urls[url].keys():
					self.urls[url][name][0] = "password"
	
	def save(self, file, password = ""):
		if file:
			if self.isKdb:
				if ".kdb" not in file: file += ".kdb"
				self.sync_entries()
				self.db.write(str(file), str(password))
			else:
				if ".json" not in file: file += ".json"
				self.sync_entries()
				with open(file, "w") as f:
					f.write(json.dumps(self.urls))