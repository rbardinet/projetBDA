#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
from vocabulary import *
from flight import Flight

class RewriterFromCSV(object):
	def __init__(self, voc : Vocabulary, df : str) :
		"""
		Translate a dataFile using a given vocabulary
		"""
		self.vocabulary : Vocabulary = voc
		self.dataFile : str = df


	def readAndRewrite(self):
		"""
		"""
		line : str
		f : Flight
		try:
			with open(self.dataFile, 'r') as source:
				for line in source:
					line = line.strip()
					if line != "" and line[0] != "#":
						f = Flight(line,self.vocabulary)
						##Do what you need with the rewriting vector here ...
						print("-----------------------------")
						print(f)
						print("Rewritten flight :",f.rewrite())
						print("-----------------------------")

		except:
			raise Exception("Error while loading the dataFile %s"%(self.dataFile))



if __name__ == "__main__":
 	if len(sys.argv)  < 3:
 		print("Usage: python rewriterFromCSV.py <vocfile> <dataFile>")
 	else:
 		if os.path.isfile(sys.argv[1]): 
 			voc : Vocabulary = Vocabulary(sys.argv[1])
	 		if os.path.isfile(sys.argv[2]): 
	 			rw : RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])
	 			rw.readAndRewrite()
	 		else:
	 			print(f"Data file {sys.argv[1]} not found")
	 	else:
	 		print("Voc file {sys.argv[2]} not found")
