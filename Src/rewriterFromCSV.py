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

	def isValid(self, f: dict, filters: dict) -> bool:
		status = True
		for key in filters:
			if f[key] != 1:
				status = False
		return status

	def readAndRewrite(self, flight_filters= {"WeatherDelay.none": 1}):
		"""
		"""
		line : str
		f : Flight
		try:
			with open(self.dataFile, 'r') as source:
				rewrite_global = None
				count = 0
				for line in source:
					print("line =",line)
					line = line.strip()
					if line != "" and line[0] != "#":
						print("striped line = ", line)
						f = Flight(line,self.vocabulary)
						##Do what you need with the rewriting vector here ...

						rewrite = f.rewrite()
						print("-----------------------------")
						print(f)
						print("Rewritten flight :", f.rewrite())
						print("-----------------------------")

						if rewrite_global == None:
							if self.isValid(rewrite, flight_filters):
								rewrite_global = rewrite

						else:
							for key in rewrite:
								if self.isValid(rewrite, flight_filters):
									rewrite_global[key] += rewrite[key]

						count+=1
				
				if rewrite_global != None:
					for key in rewrite_global:
						rewrite_global[key] = rewrite_global[key]/(count-1)
					
				print("Global flight atttribute sum : ", rewrite_global)





		except:
			raise Exception("Error while loading the dataFile %s"%(self.dataFile))



if __name__ == "__main__":
 	if len(sys.argv) < 3:
 		print("Usage: python rewriterFromCSV.py <vocfile> <dataFile>")
 	else:
 		if os.path.isfile(sys.argv[1]): 
 			voc : Vocabulary = Vocabulary(sys.argv[1])
	 		if os.path.isfile(sys.argv[2]): 
	 			rw : RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])
	 			rw.readAndRewrite({"WeatherDelay.none": 0})
	 		else:
	 			print(f"Data file {sys.argv[1]} not found")
	 	else:
	 		print("Voc file {sys.argv[2]} not found")
