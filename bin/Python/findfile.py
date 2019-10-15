# Purpose: This program is a class that is able to parse files in a directory with filters
# Author: Roshan Sundar


import os

class FindFile():
    def __init__(self):
        self.filepath = ""
        self.yesfilters = []
        self.nofilters = []
    def GetFilteredFiles(self):
        candidates = []
        os.chdir(self.filepath)
        files = os.listdir(os.getcwd())
        for f in files:
            if all(x in f for x in self.yesfilters) and not any(x in f for x in self.nofilters): # if all filters in file and none of the nofilters 
                candidates.append(f)
        return candidates
    def GetSpecificFiles(self, files):
        print files
        indexes = []
        print "enter indexes of what you want, use comma to separate"
        indexes = raw_input().split(',')
        indexes = map(int, indexes)

        specificfiles = []
        for i in indexes:
            specificfiles.append(files[i])
        return specificfiles
    def GetAbsPath(self, files):
        paths = []
        for f in files:
            paths.append(os.path.abspath(f))
        return paths
