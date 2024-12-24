# invoke_script.py
import subprocess

# Checkout Closure-27, compile it, and get its metadata
trial= {'Collections':'28'}
v1 = {'Chart':'26', 'Time':'27', 'Lang':'65', 'Mockito':'38', 'Math':'106', 'JxPath':'22','Closure':'176'}
v2={'Chart':'26', 'Time':'27', 'Lang':'65', 'Mockito':'38','Collections':'28', \
    'Codec':'18', 'Csv':'16', 'Cli':'40', 'Math':'106', 'JxPath':'22', \
          'Jsoup':'93', 'JacksonXml':'6','JacksonDatabind':'112', 'JacksonCore':'26',\
              'Gson':'18', 'Compress':'47', 'Closure':'176'}
for p in v2:
    PID=p
    BID=int(v2[p])
    for e in range(1, BID+1):
        e=f'{e}'
        command='./get_buggy_lines.sh '+p+' '+e+ ' '+ 'Bugggasssa'
        process = subprocess.run(command, shell=True)
        print(process)
    
