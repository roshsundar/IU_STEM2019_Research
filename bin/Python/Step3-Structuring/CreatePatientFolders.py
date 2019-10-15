# Purpose: This program will read txt file for patient names. Create those folders in DICOM & create Primary/Recurrence subfolders
# Author: Roshan Sundar
import os

patients_path = "/N/u/rosundar/Carbonate/SuitablePatients"
patientList = [line.rstrip('\n') for line in open(patients_path)]

Sheet = "Sheet_2"
home_path = "/N/dc2/scratch/rosundar/STEM2019/DICOM/MRI/"+Sheet+"/"

for patient in patientList:
    os.mkdir(home_path+patient)
    os.mkdir(home_path+patient+"/Primary")
    os.mkdir(home_path+patient+"/Recurrence")
