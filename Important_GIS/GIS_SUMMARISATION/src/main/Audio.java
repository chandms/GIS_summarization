package main;

public class Audio {

    public double latitude;
    public double longitude;
    public String audio_name;
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
        return audio_name;
    }

    public void setLatitude(double latitude)
    {
        this.latitude = latitude;
    }
    public void setLongitude(double longitude)
    {
        this.longitude = longitude;
    }

    public void setAudio_name(String audio_name)
    {
        this.audio_name = audio_name;
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
