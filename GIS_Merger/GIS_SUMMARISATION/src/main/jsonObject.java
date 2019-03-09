package main;

import org.codehaus.jackson.map.ObjectMapper;

import java.util.ArrayList;
import java.util.HashMap;

public class jsonObject {

    private HashMap <String,Object> mergedContent = new HashMap<>();
    public String coordinates;
    public Object clusterString;
    public String Version;
    public String flag;
    public String position;
    public String metadata;

    public jsonObject(HashMap<String,Object> mp) {
        super();
        mergedContent = mp;
        this.coordinates = mergedContent.get("coordinates").toString();
        this.clusterString = mergedContent.get("clusterString");
        this.Version = mergedContent.get("version").toString();
        this.flag = mergedContent.get("flag").toString();
        this.position = mergedContent.get("position").toString();
        this.metadata = mergedContent.get("metadata").toString();
    }



    public String getCoordinates(){return coordinates;}
    public Object getClusterString() { return clusterString;}
    public String getVersion() { return Version;}
    public String getFlag(){return flag;}
    public String getPosition() { return position;}
    public String getMetadata() {return metadata;}


}
