package SoftTfidf;

/**
 * Soft TFIDF-based distance metric, extended to use "soft" token-matching
 * with the JaroWinkler distance metric.
 */

public class JaroWinklerTFIDF extends SoftTFIDF {
    public JaroWinklerTFIDF() {
        super(new JaroWinkler(), 0.9);
    }

    public String toString() {
        return "[JaroWinklerTFIDF:threshold=" + getTokenMatchThreshold() + "]";
    }

    static public void main(String[] argv) {
        String[] array = {"computer science block area", "science cmputre department building"};
//        argv[1] = "science camputer";
        doMain(new JaroWinklerTFIDF(), array);
    }
}
