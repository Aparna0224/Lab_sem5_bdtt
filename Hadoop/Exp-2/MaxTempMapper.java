import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class MaxTempMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private Text year = new Text();
    private IntWritable temp = new IntWritable();

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();
        String[] fields = line.split(",");
        if (!fields[0].equals("Year")) { // skip header
            year.set(fields[0]);
            temp.set(Integer.parseInt(fields[3]));
            context.write(year, temp);
        }
    }
}
