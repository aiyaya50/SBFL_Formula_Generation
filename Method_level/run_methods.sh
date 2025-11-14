# Setup

work_dir="/home/aiyaya50/SBFL_Formula_Generation/method_level"
data_dir="/home/aiyaya50/Bugs"
main_dir="/home/aiyaya50"



# Get GZoltar

export GZOLTAR_AGENT_JAR="$main_dir/gzoltar/com.gzoltar.agent.rt/target/com.gzoltar.agent.rt-1.7.4-SNAPSHOT-all.jar"
export GZOLTAR_CLI_JAR="$main_dir/gzoltar/com.gzoltar.cli/target/com.gzoltar.cli-1.7.4-SNAPSHOT-jar-with-dependencies.jar"
export D4J_HOME="/home/aiyaya50/defects4j"


# Collect metadata
cd "$data_dir/$PID-${BID}b"

src_classes_dir=$(cat src_classes_dir.txt)
test_classpath=$(cat test_classpath.txt)

cd "$data_dir/$PID-${BID}b"

ser_file="$data_dir/$PID-${BID}b/gzoltar.ser"

cd "$work_dir"
output_dir="/home/aiyaya50/Bugs/$PID-${BID}b/sfl_method"
mkdir $output_dir
java -cp "$src_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$test_classpath:$GZOLTAR_CLI_JAR" \
    com.gzoltar.cli.Main faultLocalizationReport \
      --buildLocation "$src_classes_dir" \
      --granularity "methods" \
      --inclPublicMethods \
      --inclStaticConstructors \
      --inclDeprecatedMethods \
      --dataFile "$ser_file" \
      --outputDirectory "$output_dir" \
      --family "sfl" \
      --formula "ochiai:Ochiai2:Meco:Tarantula:Barinel:Jaccard:Opt:DStar:Sgf_1:Sgf_2:Fo1:Fo2:Fo3:Fo4:Fo5:Fo6:Fo7:Fo8:Fo9:Fo10:Fo12:Fo13:Fo14:Fo15:Fo16:Fo17:Fo19:Fo20:Fo21:Fo22" \
      --metric "entropy" \
      --formatter "txt" \
      
