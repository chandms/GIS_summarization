# DISARM Automation Scripts


MCS Decrypter
--------

To run the script follow the steps:

1. Copy the entire `MCSDecrypter_jar` directory to a suitable location and cd into the directory
    ```
    cd Disarm-Automation-Scripts/MCSDecrypter/out/artifacts/MCSDecrypter_jar
    ```
2. Run the MCSDecrypter.jar script
	```
    java -jar MCSDecrypter.jar <path to /Working/SurakshitKml directory> <decrypted destination directory>  <path to volunteer private key>
    ```
    Example:
    ```
    java -jar MCSDecrypter.jar /home/bishakh/DMS/sync/SurakshitKml /home/bishakh/DMS/decrypted  /home/bishakh/DMS/volunteer_pri.bgp
    ```
