# Purpose: register the primary 5 series to T1POST
# Author: Roshan Sundar

import os
import subprocess, sys

def movedown2():
    for _ in range(2):
        os.chdir(next(os.walk('.'))[1][0])
def Register(inpt, reference, out):
    cmd = "flirt -cost mutualinfo -in " +"'"+inpt+"'"+ " -ref " +reference+ " -out " +out
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

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

sheet = "Sheet_2"
patientList = ['Patient_Q', 'Patient_R', 'Patient_W', 'Patient_Z', 'Patient_AA', 'Patient_AE', 'Patient_AF', 'Patient_AG', 'Patient_AL', 'Patient_AM', 'Patient_AN', 'Patient_AQ', 'Patient_AR', 'Patient_AY']

for patient in patientList:
    patient_path = "/N/dc2/scratch/rosundar/STEM2019/NIFTI/MRI/"+sheet+"/"+patient+"/"

    # Create result directory
    outpath = patient_path + "Registered_Primary"
    os.mkdir(outpath)

    # Go to the Primary
    primary_path = patient_path + "Primary"
    os.chdir(primary_path)
    movedown2()
    primary_path = os.getcwd() + "/"
    F.filepath = primary_path

    # Get T1W
    F.yesfilters = ["AX", "T1", "nii"]
    F.nofilters = ["+C", "-C", "+-C", "-+C", "FLAIR", "SPINE", "POST", "nsa"]
    T1W = primary_path + F.GetFilteredFiles()[0]

    # Get T2W
    F.yesfilters = ["AX", "T2", "nii"]
    F.nofilters = ["FLAIR", "nsa"]
    T2W = primary_path + F.GetFilteredFiles()[0]

    # Get ADC
    F.yesfilters = ["AX","ADC", "nii"]
    F.nofilters = ["nsa"]
    ADC = primary_path + F.GetFilteredFiles()[0]

    # Get FLAIR
    F.yesfilters = ["AX", "FLAIR", "nii"]
    F.nofilters = ["nsa"]
    FLAIR = primary_path + F.GetFilteredFiles()[0]

    # Get SW-mIP
    F.yesfilters = ["SW","mIP","nii"]
    F.nofilters = ["nsa"]
    SW_mIP = primary_path + F.GetFilteredFiles()[0]

    # Get T1POST
    F.yesfilters = ["AX", "T1", "+", "C", "nii"]
    F.nofilters = ["Sag", "Cor", "nsa"]
    T1POST = primary_path + F.GetFilteredFiles()[0]

    seriesDict = {
        "T1W": T1W,
        "T2W": T2W,
        "ADC": ADC,
        "FLAIR": FLAIR,
        "SW_mIP": SW_mIP
    }

    print sheet + " " + patient
    for series in seriesDict:
        finoutpath = outpath + "/" + patient + "_primary_registered_" + series
        Register(seriesDict[series], T1POST, finoutpath)
