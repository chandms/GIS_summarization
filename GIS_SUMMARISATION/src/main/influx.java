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

import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class influx {

    public static HashMap<String, List<point>> map;
    public static final String IMAGE = "image";
    public static final String VIDEO = "video";
    public static final String AUDIO = "audio";

    public static String directory="";


    public static void main(String args[]) throws IOException {
        directory=args[0];
        map = new HashMap<>();
        InfluxDB influxDB = InfluxDBFactory.connect("http://localhost:8086", "root", "root");
        String dbName = "gis";

        String rpName = "aRetentionPolicy";

        //influxDB.createRetentionPolicy(rpName, dbName, "30d", "30m", 2, true);
        Pong response = influxDB.ping();
        if (response.getVersion().equalsIgnoreCase("unknown")) {
            //log.error("Error pinging server.");
            System.out.println("error ");
            return;
        }
        influxDB.createDatabase(dbName);
        influxDB.createRetentionPolicy("awesome_policy", "gis", "30d", '3', true);
        Query query = new Query("select lat,long,map from kml", "gis");
        QueryResult queryResult = influxDB.query(query);

//        System.out.println(queryResult.toString());

        /*InfluxDBResultMapper resultMapper = new InfluxDBResultMapper();
        List<MemoryPoint> memoryPointList = resultMapper
                .toPOJO(queryResult, MemoryPoint.class);*/
        for (QueryResult.Result result : queryResult.getResults()) {

            // print details of the entire result
            System.out.println(result.toString());

            // iterate the series within the result
            for (QueryResult.Series series : result.getSeries()) {
                // System.out.println("series.getName() = " + series.getName());
                //System.out.println("series.getColumns() = " + series.getColumns());
//                System.out.println("series.getValues() = " + series.getValues());

                for (List<Object> data : series.getValues()) {
//                    System.out.println(data);
                    if (!(data.get(3).equals("........") || data.get(3).equals(IMAGE) ||
                            data.get(3).equals(VIDEO) || data.get(3).equals(AUDIO))) {
                        if (!map.containsKey((String) data.get(3)))
                            map.put((String) data.get(3), new ArrayList<>());
                        point pi = new point();
                        pi.setLatitude((double) data.get(1));
                        pi.setLongitute((double) data.get(2));
                        pi.setAltitude(0);
                        map.get((String) data.get(3)).add(pi);
                    }
                }
                List<KmlObject> kmlObjects = new ArrayList<>();
                for (String str : map.keySet()) {
                    KmlObject object = new KmlObject();
                    object.setPoints(map.get(str));
                    object.setMessage(str);
                    object =GISMerger.addTileNameAndLevel(object);
                    kmlObjects.add(object);
                }
                System.out.println("obtained KML objects  ");
                /*for (KmlObject kmlObject : kmlObjects)
                    System.out.println(kmlObject);*/
                //System.out.println("pupul    ............");
                MergingDecisionPolicy mergingDecisionPolicy = new MergingDecisionPolicy(MergingDecisionPolicy.DISTANCE_THRESHOLD_POLICY
                ,40,0);
                GISMerger.mergeGIS(mergingDecisionPolicy,kmlObjects,map,directory);
                //System.out.println("series.getTags() = " + series.getTags());
                /*System.out.println("Hi chandrika");
                for (Map.Entry<String, List<point>> entry: map.entrySet())
                {
                    System.out.println("Key = "+entry.getKey());
                    System.out.println("Vlaue  = "+entry.getValue());
                }*/

            }
        }

        System.out.println();


    }
}
