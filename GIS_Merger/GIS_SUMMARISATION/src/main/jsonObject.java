package main;

import java.util.HashMap;

public class jsonObject {

    private HashMap <String,String> mergedContent = new HashMap<>();
    public String coordinates;
    public String clusterString;
    public String Version;
    public String flag;
    public String position;
    public String metadata;

    public jsonObject(HashMap<String,String> mp) {
        super();
        mergedContent = mp;
        this.coordinates = mergedContent.get("coordinates");
        this.clusterString = mergedContent.get("clusterString");
        this.Version = mergedContent.get("version");
        this.flag = mergedContent.get("flag");
        this.position = mergedContent.get("position");
        this.metadata = mergedContent.get("metadata");
    }



    public String getCoordinates(){return coordinates;}
    public String getClusterString() { return clusterString;}
    public String getVersion() { return Version;}
    public String getFlag(){return flag;}
    public String getPosition() { return position;}
    public String getMetadata() {return metadata;}


}
