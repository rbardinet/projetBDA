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
			print("current key = ",key)
			print("current row key value =", f[key])
			if f[key] != filters[key]:
				status = False
		print("returned status = ",status)
		return status

	# terme correles
		# termes correles

	def cover(self,vprime,R:dict)-> float:
		count = 0
		for key in R:
			if key==vprime:
				count +=1
				val += R[key]
		return val/count
	
	def dep(self, v, vprime, R={}, Rv={})-> float:
		res = cover(vprime, Rv)/cover(vprime, R)
		return res

	def assoc(self, v, vprime):
		val = dep(v,vprime)
		if val <= 1 :
			return 0
		else:
			res = 1 - 1/val
			return res

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
								count+=1
								rewrite_global = rewrite

						else:
							if self.isValid(rewrite, flight_filters):
								count+=1
								for key in rewrite:
									rewrite_global[key] += rewrite[key]
				
				if rewrite_global != None:
					for key in rewrite_global:
						rewrite_global[key] = rewrite_global[key]/(count)
					
				print("Global flight atttribute sum : ", rewrite_global)
				print("count =",count)


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
	 			rw.readAndRewrite({"WeatherDelay.none": 1 , "Dest.big":1})
				

			
	 		else:
	 			print(f"Data file {sys.argv[1]} not found")
	 	else:
	 		print("Voc file {sys.argv[2]} not found")
