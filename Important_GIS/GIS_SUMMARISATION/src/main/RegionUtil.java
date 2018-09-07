package main;


import java.awt.*;
import java.awt.geom.Point2D;
import java.lang.*;
import java.util.List;

public class RegionUtil {



    public static double distance(double lat1, double lat2, double lon1,
                                  double lon2, double el1, double el2) {

        final int R = 6371; // Radius of the earth

        double latDistance = Math.toRadians(lat2 - lat1);
        double lonDistance = Math.toRadians(lon2 - lon1);
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2))
                * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        double distance = R * c * 1000; // convert to meters

        double height = el1 - el2;

        distance = Math.pow(distance, 2) + Math.pow(height, 2);

        return Math.sqrt(distance);
    }

    static boolean coordinateInRegion(KmlObject object, double glat, double glong) {
        boolean result=false;
        int i, j;
        boolean isInside = false;
        //create an array of coordinates from the region boundary list
        double givenLat=glat;
        double givenLong=glong;
        int len= object.getPoints().size();
        point[] verts = object.getPoints().toArray(new point[len]);
        int sides = verts.length;
        double minLatitude=90,maxLatitude=-90,minLongitude=180,maxLongitude=-180;
        for(int jy=0;jy<sides;jy++)
        {
            if(verts[jy].getLatitude()<minLatitude)
                minLatitude=verts[jy].getLatitude();
            if(verts[jy].getLongitude()<minLongitude)
                minLongitude=verts[jy].getLongitude();
            if(verts[jy].getLongitude()>maxLongitude)
                maxLongitude=verts[jy].getLongitude();
            if(verts[jy].getLatitude()>maxLatitude)
                maxLatitude=verts[jy].getLatitude();
        }
//        System.out.println(minLatitude+" ," +minLongitude+","+maxLatitude+","+maxLongitude);
        double centreLatitude = (minLatitude+maxLatitude)/2;
        double centreLongitude = (maxLongitude+minLongitude)/2;
        double dist = distance(centreLatitude,givenLat,centreLongitude,givenLong,0,0);
//        System.out.println(centreLatitude+","+centreLongitude);
        System.out.println("Distance there "+dist);
        if(dist<=100)
            result= true;

        for (i = 0, j = sides-1; i < sides; j = i++) {

            if ( ((verts[i].getLatitude()>givenLat) != (verts[j].getLatitude()>givenLat)) &&
                    (givenLong < (verts[j].getLongitude()-verts[i].getLongitude()) * (givenLat-verts[i].getLatitude()) / (verts[j].getLatitude()-verts[i].getLatitude()) + verts[i].getLongitude()) )
                isInside = !isInside;


        }
        if(isInside==true || result==true)
            return true;
        else
            return false;
    }
}