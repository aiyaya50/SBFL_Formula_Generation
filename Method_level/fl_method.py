# invoke_script.py
import subprocess

# Checkout Closure-27, compile it, and get its metadata

trial = { 'Lang':'65', 'Math':'106', 'Chart':'26', 'Time':'28', 'Mockito':'38'}
trial={'Collections':'28', 'Codec':'18', 'Csv':'16', 'Cli':'40','JxPath':'22', \
          'Jsoup':'93', 'JacksonXml':'6','JacksonDatabind':'112', 'JacksonCore':'26', 'Gson':'18', 'Compress':'47'}

for p in trial:
    PID=p
    BID=int(trial[p])
    for e in range(1, BID+1):
        e=f'{e}'
        try:
            command='echo PID='+PID+'>f.sh;echo BID='+e+'>>f.sh;cat run_methods.sh >> f.sh;sh f.sh'
            process = subprocess.run(command, shell=True)
            print(process)
        except:
            print(f"Error Processing {PID}-{e}")
    
