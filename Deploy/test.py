import os
import sys
import subprocess
from os import listdir
from os.path import isfile, join

# Path to the directory
mypath = r"C:\Users\COMPUTER\Desktop\magiceye\SourceCode\face_recog\dataset_train\VanQuynh_ASPdotNET_HN"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)
outdir = os.path.join(mypath, 'output')

    # Creates the output dir if it doesn't exists
if not os.path.exists(outdir):
    os.makedirs(outdir)
else:
    print('Output dir already exists.')

for file in onlyfiles:
    name, ext = os.path.basename(file).split('.')
    print(name, ext)
    if ext == 'heic' or ext == 'HEIC':
        destination = os.path.join(outdir, name) + '.jpg'
        print(destination)
        source = os.path.join(mypath, file)
        print(source)
            # print ('converting   ',os.path.join(mypath, file))
        subprocess.call(['tifig', '-p', '-q', '100', source, destination])