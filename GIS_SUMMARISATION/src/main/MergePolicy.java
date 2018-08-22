package main;


//import org.osmdroid.util.GeoPoint;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by bishakh on 6/30/18.
 */

public class MergePolicy {
    public static final int CONVEX_HULL = 1;
    private int policy;

    public MergePolicy(int policy) {
        this.policy = policy;
    }

    public List<point> mergeKmlObjects(KmlObject object1, KmlObject object2) {
        switch (policy) {
            case CONVEX_HULL:
                List<point> polyPoints = new ArrayList<>();
                polyPoints.addAll(object1.getPoints());
                polyPoints.addAll(object2.getPoints());
                return new QuickHull().quickHull(polyPoints);
            default:
                return null;
        }
    }

}