package main;


import org.influxdb.InfluxDB;
import org.influxdb.InfluxDBFactory;
import org.influxdb.annotation.Column;
import org.influxdb.annotation.Measurement;
import org.influxdb.dto.Point;
import org.influxdb.dto.Pong;
import org.influxdb.dto.Query;
import org.influxdb.dto.QueryResult;
import org.influxdb.impl.InfluxDBResultMapper;
import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;

import java.io.*;
import java.lang.reflect.Array;
import java.time.Instant;
import java.util.*;

public class influx {

    public static HashMap<String, List<point>> map;
    public static final String IMAGE = "image";
    public static final String VIDEO = "video";
    public static final String AUDIO = "audio";

    public static Integer version=-1;



    public static String directory="";


    public static void main(String args[]) throws IOException, InterruptedException {
        InfluxDB influxDB = InfluxDBFactory.connect("http://localhost:8086", "root", "root");
        String dbName = "gis";
        String mergedDb="Merged";


        Pong response = influxDB.ping();
        if (response.getVersion().equalsIgnoreCase("unknown")) {

            System.out.println("error ");
            return;
        }
        directory = args[0];
//        String msg="";
        String versionQuery="select last(version) from memory";
        System.out.println("last Version = "+versionQuery);
        Query queryMerged= new Query(versionQuery,mergedDb);
        QueryResult qres = influxDB.query(queryMerged);

        if(qres.getResults()!=null)
        {
            for(QueryResult.Result result: qres.getResults())
            {
                if(result.getSeries()!=null) {
                    System.out.println("res "+result);
                    for (QueryResult.Series series : result.getSeries()) {
                        if(series!=null) {
                            for (List<Object> data : series.getValues()) {
                                double vert = (double) data.get(1);
                                version = Math.toIntExact(Math.round(vert));
                                break;
                            }
                        }

                    }
                }
            }
        }
        while(true) {

//            msg="";
            map = new HashMap<>();
            ArrayList<Video> videoArrayList = new ArrayList<>();
            ArrayList<Audio> audioArrayList = new ArrayList<>();
            ArrayList<Image> imageArrayList = new ArrayList<>();
            ArrayList<Text>  textArrayList = new ArrayList<>();
            HashMap<String,Integer> contactMap = new HashMap<>();
            HashMap<String,Double>  mediaMap = new HashMap<>();
            File imageFold= new File(args[0]+"sync/SurakshitImages/");
            if(imageFold.exists()) {
                for (File file : imageFold.listFiles()) {
                    if (file.isFile()) {
                        double fileSize = file.length();
                        mediaMap.put(file.getName(), fileSize);
                    }
                }
            }

            File videoFold = new File(args[0]+"sync/SurakshitVideos/");
            if(videoFold.exists()) {
                for (File file : videoFold.listFiles()) {
                    if (file.isFile()) {
                        double fileSize = file.length();
                        mediaMap.put(file.getName(), fileSize);
                    }
                }
            }
            File audioFold = new File(args[0]+"sync/SurakshitAudio/");
            if(audioFold.exists()) {
                for (File file : audioFold.listFiles()) {
                    if (file.isFile()) {
                        double fileSize = file.length();
                        mediaMap.put(file.getName(), fileSize);
                    }
                }
            }
            File mapFold = new File(args[0]+"sync/SurakshitMap/");
            if(mapFold.exists()) {
                for (File file : mapFold.listFiles()) {
                    if (file.isFile()) {
                        double fileSize = file.length();
                        mediaMap.put(file.getName(), fileSize);
                    }
                }
            }
            HashMap<String, ArrayList<Double>> volume=new HashMap<>();
            HashMap<String,ArrayList<Integer>>  countMedia= new HashMap<>();
            try {
                Query query = null;
                String querySt="";
                query = new Query("select lat,long,map,posLat,posLong,metadata,text,year,month,day,hour,minute,second from kml", dbName);
                version++;
                QueryResult queryResult = influxDB.query(query);

                if(queryResult!=null) {
                    for (QueryResult.Result result : queryResult.getResults()) {


                        //System.out.println(result.toString());
                        if(result==null || result.getSeries()==null)
                            continue;
                        for (QueryResult.Series series : result.getSeries()) {


                            contactMap = new HashMap<>();
                            File contFold = new File(args[0]+"/sync/pgpKey/");
                            if(contFold.exists()) {
                                for (File file : contFold.listFiles()) {
                                    String f = file.getName();
                                    System.out.println("file name = " + f);
                                    String[] name = f.split("_", 2);
                                    if (Character.isDigit(name[1].charAt(0))) {
                                        String fh = name[1].substring(0, 10);
                                        contactMap.put(fh, 1);
                                    }


                                }
                            }
                            for (Map.Entry<String,Integer> entry: contactMap.entrySet() )
                            {
                                System.out.println(entry.getKey()+" "+entry.getValue());
                            }

                            //Thread.sleep(20000);


                            for (List<Object> data : series.getValues()) {
                                for (int iii=0 ;iii<=13;iii++)
                                {
                                    if(data.get(iii)==null)
                                        data.set(iii,"");
                                }
                                System.out.print(Arrays.toString(data.toArray()));
                                if (!(data.get(3).equals("") || data.get(3).equals(IMAGE) ||
                                        data.get(3).equals(VIDEO) || data.get(3).equals(AUDIO))) {
                                    if (!map.containsKey((String) data.get(3)))
                                        map.put((String) data.get(3), new ArrayList<>());
                                    point pi = new point();
                                    pi.setLatitude((double) data.get(1));
                                    pi.setLongitute((double) data.get(2));
                                    pi.setAltitude(0);
                                    pi.setYear((String)data.get(8));
                                    pi.setMonth((String)data.get(9));
                                    pi.setDay((String)data.get(10));
                                    pi.setHour((String)data.get(11));
                                    pi.setMinute((String) data.get(12));
                                    pi.setSecond((String) data.get(13));
                                    pi.setMap_name((String)data.get(6));
                                    pi.setPosLatitude((double)data.get(4));
                                    pi.setPosLongitude((double)data.get(5));
                                    map.get((String) data.get(3)).add(pi);
                                    String mediaName=((String) data.get(6));
                                    String[] nameofMap = ((String) data.get(6)).split("_",3);
                                    int cfg=0;
                                    if(contactMap.get(nameofMap[1])!=null) {
                                        if (contactMap.get(nameofMap[1]) == 1) {
                                            cfg++;
                                            if (volume.get(nameofMap[1]) == null) {
                                                ArrayList<Double> tempList = new ArrayList<>();
                                                tempList.add((double) 0);
                                                tempList.add((double) 0);
                                                tempList.add((double) 0);
                                                tempList.add((double) 0);
                                                volume.put(nameofMap[1], tempList);
                                            }
                                            ArrayList<Double> currentSize = volume.get(nameofMap[1]);
                                            Double xc = currentSize.get(3);
                                            xc = currentSize.get(3) + mediaMap.get(mediaName);
                                            currentSize.add(3, xc);
                                            volume.put(nameofMap[1], currentSize);
                                            if (countMedia.get(nameofMap[1]) == null) {
                                                ArrayList<Integer> tempList = new ArrayList<>();
                                                tempList.add(0);
                                                tempList.add(0);
                                                tempList.add(0);
                                                tempList.add(0);
                                                countMedia.put(nameofMap[1], tempList);
                                            }
                                            ArrayList<Integer> counter = countMedia.get(nameofMap[1]);
                                            int xy = counter.get(3);
                                            xy = xy + 1;
                                            counter.add(3, xy);
                                            countMedia.put(nameofMap[1], counter);
                                        }
                                    }
                                    if(cfg==0)
                                    {
                                        nameofMap[1]= nameofMap[1].substring(1,nameofMap[1].length());
                                        if(contactMap.get(nameofMap[1])!=null) {
                                            if (contactMap.get(nameofMap[1]) == 1) {
                                                cfg++;
                                                if (volume.get(nameofMap[1]) == null) {
                                                    ArrayList<Double> tempList = new ArrayList<>();
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    volume.put(nameofMap[1], tempList);
                                                }
                                                ArrayList<Double> currentSize = volume.get(nameofMap[1]);
                                                Double xc = currentSize.get(3);
                                                xc = currentSize.get(3) + mediaMap.get(mediaName);
                                                currentSize.add(3, xc);
                                                volume.put(nameofMap[1], currentSize);
                                                if (countMedia.get(nameofMap[1]) == null) {
                                                    ArrayList<Integer> tempList = new ArrayList<>();
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    countMedia.put(nameofMap[1], tempList);
                                                }
                                                ArrayList<Integer> counter = countMedia.get(nameofMap[1]);
                                                int xy = counter.get(3);
                                                xy = xy + 1;
                                                counter.add(3, xy);
                                                countMedia.put(nameofMap[1], counter);

                                            }
                                        }
                                    }
                                } else if ((data.get(3).equals(VIDEO) || data.get(3).equals(IMAGE) || data.get(3).equals(AUDIO) || data.get(3).equals(""))) {
                                    //System.out.print(data.get(4) + " " + data.get(5));
                                   // msg = msg + data.get(3) + "%" + data.get(4) + "%" + data.get(5) + "%" + data.get(6) + "\n";

                                    if ((data.get(3).equals(VIDEO)))
                                    {
                                       Video video = new Video();
                                       video.setLatitude((double)data.get(4));
                                       video.setLongitude((double) data.get(5));
                                       video.setVideo_name((String) data.get(6));
                                       video.setYear((String)data.get(8));
                                       video.setMonth((String)data.get(9));
                                       video.setDay((String)data.get(10));
                                       video.setHour((String)data.get(11));
                                       video.setMinute((String)data.get(12));
                                       video.setSecond((String)data.get(13));
                                       videoArrayList.add(video);

                                        String mediaName=((String) data.get(6));
                                        String[] nameofMap = ((String) data.get(6)).split("_",3);
                                        int cfg=0;
                                        if(contactMap.get(nameofMap[1])!=null) {
                                            if (contactMap.get(nameofMap[1]) == 1) {
                                                cfg++;
                                                if (volume.get(nameofMap[1]) == null) {
                                                    ArrayList<Double> tempList = new ArrayList<>();
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    volume.put(nameofMap[1], tempList);
                                                }

                                                ArrayList<Double> currentSize = volume.get(nameofMap[1]);
                                                try {
                                                    Double xc = currentSize.get(0);
                                                    xc = currentSize.get(0) + mediaMap.get(mediaName);
                                                    currentSize.add(0, xc);
                                                    volume.put(nameofMap[1], currentSize);
                                                }
                                                catch (Exception e){System.out.println("Ooopps");}

                                                if (countMedia.get(nameofMap[1]) == null) {
                                                    ArrayList<Integer> tempList = new ArrayList<>();
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    countMedia.put(nameofMap[1], tempList);
                                                }
                                                try {
                                                    ArrayList<Integer> counter = countMedia.get(nameofMap[1]);
                                                    int xy = counter.get(0);
                                                    xy = xy + 1;
                                                    counter.add(0, xy);
                                                    countMedia.put(nameofMap[1], counter);
                                                }
                                                catch (Exception e){System.out.println("heyeyey");}

                                            }
                                        }
                                        if(cfg==0)
                                        {
                                            nameofMap[1]= nameofMap[1].substring(1,nameofMap[1].length());
                                            if(contactMap.get(nameofMap[1])!=null) {
                                                if (contactMap.get(nameofMap[1]) == 1) {
                                                    cfg++;
                                                    if (volume.get(nameofMap[1]) == null) {
                                                        ArrayList<Double> tempList = new ArrayList<>();
                                                        tempList.add((double) 0);
                                                        tempList.add((double) 0);
                                                        tempList.add((double) 0);
                                                        tempList.add((double) 0);
                                                        volume.put(nameofMap[1], tempList);
                                                    }
                                                    ArrayList<Double> currentSize = volume.get(nameofMap[1]);
                                                    try {
                                                        Double xc = currentSize.get(0);
                                                        xc = currentSize.get(0) + mediaMap.get(mediaName);
                                                        currentSize.add(0, xc);
                                                        volume.put(nameofMap[1], currentSize);
                                                    }catch (Exception e){System.out.println("ooppp");}
                                                    if (countMedia.get(nameofMap[1]) == null) {
                                                        ArrayList<Integer> tempList = new ArrayList<>();
                                                        tempList.add(0);
                                                        tempList.add(0);
                                                        tempList.add(0);
                                                        tempList.add(0);
                                                        countMedia.put(nameofMap[1], tempList);
                                                    }
                                                    ArrayList<Integer> counter = countMedia.get(nameofMap[1]);
                                                    try {
                                                        int xy = counter.get(0);
                                                        xy = xy + 1;
                                                        counter.add(0, xy);
                                                        countMedia.put(nameofMap[1], counter);
                                                    }catch (Exception e){System.out.println("heyehey");}

                                                }
                                            }
                                        }

                                    }
                                    else if((data.get(3).equals(IMAGE)))
                                    {
                                        Image image = new Image();
                                        image.setLatitude((double)data.get(4));
                                        image.setLongitude((double)data.get(5));
                                        image.setImage_name((String) data.get(6));
                                        image.setYear((String)data.get(8));
                                        image.setMonth((String)data.get(9));
                                        image.setDay((String)data.get(10));
                                        image.setHour((String)data.get(11));
                                        image.setMinute((String)data.get(12));
                                        image.setSecond((String)data.get(13));
                                        imageArrayList.add(image);
                                        String mediaName=((String) data.get(6));
                                        String[] nameofMap = ((String) data.get(6)).split("_",3);
                                        int cfg=0;
                                        if(contactMap.get(nameofMap[1])!=null) {
                                            if (contactMap.get(nameofMap[1]) == 1) {
                                                cfg++;
                                                if (volume.get(nameofMap[1]) == null) {
                                                    ArrayList<Double> tempList = new ArrayList<>();
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    volume.put(nameofMap[1], tempList);
                                                }
                                                ArrayList<Double> currentSize = volume.get(nameofMap[1]);
                                                try {
                                                    Double xc = currentSize.get(2);
                                                    xc = currentSize.get(2) + mediaMap.get(mediaName);
                                                    currentSize.add(2, xc);
                                                    volume.put(nameofMap[1], currentSize);
                                                }catch (Exception e){}
                                                if (countMedia.get(nameofMap[1]) == null) {
                                                    ArrayList<Integer> tempList = new ArrayList<>();
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    countMedia.put(nameofMap[1], tempList);
                                                }
                                                try {
                                                    ArrayList<Integer> counter = countMedia.get(nameofMap[1]);
                                                    int xy = counter.get(2);
                                                    xy = xy + 1;
                                                    counter.add(2, xy);
                                                    countMedia.put(nameofMap[1], counter);
                                                }catch (Exception e){}

                                            }
                                        }
                                        if(cfg==0)
                                        {
                                            nameofMap[1]= nameofMap[1].substring(1,nameofMap[1].length());
                                            if(contactMap.get(nameofMap[1])!=null) {
                                                if (contactMap.get(nameofMap[1]) == 1) {
                                                    cfg++;
                                                    if (volume.get(nameofMap[1]) == null) {
                                                        ArrayList<Double> tempList = new ArrayList<>();
                                                        tempList.add((double) 0);
                                                        tempList.add((double) 0);
                                                        tempList.add((double) 0);
                                                        tempList.add((double) 0);
                                                        volume.put(nameofMap[1], tempList);
                                                    }
                                                    ArrayList<Double> currentSize = volume.get(nameofMap[1]);
                                                    try {
                                                        Double xc = currentSize.get(2);
                                                        xc = currentSize.get(2) + mediaMap.get(mediaName);
                                                        currentSize.add(2, xc);
                                                        volume.put(nameofMap[1], currentSize);
                                                    }
                                                    catch (Exception e){}
                                                    if (countMedia.get(nameofMap[1]) == null) {
                                                        ArrayList<Integer> tempList = new ArrayList<>();
                                                        tempList.add(0);
                                                        tempList.add(0);
                                                        tempList.add(0);
                                                        tempList.add(0);
                                                        countMedia.put(nameofMap[1], tempList);
                                                    }
                                                    try {
                                                        ArrayList<Integer> counter = countMedia.get(nameofMap[1]);
                                                        int xy = counter.get(2);
                                                        xy = xy + 1;
                                                        counter.add(2, xy);
                                                        countMedia.put(nameofMap[1], counter);
                                                    }catch (Exception e){}

                                                }
                                            }
                                        }

                                    }

                                    else if((data.get(3).equals(AUDIO)))
                                    {
                                        Audio audio = new Audio();
                                        audio.setLatitude((double)data.get(4));
                                        audio.setLongitude((double)data.get(5));
                                        audio.setAudio_name((String)data.get(6));
                                        audio.setYear((String)data.get(8));
                                        audio.setMonth((String)data.get(9));
                                        audio.setDay((String)data.get(10));
                                        audio.setHour((String)data.get(11));
                                        audio.setMinute((String)data.get(12));
                                        audio.setSecond((String)data.get(13));
                                        audioArrayList.add(audio);


                                        String mediaName=((String) data.get(6));
                                        String[] nameofMap = ((String) data.get(6)).split("_",3);
                                        int cfg=0;
                                        if(contactMap.get(nameofMap[1])!=null && contactMap.get(nameofMap[1])==1) {
                                            cfg++;
                                            if(volume.get(nameofMap[1])==null) {
                                                ArrayList<Double > tempList = new ArrayList<>();
                                                tempList.add((double) 0);
                                                tempList.add((double) 0);
                                                tempList.add((double) 0);
                                                tempList.add((double) 0);
                                                volume.put(nameofMap[1], tempList);
                                            }
                                            ArrayList<Double> currentSize = volume.get(nameofMap[1]);
                                            try {
                                                Double xc = currentSize.get(1);
                                                xc = currentSize.get(1) + mediaMap.get(mediaName);
                                                currentSize.add(1, xc);
                                                volume.put(nameofMap[1], currentSize);
                                            }catch (Exception e){}
                                            if(countMedia.get(nameofMap[1])==null)
                                            {
                                                ArrayList<Integer > tempList = new ArrayList<>();
                                                tempList.add(0);
                                                tempList.add(0);
                                                tempList.add(0);
                                                tempList.add(0);
                                                countMedia.put(nameofMap[1], tempList);
                                            }
                                            try {
                                                ArrayList<Integer> counter = countMedia.get(nameofMap[1]);
                                                int xy = counter.get(1);
                                                xy = xy + 1;
                                                counter.add(1, xy);
                                                countMedia.put(nameofMap[1], counter);
                                            }catch (Exception e){}

                                        }
                                        if(cfg==0)
                                        {
                                            nameofMap[1]= nameofMap[1].substring(1,nameofMap[1].length());
                                            if(contactMap.get(nameofMap[1])!=null && contactMap.get(nameofMap[1])==1) {
                                                cfg++;
                                                if(volume.get(nameofMap[1])==null) {
                                                    ArrayList<Double > tempList = new ArrayList<>();
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    tempList.add((double) 0);
                                                    volume.put(nameofMap[1], tempList);
                                                }
                                                ArrayList<Double> currentSize = volume.get(nameofMap[1]);
                                                try {
                                                    Double xc = currentSize.get(1);
                                                    xc = currentSize.get(1) + mediaMap.get(mediaName);
                                                    currentSize.add(1, xc);
                                                    volume.put(nameofMap[1], currentSize);
                                                }catch (Exception e){}
                                                if(countMedia.get(nameofMap[1])==null)
                                                {
                                                    ArrayList<Integer > tempList = new ArrayList<>();
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    tempList.add(0);
                                                    countMedia.put(nameofMap[1], tempList);
                                                }
                                                ArrayList <Integer> counter = countMedia.get(nameofMap[1]);
                                                try {
                                                    int xy = counter.get(1);
                                                    xy = xy + 1;
                                                    counter.add(1, xy);
                                                    countMedia.put(nameofMap[1], counter);
                                                }catch (Exception e){}

                                            }
                                        }

                                    }
                                    else if((data.get(3)).equals(""))
                                    {
                                        Text text = new Text();
                                        text.setLatitude((double)data.get(4));
                                        text.setLongitude((double)data.get(5));
                                        text.setText((String)data.get(7));
                                        text.setYear((String)data.get(8));
                                        text.setMonth((String)data.get(9));
                                        text.setDay((String)data.get(10));
                                        text.setHour((String)data.get(11));
                                        text.setMinute((String)data.get(12));
                                        text.setSecond((String)data.get(13));
                                        textArrayList.add(text);


                                    }


                                }
                            }



                            List<KmlObject> kmlObjects = new ArrayList<>();
                            for (String str : map.keySet()) {
                                KmlObject object = new KmlObject();
                                object.setPoints(map.get(str));
                                object.setMessage(str);
                                object = GISMerger.addTileNameAndLevel(object);
                                kmlObjects.add(object);
                            }
                            Date date = new Date();
                            File file = new File(directory+"date.txt");
                            BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(file,true));
                            bufferedWriter.write(date+"%"+version+"\n");
                            bufferedWriter.close();
                            File stat_file = new File(directory+"Statistics.csv");
                            String stat = "*****************************************************************"+"\n"+"\n"+"\n";
                            for (Map.Entry<String,ArrayList<Double>> entry: volume.entrySet())
                            {
                                String name = entry.getKey();
                                String vid = Double.toString(volume.get(name).get(0))+"_"+ Integer.toString(countMedia.get(name).get(0));
                                String aud= Double.toString(volume.get(name).get(1))+"_"+ Integer.toString(countMedia.get(name).get(1));
                                String img = Double.toString(volume.get(name).get(2))+"_"+ Integer.toString(countMedia.get(name).get(2));
                                String mm = Double.toString(volume.get(name).get(3))+"_"+ Integer.toString(countMedia.get(name).get(3));
                                stat =stat+date+","+name+","+vid+","+aud+","+img+","+mm+"\n";
                            }
                            BufferedWriter bufferedWriter1 = new BufferedWriter(new FileWriter(stat_file,true));
                            bufferedWriter1.write(stat);
                            bufferedWriter1.close();
                            //System.out.println("obtained KML objects  ");
                            MergingDecisionPolicy mergingDecisionPolicy = new MergingDecisionPolicy(MergingDecisionPolicy.DISTANCE_THRESHOLD_POLICY
                                    , 40, 0);
                            GISMerger.mergeGIS(mergingDecisionPolicy, kmlObjects, map, directory,videoArrayList,imageArrayList,audioArrayList,textArrayList,version);


                        }

                    }
                }

            }catch (Exception e) {
                e.printStackTrace();
            }
//
            Thread.sleep(900000);

        }


    }
}
