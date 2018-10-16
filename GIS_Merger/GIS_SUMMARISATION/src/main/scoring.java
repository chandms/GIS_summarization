package main;

import SoftTfidf.JaroWinklerTFIDF;
import org.omg.PortableInterceptor.SYSTEM_EXCEPTION;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

import static main.GISMerger.distance;

public class scoring {


    public static void main(String args[]) throws IOException {

        File obtained = new File("/home/chandrika/Desktop/upload/DataDiff/obtained.txt");

        File diff_write = new File("/home/chandrika/Desktop/upload/DataDiff/result_data.txt");
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(diff_write));
        bufferedWriter.write("");
        bufferedWriter.close();
        File diff_write_comp = new File("/home/chandrika/Desktop/upload/DataDiff/result_comp.txt");
        BufferedWriter bufferedWriter1 = new BufferedWriter(new FileWriter(diff_write_comp));
        bufferedWriter1.write("");
        bufferedWriter1.close();

        BufferedReader bufferedReader = new BufferedReader(new FileReader(obtained));


        while(bufferedReader.read()!=-1)
        {
            String line = bufferedReader.readLine();
            String[] words=line.split(":");
            String lat = words[1];
            lat=lat.substring(1,lat.length()-1);
            String lng = words[2];
            lng = lng.substring(1,lng.length()-1);

            String[] laa = lat.split(", ");
            String[] lnn = lng.split(", ");
            ArrayList<Double> lat_array = new ArrayList<>();
            ArrayList<Double> lng_array = new ArrayList<>();
            for(String str : laa){
                str = str.trim().substring(1,str.length()-1);
                lat_array.add(Double.parseDouble(str));

            }
            for(String str : lnn){
                str = str.trim().substring(1,str.length()-1);
                lng_array.add(Double.parseDouble(str));

            }
            ArrayList<point> pointList= new ArrayList<>();
            for (int j=0;j<lat_array.size();j++) {
                point pp = new point();
                pp.setLongitute(lng_array.get(j));
                pp.setLatitude(lat_array.get(j));
                pointList.add(pp);
            }
//            System.out.println(words[0]);
            String[] text= words[0].substring(1,words[0].length()-1).split(", ");
            ArrayList<String > arr = new ArrayList<>();
            for(String str : text)
            {
                if(str.charAt(0)=='\'' || str.charAt(0)=='"')
                    str=str.substring(1);
                if(str.charAt(str.length()-1)=='\'' || str.charAt(str.length()-1)=='"')
                    str = str.substring(0,str.length()-1);
                arr.add(str);

            }
//            System.out.println(arr);
            File ground = new File("/home/chandrika/Desktop/upload/DataDiff/ground_truth.txt");
            BufferedReader bufferedReader1 = new BufferedReader(new FileReader(ground));
            double max_now =-1;
            ArrayList <point> final_points = new ArrayList<>();
            String final_string ="";
            String ob_string ="";
            while (bufferedReader1.read()!=-1)
            {
                String line_buf = bufferedReader1.readLine();
                String[] word_buf = line_buf.split(":");
                word_buf[0]=word_buf[0].trim();
                String text_comp= word_buf[0];
                String laal=word_buf[1].substring(1,word_buf[1].length()-1);
                String lnnl= word_buf[2].substring(1,word_buf[2].length()-1);
                String[] lat_buf = laal.split(", ");
                String [] long_buf = lnnl.split(", ");
                ArrayList<Double> lat_buf_arr= new ArrayList<>();
                ArrayList<Double> long_buf_arr = new ArrayList<>();
                for(String str : lat_buf)
                {
                    lat_buf_arr.add(Double.parseDouble(str));
                }
                for(String str : long_buf)
                {
                    long_buf_arr.add(Double.parseDouble(str));
                }
                ArrayList<point> comp_point = new ArrayList<>();
                for(int jk=0;jk<lat_buf_arr.size();jk++)
                {
                    point point1  = new point();
                    point1.setLatitude(lat_buf_arr.get(jk));
                    point1.setLongitute(long_buf_arr.get(jk));
                    comp_point.add(point1);
                }

                for (String str : arr)
                {
                    double tfidfScore = new JaroWinklerTFIDF().score(str,text_comp);
                    if(max_now<tfidfScore)
                    {
                        max_now=tfidfScore;
                        final_points= comp_point;
                        final_string=text_comp;
                        ob_string=str;
                    }
                }



            }
            if(max_now>=.49)
            {
                Double diff = housedorffDistance(final_points,pointList);
                System.out.println(diff+" "+final_string+" "+ob_string);
                diff_write = new File("/home/chandrika/Desktop/upload/DataDiff/result_data.txt");
                diff_write_comp = new File("/home/chandrika/Desktop/upload/DataDiff/result_comp.txt");
                bufferedWriter = new BufferedWriter(new FileWriter(diff_write,true));
                bufferedWriter1 = new BufferedWriter(new FileWriter(diff_write_comp,true));
                bufferedWriter.write(diff+"\n");
                bufferedWriter1.write(diff+":: obtained = "+ob_string+":: ground_truth = "+final_string+"\n");
                bufferedWriter.close();
                bufferedWriter1.close();
            }


        }

    }
    //Method to calculate Hausdorff Distance between two Polygons
    public static double housedorffDistance(ArrayList<point> points1,ArrayList<point> points2) {
        double hDistance1, hDistance2;
        hDistance1 = hDistance2 = Double.MIN_VALUE;
        for (point p1 : points1) {
            double mind = Double.MAX_VALUE;
            for (point p2 : points2) {
                double d = distance(p1.getLatitude(), p2.getLatitude(), p1.getLongitude(), p2.getLongitude(), 0,0);
                if (d < mind)
                    mind = d;
            }
            if (hDistance1 < mind)
                hDistance1 = mind;
        }
        for (point p1 : points2) {
            double mind = Double.MAX_VALUE;
            for (point p2 : points1) {
                double d = distance(p1.getLatitude(), p2.getLatitude(), p1.getLongitude(), p2.getLongitude(), 0,0);
                if (d < mind)
                    mind = d;
            }
            if (hDistance2 < mind)
                hDistance2 = mind;
        }
        if (hDistance1 > hDistance2)
            return hDistance1;
        return hDistance2;
    }

}
