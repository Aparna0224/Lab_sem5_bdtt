import java.io.*;
import java.util.HashMap;
import org.apache.hadoop.io.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.conf.Configuration;

public class MapSideJoinMapper extends Mapper<LongWritable, Text, Text, Text> {

    private HashMap<String, String> customerMap = new HashMap<>();
    private Text outputKey = new Text();
    private Text outputValue = new Text();

    @Override
    protected void setup(Context context) throws IOException {
        Path[] cacheFiles = context.getLocalCacheFiles();
        File f = new File(cacheFiles[0].toUri());
        BufferedReader reader = new BufferedReader(new FileReader(f));

        String line;
        while ((line = reader.readLine()) != null) {
            String[] parts = line.split(",");
            customerMap.put(parts[0], parts[1]);
        }
        reader.close();
    }

    public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        String[] parts = value.toString().split(",");
        String orderId = parts[0];
        String custId = parts[1];
        String amount = parts[2];

        String custName = customerMap.get(custId);

        if (custName != null) {
            outputKey.set(orderId);
            outputValue.set(custName + "," + amount);
            context.write(outputKey, outputValue);
        }
    }
}
