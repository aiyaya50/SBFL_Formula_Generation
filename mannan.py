import pandas as pd
import re
import numpy as np

fl_metric=False 
#True for top_n while false for wasted_effort

check='raw' 
#raw for raw analysis and processed to remove elements with zero and constraints to top 1000 elements

metric=['ochiai', 'ochiai2', 'tarantula','barinel','opt','dstar', 'meco','sgf_1','sgf_2','fo1','fo2','fo3','fo4','fo5','fo6','fo7','fo8','fo9','fo10','fo12','fo13','fo14','fo15','fo16','fo17','fo19','fo20','fo21', 'fo22']
# The formulas considered for the analysis

# The selected projects for the analysis
trialsss= {'Lang':'65'}
# D4J v1 and 2
trialsss = {'Chart':'26', 'Time':'26', 'Mockito':'38',  'Math':'106'}
trial={'Lang':'65', 'Chart':'26', 'Time':'26', 'Mockito':'38',  'Math':'106','Collections':'28', 'Codec':'18', 'Csv':'16', 'Cli':'39', 'Math':'106', 'JxPath':'22', \
          'Jsoup':'93', 'JacksonXml':'6','JacksonDatabind':'112', 'JacksonCore':'26', 'Gson':'18', 'Compress':'47'}

def fileResult(table, metric):
    fil = f"topn_{check}_result.csv" if fl_metric else f"we_{check}_result.csv"
    f = open(fil, "w")
    f.write("metrics:\t")
    for e in metric:
        f.write(f'{e}\t')
    f.write('\n')
    f.close()

    f = open(fil, "a")
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
    f = open(dir, "r", errors='ignore')
    line='not'
    buglist=[]
    for x in f:
        
        if 'org' in x or 'com' in x:
            # line= x
            # clean and prepare the bug line to conform with the Gzoltar naming
            line= x.translate(str.maketrans({'/':'.', '-':''}))
            line=re.sub('.java',':', line)
            line=re.sub('a.src.|a.source.|#|a.src.main:.|main:.','@', line.strip())    
            # prepare the range of buggy line to append to the bug url
            # line2= line2.replace("@","")
            line1=line.split('@')[0].strip()
            number=line.split('@')[1].strip()
            #line+=re.sub('[a-z|A-Z|@|-]','', x).split('#')[1].strip()
            line1 +=number        processed

        #  ls is list of url from Gzoltar fl reports while 
        # bugl is the bugl is the range of bug lines extracted from D4J patch
def splitListContent(ls, buglines, assessor):
    
    #print(buglines)
    nList=[]
    class_notifier=0processed
    for x,i in ls.iterrows():
        #print(f'index{x}')
        nList.append(x)
        i = i['name']
        #print (rank)

        # if id in i:
        #     print('congrats')

        
            # separator for the Gzoltar reported buggy_line url and line number
        if ':' in i:
            # key is the url containing some speciaprocessedl characters
            # value is the line number 
            key, value = i.split(':')
            
            # key is the url containing some special characters
            # replace $ in key to conform with url processed'))
            key=key.split('#')[0]
            element = f'{key}:{value}'
            
                     
            # split D4J bugl into url and line no
           
            if element in buglines:
                #print(f'in chunk{element in buglines}')
                return ls.at[x, 'rank'] if assessor else nList.index(x) 
                
            
            for bugl in buglines:
                url, no =bugl.split(':')
                # create range of buggy lines 
                
                if url == key and class_notifier==0:
                    class_notifier=ls.at[x, 'rank'] if assessor else nList.index(x) 

                    
                    #for class granularity return f'Success Match'
                    # To improve the localization to cover range of lines 
                    # if value in range (int(no.split(',')[0]), int(no.split(',')[1])+1, 1):
                    
                       
                          
    if (class_notifier>0):
        return f'C-{class_notifier}'
    return 0    # print(f'{key}-{bugl.split(':')[0]}')

    
# iterate the selected projectsgenerated from D4J patch file
            key= key.translate(str.maketrans('$','.
table=[]
for p in trial:
    PID=p
    BID=int(trial[p])
    # obtain the buggy_line
    bug_location=''
     
    print(f'%%%%{p}%%%%')
    
    # iterate the bugs in each project
    
    for e in range(1, BID+1):
        # bug_location=f'/home/aiyaya50/defects4j/framework/projects/{p}/patches/'
        bug_location=f'/home/aiyaya50/buggy_statements/{p}-{e}.buggy.lines'
        
        buggy_line=findBuggyLine(bug_location)
        
        c=f'{p}-{e}'
        result=[]
        result.append(c)
        
        # iterate through the results of each formula per bug 
        for m in metric:
            
            #e=f'{e}' print(df)print(f'Buggy line at:{buggy_line}')
            #dir=f'/media/aiyaya50/08F4-864B/Bugs/{PID}-{e}b/sfl/txt/{m}.ranking.csv'
            dir=f'/home/aiyaya50/Bugs/{PID}-{e}b/sfl/txt/{m}.ranking.csv'
            try:
                df= pd.read_csv(dir, sep=';',  header=0, encoding='unicode_escape')
                # df= df['suspiciousness_value']
                #data cleaning
                          
               

                #print (df)
                # df.info()
                # line=re.sub('a.src.|a.source.|a.src.main:.|main:.','', line.strip())
                df['suspiciousness_value'] = pd.to_numeric(df['suspiciousness_value'])
                for x in df.index:
                    if abs(df.loc[x, "suspiciousness_value"])==np.inf:
                        df.replace([np.inf, -np.inf], [np.NaN,np.NaN], inplace=True)
                    if abs(df.loc[x, "suspiciousness_value"])==0 and check=='processed':
                        #df.drop(df.loc[x])
                        df.replace([0, -0], [np.NaN,np.NaN], inplace=True)
                        
                       
                        
                df.insert(0,"rank", df['suspiciousness_value'].rank(ascending=False, method='dense', na_option='bottom'))
                df.sort_values(by='rank', inplace= True, ascending=True)       
                
                #print (df)
                if check=='processed':
                    df=df[:1000]
                
                
                score = splitListContent(df, buggy_line, fl_metric)
                
                
                
                
                result.append(score)
                print(f'{p}-{e}-{m} bug is Located and rank at:{score}')

                #df.to_csv(f'/home/aiyaya50/uranking/{p}{e}{m}.csv')
                # print(f'{p}-{e}({buggy_line})-{m}%Located at Top_:{top}')
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
    
