# Purpose: This program registers the Recurrence T1POST to Primary T1POST
# Author: Roshan Sundar

import os
import subprocess, sys

def movedown2():
    for _ in range(2):
        os.chdir(next(os.walk('.'))[1][0])
def Register(inpt, reference, out):
    cmd = "flirt -in " +inpt+ " -ref " +reference+ " -out " +out
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
F.yesfilters = ["AX", "T1", "+", "C", "nii"]
F.nofilters = ["Sag", "Cor"]

sheet = "Sheet_2"
patientList = ['Patient_Q', 'Patient_R', 'Patient_W', 'Patient_Z', 'Patient_AA', 'Patient_AE', 'Patient_AF', 'Patient_AG', 'Patient_AL', 'Patient_AM', 'Patient_AN', 'Patient_AQ', 'Patient_AR', 'Patient_AY']

for patient in patientList:
    patient_path = "/N/dc2/scratch/rosundar/STEM2019/NIFTI/MRI/"+sheet+"/"+patient+"/"

    # Create result directory
    outpath = patient_path + "Registered_Recurrence"
    os.mkdir(outpath)
    outpath += "/"+patient+"_recurrence_registeredToPrimary_T1POST"

    # Get Primary T1POST
    primary_path = patient_path + "Primary"
    os.chdir(primary_path)
    movedown2()
    primary_path = os.getcwd()+"/"

    F.filepath = primary_path
    primary_path += F.GetFilteredFiles()[0]

    # Get Recurrence T1POST
    recurrence_path = patient_path + "Recurrence"
    os.chdir(recurrence_path)
    movedown2()
    recurrence_path = os.getcwd()+"/"

    F.filepath = recurrence_path
    recurrence_path += F.GetFilteredFiles()[0]

    # Register Recurrence to primary
    Register(recurrence_path, primary_path, outpath)
