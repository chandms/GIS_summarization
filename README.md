# GIS_summarization

## Prerequisites

1. [Link to psync](https://github.com/ItsForkIT/psync-pc)
2. [Link to Disarm-Automation-Scripts](https://github.com/ItsForkIT/Disarm-Automation-Scripts)
3. Install influxdb, Create two Databases - gis and Merged and create measurements kml and memory respectively.

Clone both of these (1 & 2) repositories in your local machine.

## Steps to Run the Project

**Folder Structure** 

a. Make a working Directory

b. Clone this repository
  * Create folder "fold"
   
         copy all the contents of leaflet in fold.
      
         create a "sync" folder inside fold which is the destination of synced files by psync.
    
  * Create folder "PatchedKML"
   
  * Create folder "kmlFiles" and create another folder "tempDecrypt" inside kmlFiles
   
  * Copy "script" folder
   
  * Collect the Jar file from [Link](https://github.com/chandms/GIS_summarization/blob/master/GIS_Merger/GIS_SUMMARISATION/out/artifacts/CM_GIS_SUMMARISATION_jar/GIS_SUMMARISATION.jar). Store that jar in this current directory.(This is the Merger).
   
  * copy Copier.py
   
  * copy counter.py
   
  * copy workable.py (KML Parser which inserts data into kml measurement of gis database in influxdb)
   
  * copy "ftpd-sync" folder outside the current folder.
   
         create "work" folder inside it.
c. Create another folder "psn" outside and store the psync jar and destination of sync folder(Created Directory/fold/sync/) is passed through arguments.
 
 
 **Running Process**
 
 Store all the services in /etc/systemd/system
 
 a. run psync
 
 b. python3 workable.py ~/Created Directory/PatchedKML/ (test_parser)
 
 c. java -jar GIS_SUMMARIZATION.jar ~/Created Directory/fold/ DB_NAME (test_merger)
 
 d. run diffpatcher (test_diffpatcher)
 
 e  run decrypter   (test_decrypter)
 
 d. python3 counter.py ~/Created Directory/fold/sync/ ( test_counter,Required for some statistical calculation)
 
 e. python3 copier.py (copies some files from fold directory to ~/ftpd-sync/work/)
 
 f. python3 runner.py ( initialtion of longrange rsync)
   
