import java.io.File;

public class decrypter {

    static String sourcePath;
    static String destPath;
    static String volunteerPrivKeyPath;
    static String volunteerPubKeyPath;

static Runnable decrypter  = new Runnable() {
    @Override
    public void run() {
        while(true){
            System.out.println("Scanning: " + sourcePath);
            File dir = new File(sourcePath);
            File[] directoryListing = dir.listFiles();
            if (directoryListing != null) {
                for (File child : directoryListing) {
                    System.out.println(child.getAbsolutePath());

                    if(child.getName().contains("volunteer")){
                        File destFile = new File(destPath + File.separator + child.getName().replace("bgp", "kml"));
                        if(!destFile.exists()) {
                            System.out.println("Decrypting.." + child.getAbsolutePath() + " to " + destPath);
                            try {
                                KeyBasedFileProcessor.decrypt(child.getAbsolutePath(), volunteerPrivKeyPath, volunteerPubKeyPath,  "volunteer@disarm321", destPath);
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        }
                        else {
                            System.out.println("SKIPPING AS EXISTS: " + child.getAbsolutePath());
                        }

                    }else{
                        System.out.println("SKIPPING AS NOT VOLUNTEER: " + child.getAbsolutePath());

                    }
                }
            } else {

            }
            System.out.println("===============================");


            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
};




public static void main(String args[]){
    sourcePath = args[0];
    destPath = args[1];
    volunteerPrivKeyPath = args[2];
    volunteerPubKeyPath = args[3];
//    sourcePath = "/home/bishakh/DMS/sync/SurakshitKml";
//    destPath = "/home/bishakh/DMS/decrypted";
//    volunteerKeyPath = "/home/bishakh/DMS/volunteer_pri.bgp";



    // Decryption Test

//    try {
//        KeyBasedFileProcessor.decrypt("/sdcard/video.mp4.bpg", "/sdcard/secret.bpg", "123");
//    } catch (Exception e) {
//        e.printStackTrace();
//    }
    Thread decrypterThread = new Thread(decrypter);
    decrypterThread.start();



System.out.println("++++++++++ Decrypter Started +++++++++");
}


}
