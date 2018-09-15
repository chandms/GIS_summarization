
package main;

public class point {
    public double latitude;
    public double longitute;
    public double altitude;
    public String year;
    public String month;
    public String day;
    public String hour;
    public String minute;
    public String second;
    public String map_name;
    public double posLatitude;
    public double posLongitude;

    public double getposLongitute() {
        return posLongitude;
    }
    public double getPosLatitude()
    {
        return posLatitude;
    }
    public void setPosLatitude(double posLatitude)
    {
        this.posLatitude=posLatitude;
    }
    public void setPosLongitude(double posLongitude)
    {
        this.posLongitude=posLongitude;
    }
    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public void setLongitute(double longitute) {
        this.longitute = longitute;
    }

    public void setAltitude(double altitude) {
        this.altitude = altitude;
    }

    public double getLongitude() {
        return longitute;
    }

    public double getAltitude() {
        return altitude;
    }

    public String getMap_name(){return map_name;}

    @Override
    public String toString() {
        return "(" + getLatitude() + " " + getLongitude() + ")";
    }

    public String getYear(){return year;}
    public String getMonth(){return month;}
    public String getDay(){return day;}
    public String getHour(){return hour;}
    public String getMinute(){return minute;}
    public String getSecond(){return second;}

    public void setYear(String year){this.year=year;}
    public void setMonth(String month){this.minute=month;}
    public void setDay(String day){this.day=day;}
    public void setHour(String hour){this.hour=hour;}
    public void setMinute(String minute){this.minute=minute;}
    public void setSecond(String second){this.second=second;}
    public void setMap_name(String map_name){this.map_name=map_name;}
}