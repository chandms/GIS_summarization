# GIS_summarization

## Prerequisites

1. [Link to psync](https://github.com/ItsForkIT/psync-pc)
2. [Link to Disarm-Automation-Scripts](https://github.com/ItsForkIT/Disarm-Automation-Scripts)
3. Install **influxdb**, Create two Databases - **gis** and **Merged** and create _measurements_ **kml** and **memory** respectively.

Clone both of these (1 & 2) repositories in your local machine.

## Steps to Run the Project

**Folder Structure** 

a. Make a _working Directory_ (here consider the folder named **lr_test**)

b. Clone this repository and include following in lr_test.
  * Create folder "fold"
   
         copy all the contents of leaflet in fold.
      
         create a "sync" folder inside fold which is the destination of synced files by psync.
    
  * Create folder "PatchedKML".
   
  * Create folder "kmlFiles" and create another folder "tempDecrypt" inside kmlFiles.
   
  * Copy "script" folder.
   
  * Collect the Jar file from [Merging Jar Link](https://github.com/chandms/GIS_summarization/blob/master/GIS_Merger/GIS_SUMMARISATION/out/artifacts/CM_GIS_SUMMARISATION_jar/GIS_SUMMARISATION.jar). Store that jar in lr_test.
   
  * copy copier.py (copies some files from fold directory to ~/ftpd-sync/work/)
   
  * copy counter.py (Required for some statistical calculation)
   
  * copy workable.py (KML Parser which inserts data into kml measurement of gis database in influxdb)
  
c. copy "ftpd-sync" folder outside the current folder.
   
         create "work" folder inside it.
         
d. Create another folder "psn" outside and store the psync jar and destination of sync folder(~/lr_test/fold/sync/) is passed through arguments.
 
 
 **Running Process**
 
 Store all the services in /etc/systemd/system
 
 a. run psync (sudo systemctl start psync.service)
 
 b. python3 workable.py ~/lr_test/PatchedKML/ (test_parser) (sudo systemctl start test_parser.service)
 
 c. java -jar GIS_SUMMARIZATION.jar ~/lr_test/fold/ DB_NAME (test_merger) (sudo systemctl start test_merge.service)
 
 d. run diffpatcher (test_diffpatcher) (sudo systemctl start test_diffpatcher.service)
 
 e  run decrypter   (test_decrypter) (sudo systemctl start test_decrypter.service)
 
 d. python3 counter.py ~/lr_test/fold/sync/ (sudo systemctl start test_counter.service) 
 
 e. python3 copier.py (sudo systemctl start test_copier.service)
 
 f. python3 runner.py (sudo systemctl start test_runner.service)
   
