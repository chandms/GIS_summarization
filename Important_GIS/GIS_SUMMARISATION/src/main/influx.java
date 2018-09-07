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
            try {
                Query query = null;
                String querySt="";
                query = new Query("select lat,long,map,posLat,posLong,metadata,text,year,month,day,hour,minute,second from kml", dbName);
                version++;
                QueryResult queryResult = influxDB.query(query);

                if(queryResult!=null) {
                    for (QueryResult.Result result : queryResult.getResults()) {


                        //System.out.println(result.toString());

                        for (QueryResult.Series series : result.getSeries()) {


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
//            File file = new File(directory + "media.txt");
//            PrintWriter printWriter = new PrintWriter(file);
//            printWriter.write("");
//            printWriter.close();
//            BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(file));
//
//            bufferedWriter.write(msg);
//            bufferedWriter.close();
//            System.out.println("hi I reached there");

            Thread.sleep(180000);

        }


    }
}
