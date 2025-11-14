import pandas as pd
import re
import numpy as np

fl_metric=True 
#True for top_n while false for wasted_effort

check='raw' 
#raw for raw analysis and processed to remove elements with zero and constraints to top 1000 elements

metric=['ochiai', 'ochiai2', 'tarantula','barinel','opt','dstar', 'meco','sgf_1','sgf_2','fo1','fo2','fo3','fo4','fo5','fo6','fo7','fo8','fo9','fo10','fo12','fo13','fo14','fo15','fo16','fo17','fo19','fo20','fo21', 'fo22']
# The formulas considered for the analysis

# The selected projects for the analysis
trialsss= {'Lang':'65'}
# D4J v1 and 2
trial = {'Time':'26','Lang':'65', 'Chart':'26', 'Mockito':'38',  'Math':'106'}
tria12l={'Lang':'65', 'Chart':'26', 'Time':'26', 'Mockito':'38',  'Math':'106','Collections':'28', 'Codec':'18', 'Csv':'16', 'Cli':'39', 'Math':'106', 'JxPath':'22', \
          'Jsoup':'93', 'JacksonXml':'6','JacksonDatabind':'112', 'JacksonCore':'26', 'Gson':'18', 'Compress':'47'}

def fileResult(table, metric):
    fil = f"method_level/topn_{check}_method_result.csv" if fl_metric else f"method_level/ewe_{check}_method_result.csv"
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

def findBuggyClassAndMethod(dir):
    try:
        f = open(dir, "r", errors='ignore')
        #line='not'
        buglist=[]
        for x in f:
            if 'org' in x or 'com' in x:   
                buglist.append(x.strip()) 
        f.close
        return buglist
    except Exception as ef:
        print(f'Error: {ef}')
        return 'Na'

        #  ls is list of url from Gzoltar fl reports while 
        # bugl is the bugl is the range of bug lines extracted from D4J patch
def topNandWastedEffort(ls, bugMethods, assessor):
    
    print()
    nList=[]
    class_notifier=0
    for x,i in ls.iterrows():
        #print(f'index{x}')
        nList.append(x+1)

        i = i['name']
        if '#' in i:
            buggies = i.split('#')
            
            buggy_class, buggy_method = buggies[0], buggies[1]

            buggy_class= buggy_class.translate(str.maketrans('$','.'))
            buggy_method=buggy_method.split('(')[0]
            element = f'{buggy_class}, {buggy_method}'
            
                     
            # split D4J bugl into url and line no
           
            if element in bugMethods:
                #print('found')
                return ls.at[x, 'rank'] if assessor else nList.index(x-1)
                
            
            for bugl in bugMethods:
                url, met =bugl.split(',')
                # create range of buggy lines 
                
                if url == buggy_class and class_notifier==0:
                    class_notifier=ls.at[x, 'rank'] if assessor else nList.index(x)
                # if value in range (int(no.split(',')[0]), int(no.split(',')[1])+1, 1):
                                           
    if (class_notifier>0):
        return f'C-{class_notifier}'
    return 0    # print(f'{key}-{bugl.split(':')[0]}')

    
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
        # bug_location=f'/home/aiyaya50/defects4j/framework/projects/{p}/patches/'
        bug_location=f'/home/aiyaya50/buggy-methods/{p}-{e}_ext.buggy.methods'
        
        buggy_line=findBuggyClassAndMethod(bug_location)
        
        c=f'{p}-{e}'
        result=[]
        result.append(c)
        
        # iterate through the results of each formula per bug 
        for m in metric:

            dir=f'/home/aiyaya50/Bugs/{PID}-{e}b/sfl_method/sfl/txt/{m}.ranking.csv'
            try:
                df= pd.read_csv(dir, sep=';',  header=0, encoding='unicode_escape')
                
                # line=re.sub('a.src.|a.source.|a.src.main:.|main:.','', line.strip())
                df['suspiciousness_value'] = pd.to_numeric(df['suspiciousness_value'])
                for x in df.index:
                    if abs(df.loc[x, "suspiciousness_value"])==np.inf:
                        df.replace([np.inf, -np.inf], [np.nan,np.nan], inplace=True)
                    if abs(df.loc[x, "suspiciousness_value"])==0 and check=='processed':
                        #df.drop(df.loc[x])
                        df.replace([0, -0], [-1000,-1000], inplace=True)
                        
                       
                        
                df.insert(0,"rank", df['suspiciousness_value'].rank(ascending=False, method='dense', na_option='bottom'))
                df.sort_values(by='rank', inplace= True, ascending=True)       
                
                #print (df)
                if check=='processed':
                    df=df[:1000]
                score = topNandWastedEffort(df, buggy_line, fl_metric)
                result.append(score)
                print(f'{p}-{e}-{m} bug is Located and rank at:{score}')

            except Exception as ef:
                print(f'Directory does not exist: {ef}')
                
        table.append(result)       
print (table)
fileResult(table, metric)    
    
