package main;

import java.util.Random;

public class MergingDecisionPolicy {
    private int policy;
    private double thresholdDistance;
    private double thresholdtdIdfScore;
    public static final int RANDOM_POLICY = 1;
    public static final int DISTANCE_THRESHOLD_POLICY = 2;
    public static final int DISTANCE_OR_TFIDF_THRESHOLD_POLICY = 3;
    public static final int DISTANCE_AND_TFIDF_THRESHOLD_POLICY = 4;
    public static final int TFIDF_AND_DISTANCE_THRESHOLD_POLICY = 6;
    public static final int TFIDF_THRESHOLD_POLICY = 5;

    public MergingDecisionPolicy(int policy, double thresholdDistance, double thresholdtdIdfScore) {
        this.policy = policy;
        this.thresholdDistance = thresholdDistance;
        this.thresholdtdIdfScore = thresholdtdIdfScore;
    }

    public boolean mergeDecider(double tfidfScore, double housDroff) {
        switch (policy) {
            case RANDOM_POLICY:
                Random random = new Random();
                return random.nextBoolean();
            case DISTANCE_THRESHOLD_POLICY:
                return housDroff <= thresholdDistance;
            case DISTANCE_OR_TFIDF_THRESHOLD_POLICY:
                return housDroff <= thresholdDistance || tfidfScore >= thresholdtdIdfScore;
            case DISTANCE_AND_TFIDF_THRESHOLD_POLICY:
                return housDroff <= thresholdDistance && tfidfScore >= thresholdtdIdfScore;
            case TFIDF_THRESHOLD_POLICY:
                return tfidfScore >= thresholdtdIdfScore;
            case TFIDF_AND_DISTANCE_THRESHOLD_POLICY:
                return tfidfScore >= thresholdtdIdfScore && housDroff <= thresholdDistance;
            default:
                return false;
        }
    }
}