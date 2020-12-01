import os
import sys
import subprocess
from os import listdir
from os.path import isfile, join
import shutil

# Path to the directory
mypath = r"C:\Users\Admin\Downloads\Celebdata\train"
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
outpath=r"C:\Users\Admin\Downloads\Celebdata\test"
# print(onlyfiles)
i=0
for folder in listdir(mypath):
	i=int(folder)
	folderpath=mypath+'\\'+folder
	# print(listdir(folderpath)[0])


	file=listdir(folderpath)[0]
	filepath=folderpath+'\\'+file
	# os.mkdir(outpath+'/'+str(i))
	output=outpath+'/'+str(i)+'/'+str(i+2)+'.jpg'
	print(output)

	# os.rename(filepath,output)
	shutil.move(filepath,output)
