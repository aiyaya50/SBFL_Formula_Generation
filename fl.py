# invoke_script.py
import subprocess

# Checkout Closure-27, compile it, and get its metadata
trial= {'Time':'27'}
v1 = {'Chart':'26', 'Time':'27', 'Lang':'65', 'Mockito':'38', 'Math':'106', 'JxPath':'22','Closure':'176'}
v2={'Collections':'28', 'Codec':'18', 'Csv':'16', 'Cli':'40', 'Math':'106', 'JxPath':'22', \
          'Jsoup':'93', 'JacksonXml':'6','JacksonDatabind':'112', 'JacksonCore':'26', 'Gson':'18', 'Compress':'47'}
for p in trial:
    PID=p
    BID=int(trial[p])
    for e in range(1, BID+1):
        e=f'{e}'
        command='echo PID='+PID+'>f.sh;echo BID='+e+'>>f.sh;cat run.sh >> f.sh;sh f.sh'
        process = subprocess.run(command, shell=True)
        print(process)
    
