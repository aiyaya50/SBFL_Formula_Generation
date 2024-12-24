PID=Time
BID=1
# Setup

work_dir="/home/aiyaya50/Bugs"
main_dir="/home/aiyaya50"
export _JAVA_OPTIONS="-Xmx6144M -XX:MaxHeapSize=4096M"
export MAVEN_OPTS="-Xmx1024M"
export ANT_OPTS="-Xmx6144M -XX:MaxHeapSize=4096M"


# Get GZoltar

export GZOLTAR_AGENT_JAR="$main_dir/gzoltar/com.gzoltar.agent.rt/target/com.gzoltar.agent.rt-1.7.4-SNAPSHOT-all.jar"
export GZOLTAR_CLI_JAR="$main_dir/gzoltar/com.gzoltar.cli/target/com.gzoltar.cli-1.7.4-SNAPSHOT-jar-with-dependencies.jar"


# Get D4J

export D4J_HOME="/home/aiyaya50/defects4j"

#
# Checkout Closure-27, compile it, and get its metadata
#

# Checkout
cd "$work_dir"
rm -rf "$PID-${BID}b"; "$D4J_HOME/framework/bin/defects4j" checkout -p "$PID" -v "${BID}b" -w "$PID-${BID}b"

# Compile
cd "$work_dir/$PID-${BID}b"
defects4j compile

# Collect metadata
cd "$work_dir/$PID-${BID}b"
test_classpath=$($D4J_HOME/framework/bin/defects4j export -p cp.test)
src_classes_dir=$($D4J_HOME/framework/bin/defects4j export -p dir.bin.classes)
src_classes_dir="$work_dir/$PID-${BID}b/$src_classes_dir"
test_classes_dir=$($D4J_HOME/framework/bin/defects4j export -p dir.bin.tests)
test_classes_dir="$work_dir/$PID-${BID}b/$test_classes_dir"
echo "$PID-${BID}b's classpath: $test_classpath" >&2
echo $test_classpath > "$work_dir/$PID-${BID}b/test_classpath.txt";
echo "$PID-${BID}b's bin dir: $src_classes_dir" >&2
echo $src_classes_dir > "$work_dir/$PID-${BID}b/src_classes_dir.txt";
echo "$PID-${BID}b's test bin dir: $test_classes_dir" >&2
echo $test_classes_dir > "$work_dir/$PID-${BID}b/test_class_dir.txt";
#
# Collect unit tests to run GZoltar with
#

cd "$work_dir/$PID-${BID}b"
unit_tests_file="$work_dir/$PID-${BID}b/unit_tests.txt"
relevant_tests="*"  # Note, you might want to consider the set of relevant tests provided by D4J, i.e., $D4J_HOME/framework/projects/$PID/relevant_tests/$BID

java -cp "$test_classpath:$test_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$GZOLTAR_CLI_JAR" \
  com.gzoltar.cli.Main listTestMethods \
    "$test_classes_dir" \
    --outputFile "$unit_tests_file" \
    --includes "$relevant_tests"
head "$unit_tests_file"

#
# Collect classes to perform fault localization on
# Note: the `sed` commands below might not work on BSD-based distributions such as MacOS.
#

cd "$work_dir/$PID-${BID}b"

loaded_classes_file="$D4J_HOME/framework/projects/$PID/loaded_classes/$BID.src"
normal_classes=$(cat "$loaded_classes_file" | sed 's/$/:/' | sed ':a;N;$!ba;s/\n//g')
inner_classes=$(cat "$loaded_classes_file" | sed 's/$/$*:/' | sed ':a;N;$!ba;s/\n//g')
classes_to_debug="$normal_classes$inner_classes"
echo "Likely faulty classes: $classes_to_debug" >&2

#
# Run GZoltar
#

cd "$work_dir/$PID-${BID}b"

ser_file="$work_dir/$PID-${BID}b/gzoltar.ser"
java -XX:MaxPermSize=4096M -javaagent:$GZOLTAR_AGENT_JAR=destfile=$ser_file,buildlocation=$src_classes_dir,includes=$classes_to_debug,excludes="",inclnolocationclasses=false,output="FILE" \
  -cp "$src_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$test_classpath:$GZOLTAR_CLI_JAR" \
  com.gzoltar.cli.Main runTestMethods \
    --testMethods "$unit_tests_file" \
    --collectCoverage

#
# Generate fault localization report
#

cd "$work_dir/$PID-${BID}b"

java -cp "$src_classes_dir:$D4J_HOME/framework/projects/lib/junit-4.11.jar:$test_classpath:$GZOLTAR_CLI_JAR" \
    com.gzoltar.cli.Main faultLocalizationReport \
      --buildLocation "$src_classes_dir" \
      --granularity "line" \
      --inclPublicMethods \
      --inclStaticConstructors \
      --inclDeprecatedMethods \
      --dataFile "$ser_file" \
      --outputDirectory "$work_dir/$PID-${BID}b" \
      --family "sfl" \
      --formula "ochiai:Ochiai2:Meco:Tarantula:Barinel:Opt:DStar:Sgf_1:Sgf_2:Fo1:Fo2:Fo3:Fo4:Fo5:Fo6:Fo7:Fo8:Fo9:Fo10:Fo12:Fo13:Fo14:Fo15:Fo16:Fo17:Fo19:Fo20:Fo21:Fo22" \
      --metric "entropy" \
      --formatter "txt"
