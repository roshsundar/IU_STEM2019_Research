# Purpose: This progam takes txt file output by GetSuitableCases.py and picks the first case 
# for each patient out of it, and outputs new list into txt file
# Author: Roshan Sundar
import re

inpath = "/N/u/rosundar/Carbonate/S2_potential_cases"
outpath = "/N/u/rosundar/Carbonate/s2first_potential_cases.txt"

lineList = [line.rstrip('\n') for line in open(inpath)]

firstList = []
first = ""
for line in lineList:
    patient = "".join(re.findall("[a-zA-Z]+", line.split('-')[0][2:]))
    if patient != first:
        firstList.append(line)
        first = patient

f = open(outpath, "w+")
for first in firstList:
    print >> f, first
f.close()
