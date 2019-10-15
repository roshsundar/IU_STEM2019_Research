# Purpose: This program will check the primary folder for each patient and
#          print the 6 series, or none if one doesnt exist
# Author: Roshan Sundar

import os
import findfile

sheet = "Sheet_2"
patient = "Patient_P"
home = "/N/dc2/scratch/rosundar/STEM2019/NIFTI/MRI/"+sheet+"/"+patient+"/Primary/"
os.chdir(home)
home += (next(os.walk('.'))[1][0])+"/"
os.chdir(home)
home += (next(os.walk('.'))[1][0])
os.chdir(home)

F = findfile.FindFile()
F.filepath = os.getcwd()

def ReturnFiles():
    filelist = F.GetFilteredFiles()
    if not filelist: #if list empty
        return "NONE"
    return filelist[0]

# Get T1W
F.yesfilters = ["AX", "T1", "nii"]
F.nofilters = ["+C", "-C", "+-C", "-+C", "FLAIR", "SPINE", "POST", "nsa"]
T1W = ReturnFiles()
print "T1W: "+T1W

# Get T2W
F.yesfilters = ["AX", "T2", "nii"]
F.nofilters = ["FLAIR", "nsa"]
T2W = ReturnFiles()
print "T2W: "+T2W

# Get ADC
F.yesfilters = ["AX","ADC", "nii"]
F.nofilters = ["nsa"]
ADC = ReturnFiles()
print "ADC: "+ADC

# Get FLAIR
F.yesfilters = ["AX", "FLAIR", "nii"]
F.nofilters = ["nsa"]
FLAIR = ReturnFiles()
print "FLAIR: "+FLAIR

# Get SW-mIP
F.yesfilters = ["SW","mIP","nii"]
F.nofilters = ["nsa"]
SW_mIP = ReturnFiles()
print "SW_mIP: "+SW_mIP

# Get T1POST
F.yesfilters = ["AX", "T1", "+", "C", "nii"]
F.nofilters = ["Sag", "Cor", "nsa"]
T1POST = ReturnFiles()
print "T1POST: "+T1POST
