import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.*;
import org.apache.hadoop.mapreduce.lib.output.*;

public class MapSideJoinDriver {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Map Side Join");

        job.setJarByClass(MapSideJoinDriver.class);
        job.setMapperClass(MapSideJoinMapper.class);
        job.setNumReduceTasks(0); // No reducer
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        // Add customers.txt to distributed cache
        job.addCacheFile(new Path("/input/customers.txt").toUri());

        FileInputFormat.addInputPath(job, new Path("/input/orders.txt"));
        FileOutputFormat.setOutputPath(job, new Path("/output_mapjoin"));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
