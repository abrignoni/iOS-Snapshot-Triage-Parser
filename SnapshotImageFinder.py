import argparse
from argparse import RawTextHelpFormatter
from six.moves.configparser import RawConfigParser
from shutil import copy
import sys
import io
import os
import glob

parser = argparse.ArgumentParser(description="\
	iOS Snapshot KTX File Finder\
	\n\n Locate iOS snapshot KTX files."
, prog='SnapshotKtxFinder.py'
, formatter_class=RawTextHelpFormatter)
parser.add_argument('data_dir_to_analyze',help="Path to Data Directory.")

args = parser.parse_args()
data_dir = args.data_dir_to_analyze

foldername = ('FoundSnapshotImages')
pathfound = 0
path = os.getcwd()
outpath = path + "/" + foldername
count = 0
pathlog =[]	
os.makedirs(outpath)
print("\n--------------------------------------------------------------------------------------")
print("iOS Snapshot KTX file finder")
print("By: Alexis Brignoni | @AlexisBrignoni | abrignoni.com")
print("Source directory to be searched: " + data_dir)
print("\n--------------------------------------------------------------------------------------")
print("")
print('Searching for iOS Snapshot images.')
print('Please wait...')

for root, dirs, filenames in os.walk(data_dir):
		for f in filenames:
			if f.endswith('@3x.ktx'):
				pathfound = os.path.join(root, f)
				copy(pathfound, outpath)
				pathlog.insert(count, pathfound)
				#print(pathlog[count])
				count = count + 1
				
			
if pathfound == 0:
	print('')
	print('No snapshot ktx or png files available.')
else:
	print('')
	print('Snapshot ktx files moved to: '+ outpath)
	print('Snapshot ktx files moved total: '+ str(count))
	with open("SnapshotImageFinderPathsRreport.txt", "w") as output:
		output.write('iOS Snapshot KTX File Finder \n')
		output.write('By: Alexis Brignoni | @AlexisBrignoni | abrignoni.com \n')
		output.write('Snapshot KTX files moved to: '+ outpath+'\n')
		output.write('Snapshot ktx files moved total: '+ str(count)+'\n')
		output.write('\n')
		output.write('KTX file paths from source directory: \n')
		for item in pathlog:
			output.write('%s\n' % item)
	print('Copy log at: '+path+'\SnapshotImageFinderPathsRreport.txt')		
