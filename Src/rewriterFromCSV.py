#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
from vocabulary import *
from flight import Flight


class RewriterFromCSV(object):

    def __init__(self, voc: Vocabulary, df: str):
        """
        Translate a dataFile using a given vocabulary
        """
        self.vocabulary: Vocabulary = voc
        self.dataFile: str = df

    def isValid(self, f: dict, filters: dict) -> bool:
        status = True
        for key in filters:
            # print("current key = ",key)
            # print("current row key value =", f[key])
            if f[key] != filters[key]:
                status = False
        # print("returned status = ",status)
        return status

    def readAndRewrite(self, flight_filters={"WeatherDelay.none": 1}):
        """
        """
        line: str
        f: Flight
        try:
            with open(self.dataFile, 'r') as source:
                rewrite_global = None
                count = 0
                hasValidated = False
                linecount = 0
                firstline = 0
                
                for line in source:


                    if(linecount==0):
                        firstline = line

                    # print("line =",line)
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        # print("striped line = ", line)
                        f = Flight(line, self.vocabulary)
                        # Do what you need with the rewriting vector here ...

                        rewrite = f.rewrite()
                        # print("-----------------------------")
                        # print(f)
                        # print("Rewritten flight :", f.rewrite())
                        # print("-----------------------------")


                        if self.isValid(rewrite, flight_filters):
                            hasValidated = True
                            if rewrite_global == None:
                                count += 1
                                rewrite_global = rewrite

                            else:
                                count += 1
                                for key in rewrite:
                                    rewrite_global[key] += rewrite[key]
                        
                if not hasValidated :
                    # print(" no attribute validated for filters : ",flight_filters)
                    rewrite_global = Flight(firstline, self.vocabulary).rewrite()
                    count = 1


                    # print("current rewrite_global = ",rewrite_global)

                for key in rewrite_global:
                    rewrite_global[key] = rewrite_global[key]/(count)

                # print("Global flight atttribute sum : ", rewrite_global)
                #print("count =",count)

                return rewrite_global

        except:
            raise Exception("Error while loading the dataFile %s" %
                            (self.dataFile))


if __name__ == "__main__":

    def cover(v, R: dict) -> float:
        #print("in cover, v = ",v," R= ",R)
        return R[list(v.keys())[0]]

    def dep(v, vprime, rw, R) -> float:
        Rv = rw.readAndRewrite(v)
        #print("Rv = ",Rv)
        coverR = cover(vprime, R)
        if coverR == 0:
            return 0
        else :
            res = cover(vprime, Rv)/cover(vprime, R)
            return res

    def assoc(v, vprime, rw, R):
        depres = dep(v, vprime, rw, R)

        if(depres <= 1):
            return 0
        else :
            return 1 - (1/depres)

    def findCorelated(rw,R,v=None):

        if v!=None :
            print("CORRELATING ",v.keys()," TO :")
            for key2 in R :

                print("==",key2)

                vprime={}
                vprime[key2]=1

                coef = assoc(v,vprime, rw, R)

                print("correlation = ",coef )

        else : 

            for key1 in R :
                print("CORRELATING ",key1," TO :")
                for key2 in R :

                    print("==",key2)

                    v = {}
                    v[key1]=1

                    vprime={}
                    vprime[key2]=1

                    coef = assoc(v,vprime, rw, R)

                    print("correlation = ",coef )

    if len(sys.argv) < 3:
        print("Usage: python rewriterFromCSV.py <vocfile> <dataFile>")
    else:
        if os.path.isfile(sys.argv[1]):
            voc: Vocabulary = Vocabulary(sys.argv[1])
            if os.path.isfile(sys.argv[2]):
                rw: RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])
                
                R = rw.readAndRewrite()

                print("R = ",R)

                if len(sys.argv) == 5:

                    print("Selected filters = ", sys.argv[3])
                    print("Selected value = ", sys.argv[4])

                    filter = {}
                    filter[str(sys.argv[3])] = float(sys.argv[4])

                    print("filters =", filter)
                    
                    findCorelated(rw,R, filter)
                
                else :
                    findCorelated(rw,R)

            else:
                print(f"Data file {sys.argv[1]} not found")
        else:
            print("Voc file {sys.argv[2]} not found")
