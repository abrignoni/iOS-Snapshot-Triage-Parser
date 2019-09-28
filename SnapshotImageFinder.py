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
os.makedirs(outpath)
print('Searching for iOS Snapshot images.')
print('Please wait...')
for root, dirs, filenames in os.walk(data_dir):
		for f in filenames:
			if f.endswith('@3x.ktx'):
				pathfound = os.path.join(root, f)
				copy(pathfound, outpath)
				count = count + 1
			elif f.endswith('@2x.ktx'):
				pathfound = os.path.join(root, f)
				copy(pathfound, outpath)
				count = count + 1
			
if pathfound == 0:
	print("")
	print("No snapshot ktx or png files available.")
else:
	print("")
	print("Snapshot ktx files moved to: "+ outpath)
	print("Snapshot ktx files moved total: "+ str(count))
