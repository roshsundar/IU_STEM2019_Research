# Purpose: This program is meant to run on mpiuser (located on desktop as of now). Tars all cases input by SuitableCases.txt (output by GetPatientCases.py) & outputs to data.tar
# Author: Roshan Sundar
import os
import subprocess, sys
import shutil

datesList = [line.rstrip('\n') for line in open("SuitableCases.txt")]

savepath = "/home/mpiuser/Desktop/data.tar"
datapath = "/mnt/MIPLDATA/DATA/NeuroRepo_GBM/7777-00137/MRI/"
os.chdir(datapath)

cmd = "tar -cpf " + savepath + " " + " ".join(datesList)
print cmd

p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
while True:
    out = p.stderr.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()
