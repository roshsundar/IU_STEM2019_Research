# Purpose: Converts the dicom to nifti using dcm2niix
# Author: Roshan Sundar

import os
import subprocess, sys
import shutil

def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]

def movedown2():
    for _ in range(2):
        os.chdir(next(os.walk('.'))[1][0])

def Convert(outpath, inpath):
    cmd = r"dcm2niix -f %i_%f_%p_%z -z i -o " + outpath + " " + inpath
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    while True:
        out = p.stderr.read(1)
        if out == '' and p.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

Sheet = "Sheet_2"
patientList = ['Patient_Q', 'Patient_R', 'Patient_W', 'Patient_Z', 'Patient_AA', 'Patient_AE', 'Patient_AF', 'Patient_AG', 'Patient_AL', 'Patient_AM', 'Patient_AN', 'Patient_AQ', 'Patient_AR', 'Patient_AY']

for patient in patientList:
    inpath = "/N/dc2/scratch/rosundar/STEM2019/DICOM/MRI/"+Sheet+"/"+patient+"/"
    outpath = "/N/dc2/scratch/rosundar/STEM2019/NIFTI/MRI/"+Sheet+"/"+patient+"/" # This directory SHOULDNT EXIST, program will create it & copy folder struct from inpath

    shutil.copytree(inpath, outpath, ignore=ig_f)

    # Primary
    primary_inpath = inpath + "Primary"
    primary_outpath = outpath + "Primary"

    os.chdir(primary_inpath)
    movedown2()
    primary_inpath = os.getcwd()

    primary_outpath = primary_inpath.replace("DICOM", "NIFTI")

    Convert(primary_outpath, primary_inpath)

    # Recurrence
    recurrence_inpath = inpath + "Recurrence"
    recurrence_outpath = outpath + "Recurrence"

    os.chdir(recurrence_inpath)
    movedown2()
    recurrence_inpath = os.getcwd()

    recurrence_outpath = recurrence_inpath.replace("DICOM", "NIFTI")

    Convert(recurrence_outpath, recurrence_inpath)
