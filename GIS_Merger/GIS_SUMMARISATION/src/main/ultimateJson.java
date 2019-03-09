package main;

import java.util.ArrayList;

public class ultimateJson {

    public String version;
    public  ArrayList <jsonObject> jsonObjects;
    public ultimateJson(ArrayList<jsonObject> ar,String ver) {
        super();

        jsonObjects = ar;
        version = ver;

    }
}
