import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.SequenceFile;
import org.apache.hadoop.io.SequenceFile.Writer;

public class SequenceFileWriterExample {
    public static void main(String[] args) throws IOException {
        Configuration conf = new Configuration();
        conf.set("fs.defaultFS", "file:///");
        Path path = new Path("sequencefile_output.seq");

        IntWritable key = new IntWritable();
        Text value = new Text();
        SequenceFile.Writer writer = SequenceFile.createWriter(conf,
            Writer.file(path),
            Writer.keyClass(IntWritable.class),
            Writer.valueClass(Text.class));
        for (int i = 0; i < 5; i++) {
            key.set(i);
            value.set("Value_" + i);
            writer.append(key, value);
        }

        writer.close();
        System.out.println("Sequence file written successfully.");
    }
}
