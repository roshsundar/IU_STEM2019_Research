# Purpose: This program is meant to run on mpiuser (located on desktop as of now). Finds the cases that have all 6 series & outputs to textfile cases.txt
# Author: Roshan Sundar
import os
import re

origdir = os.getcwd()

class FindFile():
    def __init__(self):
        self.filepath = ""
        self.yesfilters = []
        self.nofilters = []
    def GetFilteredFiles(self):
        candidates = []
        os.chdir(self.filepath)
        files = os.listdir(os.getcwd())
        files = map(str.strip, files)

        for f in files:
            if all(x in f for x in self.yesfilters):
                if not any(x in f for x in self.nofilters): # if all filters in file and none of the nofilters
                            candidates.append(f)

        return candidates

F = FindFile()
goodCases = []


home = "/mnt/MIPLDATA/DATA/NeuroRepo_GBM/7777-00137/MRI/"
os.chdir(home)
dates = os.listdir(os.getcwd())
#dates=['20151203'] #trouble shoot for individual date
for date in dates:
    os.chdir(home+date)
    cases = os.listdir(os.getcwd())
    cases = [c for c in cases if "S2" in c]
    for case in cases:
        os.chdir(home+date)
        os.chdir(case)
        os.chdir(next(os.walk('.'))[1][0])

        F.filepath = os.getcwd()
        
        isGood = True

        #T1W check
        F.yesfilters = ["AX", "T1"]
        F.nofilters = ["+C", "-C", "+-C", "-+C", "FLAIR", "SPINE", "POST"]
        if not F.GetFilteredFiles():
            isGood = False
  
        #T2W check
        F.yesfilters = ["AX", "T2"]
        F.nofilters = ["FLAIR"]
        if not F.GetFilteredFiles():
            isGood = False
        
        #ADC check
        F.yesfilters = ["AX","ADC"]
        F.nofilters = ["leedle"]
        if not F.GetFilteredFiles():
            isGood = False
        
        #FLAIR check
        F.yesfilters = ["AX", "FLAIR"]
        F.nofilters = ["leedle"]
        if not F.GetFilteredFiles():
            isGood = False
        
        #SW-mIP check
        F.yesfilters = ["SW","mIP"]
        F.nofilters = ["leedle"]
        if not F.GetFilteredFiles():
            isGood = False
        
        #T1POST check
        F.yesfilters = ["AX", "T1", "+", "C"]
        F.nofilters = ["Sag", "Cor"]
        if not F.GetFilteredFiles():
            isGood = False

        if isGood:
            goodCases.append(case)

convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
goodCases = sorted(goodCases, key = alphanum_key)

with open('/home/mpiuser/Desktop/cases.txt', 'w+') as f:
    for case in goodCases:
        print >> f, case
    f.close()

os.chdir(origdir)
