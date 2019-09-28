import datetime
import argparse
from argparse import RawTextHelpFormatter
from six.moves.configparser import RawConfigParser
import sys
import ccl_bplist
import plistlib
import io
import os
import glob
import sqlite3
from shutil import copy
from time import process_time

parser = argparse.ArgumentParser(description="\
	iOS Snapshot KTX Traige Parser\
	\n\n Parse iOS snapshot plists and matching ktx files."
, prog='SnapTriage.py'
, formatter_class=RawTextHelpFormatter)
parser.add_argument('data_dir_snaps',help="Path  to the Snapshot images Directory")
parser.add_argument('data_dir_appState',help="Path to the applicationState.db Directory..")

args = parser.parse_args()
data_dir = args.data_dir_snaps
appState_dir = args.data_dir_appState
count = 0
pathfound = 0

#create directories
#foldername = str(int(datetime.datetime.now().timestamp()))
foldername = ("SnapshotTriageReports_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

#calculate timestamps
unix = datetime.datetime(1970, 1, 1)  # UTC
cocoa = datetime.datetime(2001, 1, 1)  # UTC
delta = cocoa - unix 

for root, dirs, filenames in os.walk(appState_dir):
		for f in filenames:
			if f == "applicationState.db":
				pathfound = os.path.join(root, f)


if pathfound == 0:
	print("No applicationState.db")
else:
	path = os.getcwd()
	try:  
		outpath = path + "/" + foldername
		os.mkdir(outpath)
		os.mkdir(outpath+"/ExtractedBplistsFirstLevel")
		os.mkdir(outpath+"/ExtractedBplistsSecondLevel")
		os.mkdir(outpath+"/Reports")
		os.mkdir(outpath+"/Reports/images")
	except OSError:  
		print("Error making directories")
	
	
	
	print("\n--------------------------------------------------------------------------------------")
	print("iOS Snapshot Triage Parser.")
	print("Objective: Triage iOS Snapshot images.")
	print("By: Alexis Brignoni | @AlexisBrignoni | abrignoni.com")
	print("Processed images directory: " + data_dir)
	print("Snapshots database: " + appState_dir)
	print("\n--------------------------------------------------------------------------------------")
	print("")
	
	print("Database located at: "+pathfound)
	print("Please wait...")
	
	#connect sqlite databases
	#database = 'applicationState.db'
	db = sqlite3.connect(pathfound)
	cursor = db.cursor()

	cursor.execute('''SELECT
	application_identifier_tab.id,
	application_identifier_tab.application_identifier,
	kvs.value
	FROM kvs, application_identifier_tab, key_tab
	WHERE application_identifier_tab.id = kvs.application_identifier
	and key_tab.key = 'XBApplicationSnapshotManifest'
	and key_tab.id = kvs.key
	''')

	all_rows = cursor.fetchall()
	
	for row in all_rows:
		bundleid = row[1]
		wbplist = row [2]
		print('Processing: '+bundleid)
		output_file = open('./'+foldername+'/ExtractedBplistsFirstLevel/'+bundleid+'.bplist', 'wb') #export from applicationState.db
		output_file.write(wbplist)
		output_file.close()
		
		g = open('./'+foldername+'/ExtractedBplistsFirstLevel/'+bundleid+'.bplist', 'rb')
		plistg = ccl_bplist.load(g)
		
		output_file = open('./'+foldername+'/ExtractedBplistsSecondLevel/'+bundleid+'.bplist', 'wb') #export from applicationState.db
		output_file.write(plistg)
		output_file.close()
		
		g = open('./'+foldername+'/ExtractedBplistsSecondLevel/'+bundleid+'.bplist', 'rb')
		plistg = ccl_bplist.load(g)
		long = len(plistg['$objects'])
		
		#start report
		h = open('./'+foldername+'/Reports/'+bundleid+'.html', 'w') #write report
		h.write('<html><body>')
		h.write('<h2>iOS Snapshots Triage Report </h2>')
		h.write('<h3>Application: '+bundleid+'</h3>')
		h.write('Data aggregated per following data source: '+pathfound)
		h.write('<br/>')		
		h.write('Times in UTC')
		h.write('<br/>')
		h.write ('<style> table, th, td {border: 1px solid black; border-collapse: collapse;}</style>')
		h.write('<br/>')
		
		#opne table
		h.write('<table>')
		for i in range (0, long):
			test = (plistg['$objects'][i])
			try:
				if test.endswith('@3x.ktx'):
					h.write('<tr>')
					h.write('<td>')
					image = test.split('.')
					imagenew = image[0]
					path2 = os.getcwd()
					imagepath = (path+'/'+data_dir+'/'+imagenew+'.png')
					imageoutpath = (outpath+'/Reports/images')
					#print ('path2: '+path2)
					#print('image: '+imagepath)
					#print('imagefinal: '+imageoutpath)
					#print('foldername: '+foldername)
					copy(imagepath, imageoutpath)
					h.write('<a href=./images/'+imagenew+'.png target="_blank">')
					h.write('<img src=./images/'+imagenew+'.png width="310" height="552" ')
					h.write('/>')
					h.write('</a>')
					h.write('</td>')
					h.write('</tr>')
					#new html block
					#convert the ktx to jpg and add to html
					#print(test)

			except:
				pass
				
			try:
				if test.endswith('@2x.ktx'):
					h.write('<tr>')
					h.write('<td>')
					image = test.split('.')
					imagenew = image[0]
					h.write('<a href=../../'+data_dir+'/'+imagenew+'.png target="_blank">')
					h.write('<img src=../../'+data_dir+'/'+imagenew+'.png width="310" height="552" ')
					h.write('/>')
					h.write('</a>')
					h.write('</td>')
					h.write('</tr>')
					#new html block
					#convert the ktx to jpg and add to html
					#print(test)
					#new html block
					#convert the ktx to jpg and add to html
				
			except:
				pass
			
			try:
				if test.endswith('.png'):
					h.write('<tr>')
					h.write('<td>')
					h.write('File type not found on system - '+str(test))
					h.write('</td>')
					h.write('</tr>')
					#new html block
					#convert the ktx to jpg and add to html
					#print(test)
				
			except:
				pass
			
			try:
				if test['NS.time']:
					dates = test['NS.time']
					dia = str(dates)
					dias = (dia.rsplit('.', 1)[0])
					timestamp = datetime.datetime.fromtimestamp(int(dias)) + delta
					
					h.write('<tr>')
					h.write('<td>')
					h.write(str(timestamp))
					h.write('</td>')
					h.write('</tr>')
					
					#print(timestamp)
					
			except:
				pass		
		h.write('<table>')
		h.write('<br/>')		
		h.write('Script by: abrignoni.com')
		h.write('</html>')
		h.close()
		count = count + 1
print('Total of apps with processed snapshots: '+str(count))