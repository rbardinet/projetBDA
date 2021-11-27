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
        #Returns True if the current line (in f) has an attribute(s) that matches the filters exactly
        status = True
        for key in filters:
            if f[key] != filters[key]:
                status = False
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

                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        # Do what you need with the rewriting vector here ...

                        rewrite = f.rewrite()


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
                    rewrite_global = Flight(firstline, self.vocabulary).rewrite()
                    count = 1

                for key in rewrite_global:
                    rewrite_global[key] = rewrite_global[key]/(count)

                return rewrite_global

        except:
            raise Exception("Error while loading the dataFile %s" %
                            (self.dataFile))


if __name__ == "__main__":

    def cover(v, R: dict) -> float:
        return R[list(v.keys())[0]]

    def dep(v, vprime, rw, R) -> float:
        Rv = rw.readAndRewrite(v)
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


    def getDistance(R,v,vprime):
        if v == vprime:
            return 0

        v_arr = v.split(".")
        vprime_arr = vprime.split(".")

        if v_arr[0] == vprime_arr[0] :

            #Same category so distance calculated numerically
            #We need to look for the distance
            categorykeys = []
            for key in R :
                if key.split(".")[0] == v_arr[0] :
                    categorykeys.append(key.split(".")[1])
            
            index_v = categorykeys.index(v_arr[1])
            index_vprime = categorykeys.index(vprime_arr[1])

            return abs(index_v - index_vprime)/(len(categorykeys)-1)
        
        else :
            #They are not the same category
            return 1
  

    def rateAtypical(R,v_key):
        #Rates the atypicality of a key within the flight database
        max = 0

        for key in R :

            tmpmin = min(getDistance(R,key,v_key),min(cover({key:-1},R),1-cover({v_key:-1},R)))

            if (tmpmin > max) :

                max = tmpmin
        
        return max


    def listAtypical(R):
        Atypical = {}

        for key in R :
            Atypical[key] = rateAtypical(R,key)
        
        return Atypical


    if len(sys.argv) < 3:
        print("Usage: python rewriterFromCSV.py <vocfile> <dataFile>")
    else:
        if os.path.isfile(sys.argv[1]):
            voc: Vocabulary = Vocabulary(sys.argv[1])
            if os.path.isfile(sys.argv[2]):

                if(len(sys.argv)>=4):

                    if(sys.argv[3]=="etape1"):
                        
                        rw: RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])      
                        R = rw.readAndRewrite()
                        print(R)

                    elif(sys.argv[3]=="etape2"):

                        rw: RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])

                        if(len(sys.argv)==5):
                            filters = dict(sys.argv[4])

                            R = rw.readAndRewrite(filters)

                        else :
                            R = rw.readAndRewrite()
                        print(R)

                    elif(sys.argv[3]=="etape3_Correlation"):

                        if len(sys.argv) == 6:
                            print("Selected filters = ", sys.argv[4])
                            print("Selected value = ", sys.argv[5])
                            filter = {}
                            filter[str(sys.argv[4])] = float(sys.argv[5])
                            print("filters =", filter)
                    
                            rw: RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])      
                            R = rw.readAndRewrite()

                            findCorelated(rw,R, filter)

                        elif len(sys.argv) == 4:
                            rw: RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])      
                            R = rw.readAndRewrite()

                            findCorelated(rw,R)

                    elif(sys.argv[3]=="etape3_Atypicality"):
                        rw: RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])      
                        R = rw.readAndRewrite()
                        print(listAtypical(R))
                
                else :
                    pass

            else:
                print(f"Data file {sys.argv[1]} not found")
        else:
            print("Voc file {sys.argv[2]} not found")
