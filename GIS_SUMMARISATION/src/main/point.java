
package main;

public class point {
    public double latitude;
    public double longitute;
    public double altitude;


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

    @Override
    public String toString() {
        return "(" + getLatitude() + " " + getLongitude() + ")";
    }
}