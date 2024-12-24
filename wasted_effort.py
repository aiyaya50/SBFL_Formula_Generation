import pandas as pd
import re
# The formulas considered for the analysis
metric=['ochiai', 'ochiai2', 'tarantula','barinel','opt','dstar', 'yaya','fo1','fo2','fo3','fo4','fo5','fo6','fo7','fo8','fo9','fo10','fo11','fo12','fo13','fo14','fo15','fo16','fo17','fo18','fo19','fo20','fo21', 'fo22']

# The selected projects for the analysis
trial= {'Chart':'26', 'Time':'27','Mockito':'38'}
# D4J v1 and 2
trials = {'Chart':'26', 'Time':'27','Mockito':'38', 'JxPath':'22',\
         'Collections':'28', 'Codec':'18', 'Csv':'16', 'Cli':'40', 'Math':'106',\
      'Jsoup':'93', 'JacksonXml':'6','JacksonDatabind':'112', 'JacksonCore':'26', 'Gson':'18',\
          'Compress':'47'}
def fileResult(table, metric):
    f = open("we_result.csv", "w", encoding='utf-8', errors='replace')
    f.write("metrics:\t")
    for e in metric:
        f.write(f'{e}\t')
    f.write('\n')
    f.close()

    f = open("we_result.csv", "a", encoding='utf-8', errors='replace')
    for e in table:
        for x in e:
            f.write(f'{x}\t')
        f.write('\n')
    f.close()
    print('Congratulationssss')

#Fecth bug location from the projects active bug csv file
# Split elements of a list/df with : separator 
# and search the new elements at the second index 
#for location of bug 
def splitItem(item, separator):
    if separator in item:
            key, value = item.split(separator)
            return value
    else:
        return item

def findBuggyLine(dir):
    f = open(dir, "r")
    line='not'
    nList=[]
    for x in f:
        
        if '---' in x:
            # line= x
            # clean and prepare the bug line to conform with the Gzoltar naming
            line= x.translate(str.maketrans({'/':'.', '-':''}))
            line=re.sub('.java',':', line)
            line=re.sub('a.src.|a.source.|a.src.main:.|main:.','', line.strip())
            
        if '@@' in x:
            # prepare the range of buggy line to append to the bug url
            # line2= line2.replace("@","")
            line+=re.sub('[a-z|A-Z|@|-]','', x).split('+')[0].strip()
                     
            print(f'Buggy Line{line}')
            return (line)
    f.close
    print(f'We did not pray for this: {x}')
    return line
        

        #  ls is list of url from Gzoltar fl reports while 
        # bugl is the bugl is the range of bug lines extracted from D4J patch
def splitListContent(ls, bugl):
    nList=[]
    for i in ls:
        # if id in i:
        #     print('congrats')

        if ':' in i:
            # separator for the Gzoltar reported buggy_line url and line number
            if ':' in i:
                # key is the url containing some special characters
                # value is the line number 
                key, value = i.split(':')
                
                # key is the url containing some special characters
                # replace $ in key to conform with url generated from D4J patch file
                key= key.translate(str.maketrans('$','.'))
                key=key.split('#')[0]
                element = f'{key}:{value}'
                
                nList.append(element)
                
                # split D4J bugl into url and line no
                url, no =bugl.split(':')

                # create range of buggy lines 
                ranj = no.split(',')
                
                if len(ranj)>1:
                    a, b = ranj
                    # print(f'{int(value) in range(int(a),int(a)+int(b)+1, 1)} {a}-{value}-{key}')
                   
                if url == key:
                    #for class granularity return f'Success Match'
                    # To improve the localization to cover range of lines 
                    # if value in range (int(no.split(',')[0]), int(no.split(',')[1])+1, 1):
                    if (int(value) in range(int(a),int(a)+int(b)+1, 1)):
                                           
                        print(int(value.strip()) in range(int(a),int(a)+int(b)+1, 1))
                        element = f'{key}:{value.strip()}'
                        return nList.index(element)+1
                    else:
                        return 'C'
                # print(f'{key}-{bugl.split(':')[0]}')

    # print (nList)
    if bugl.split(':')[0] in nList:
        return f'Localized at TOP_{nList.index(id)+1}'
    else:
        return 0
# iterate the selected projects
table=[]
for p in trial:
    PID=p
    BID=int(trial[p])
    # obtain the buggy_line
    bug_location=''
     
    print(f'%%%%{p}%%%%')
    
    # iterate the bugs in each project
    
    for e in range(1, BID+1):
        bug_location=f'/home/aiyaya50/defects4j/framework/projects/{p}/patches/'
        bug_location+=f'/{e}.src.patch'
        buggy_line=findBuggyLine(bug_location)
        
        c=f'{p}-{e}'
        result=[]
        result.append(c)
        
        # iterate through the results of each formula per bug 
        for m in metric:
            
            #e=f'{e}' print(df)print(f'Buggy line at:{buggy_line}')
            dir=f'/home/aiyaya50/Bugs/{PID}-{e}b/sfl/txt/{m}.ranking.csv'
            try:
                df= pd.read_csv(dir, sep=';', dtype=object)
                # df= df['suspiciousness_value']
                #data cleaning
                          
                df=df[df['suspiciousness_value']!='0.0']
                df=df[df['suspiciousness_value']!='NaN']
                df=df[df['suspiciousness_value']!='']

                df.dropna(subset=['suspiciousness_value'], inplace = True)
                # df.info()
                # line=re.sub('a.src.|a.source.|a.src.main:.|main:.','', line.strip())
                
                df=df['name']
               
                
                # print (df)
                df=df[:500]
                score = splitListContent(df, buggy_line)
                result.append(score)
                print(f'{p}-{e}({buggy_line})-{m}%Located at Line:{score}')
                #print(df)
                '''exists =(df==buggy_line).any().any()
                print(f'{exists} {buggy_line}')'''
            except:
                print(f'Directory does not exist{KeyError}')
                '''
                '''
        table.append(result)       
print (table)
fileResult(table, metric)    
    