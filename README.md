# iOS-Snapshot-Triage-Parser

For details on how to use the scripts and macOS Automator quick action see the following blog post:  
https://abrignoni.blogspot.com/2019/09/ios-snapshots-triage-parser-working.html

Script purpose and workflow:
1. Run SnapshotImageFinder.py to identify iOS snapshot images and extract them from a targeted iOS file system extraction directory. These files end with @3.ktx or @2.ktx.  

2. Extract the macOS Automator quick action from the ktx_quick.zip file. With it convert all the .ktx files extracted in step #1 to .png format.  

3. Run SnapshotTriage.py to extract, parse and match the images with the snapshot metadata contained in the extracted bplists from the applicationState.db datastore. This script accepts 2 parameters, the directory where the applicationState.db is located and the directory where the .png files are located.  

4. After execution of the previews steps a triage report directory will be created containing the extracted bplists and iOS snapshot reports in HTML per app.   
