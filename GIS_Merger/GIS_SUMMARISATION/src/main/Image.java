package main;

public class Image {

    public double latitude;
    public double longitude;
    public String image_name;
    public String year;
    public String month;
    public String day;
    public String hour;
    public String minute;
    public String second;

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public String getName() {
        return image_name;
    }

    public void setLatitude(double latitude)
    {
        this.latitude=latitude;
    }
    public void setLongitude(double longitude)
    {
        this.longitude = longitude;
    }
    public void setImage_name(String image_name)
    {
        this.image_name = image_name;
    }

    public String getYear(){return year;}
    public String getMonth(){return month;}
    public String getDay(){return day;}
    public String getHour(){return hour;}
    public String getMinute(){return minute;}
    public String getSecond(){return second;}

    public void setYear(String year){this.year=year;}
    public void setMonth(String month){this.month=month;}
    public void setDay(String day){this.day=day;}
    public void setHour(String hour){this.hour=hour;}
    public void setMinute(String minute){this.minute=minute;}
    public void setSecond(String second){this.second=second;}

}
