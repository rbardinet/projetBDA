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
                rw: RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])
                
                R = rw.readAndRewrite()

                #print("R = ",R)

                print("Atypical ratings for each key = ",listAtypical(R))

            else:
                print(f"Data file {sys.argv[1]} not found")
        else:
            print("Voc file {sys.argv[2]} not found")
