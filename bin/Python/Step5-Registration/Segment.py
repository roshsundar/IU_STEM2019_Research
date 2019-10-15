# Purpose: Segments T1POST for GM WM 
# Author: Roshan Sundar

import findfile
import os
import subprocess, sys

def movedown2():
    for _ in range(2):
        os.chdir(next(os.walk('.'))[1][0])

def RunCMD(cmd):
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()
def SkullStrip(inpath, outpath, name):
    cmd = "bet " + inpath + " " + outpath+name
    RunCMD(cmd)
def Segment(inpath, outpath, outname):
    cmd = "fast -o " + outpath+outname + " " + inpath
    RunCMD(cmd)

F = findfile.FindFile()

sheet = "Sheet_2"
patientList = ["Patient_F", "Patient_K", "Patient_L", "Patient_N", "Patient_O", "Patient_P"]

for patient in patientList:
    patient_path = "/N/dc2/scratch/rosundar/STEM2019/NIFTI/MRI/"+sheet+"/"+patient+"/"

    # Create result directory
    outpath = patient_path + "Segmented/"
    os.mkdir(outpath)

    # Go to the Primary
    primary_path = patient_path + "Primary"
    os.chdir(primary_path)
    movedown2()
    primary_path = os.getcwd() + "/"
    F.filepath = primary_path

    # Get T1POST
    F.yesfilters = ["AX", "T1", "+", "C", "nii"]
    F.nofilters = ["Sag", "Cor", "nsa"]
    T1POST = primary_path + F.GetFilteredFiles()[0]

    # Skull Strip
    name = patient + "_stripped"
    SkullStrip(T1POST, outpath, name)

    # Segment
    inputpath = outpath+name
    name = patient+"_segmented"
    Segment(inputpath, outpath, name)
