import pandas as pd
import re
import numpy as np

fl_metric=False 
#True for top_n while False for wasted_effort

check='raw' 
#'raw' for raw analysis and 'processed' to remove elements with zero and constraints to top 1000 elements

metric=['barinel','dstar', 'jaccard','meco','ochiai', 'ochiai2','opt','tarantula','sgf_1','sgf_2','fo1','fo2','fo3','fo4','fo5','fo6','fo7','fo8','fo9','fo10','fo12','fo13','fo14','fo15','fo16','fo17','fo19','fo20','fo21', 'fo22']
metrics=['barinel','dstar', 'jaccard','meco','ochiai', 'ochiai2','opt','tarantula','sgf_1','sgf_2','fo7','fo17']
# The formulas considered for the analysis

# The selected projects for the analysis
trial= {'Lang':'65'}
# D4J v1 and 2
trial= {'Lang':'65', 'Chart':'26', 'Time':'26', 'Mockito':'38',  'Math':'106','Jsoup':'93','Compress':'47'}
trial1={'Lang':'65', 'Chart':'26', 'Time':'26','Mockito':'38',  'Math':'106', \
    'Collections':'28', 'Codec':'18', 'Csv':'16', 'Cli':'39', 'JxPath':'22','Jsoup':'93',\
    'JacksonXml':'6','JacksonDatabind':'112','JacksonCore':'26','Gson':'18','Compress':'47'}

def fileResult(table, metric):
    fil = f"SBFL_Formula_Generation/topn_{check}_result.csv" if fl_metric else f"SBFL_Formula_Generation/ewe_{check}_result.csv"
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
            line1 +=number        
            #print(f'Buggy Line {e}-{line1}')
            buglist.append(line1)
            
    return buglist
    f.close
    print(f'We did not pray for this: {x}')
    return line
        

        #  ls is csv file of elements and suspiciousness from Gzoltar fl reports while 
        # bugl is the buglines is the range of bug lines extracted from D4J patch
def splitListContent(ls, buglines, assessor):
    
    #
    nList=[]

    #to track class granularity suspisiousness 
    class_notifier=0
    for x,i in ls.iterrows():
        #keep track of index
        nList.append(x)

        i = i['name']
        
        # separator for the elements from Gzoltar coverage info; statement url and line number
        if ':' in i:
            # key is the url containing some special characters
            # value is the line number 
            key, value = i.split(':')
            
            # replace $ in key to conform with url generated from D4J patch file
            key= key.translate(str.maketrans('$','.'))

            #split key using # delimiter and rejoin the first item with value for comformity with items in buggyline 
            key=key.split('#')[0]
            element = f'{key}:{value}'
            
                     
            # check if the current element is in the list of buggyline
            if element in buglines:
                total_executable_elements = 1
                total_executable_elements=len(ls)
                #tie_element=ls[ls['rank']==ls.at[x, 'rank']]
                
                rank=ls.at[x, 'rank']
               
                exam_score=100*rank/total_executable_elements
                #print(f'ExamScore: {exam_score}')
                
                #return top_n if assessor is true else return wasted effort
                #the choice of rank or serial depends on the arbitary defn of top_n
                #'serial' give the exact location of statement while 
                # rank give the rank of an statement based on average ranking formula as in Wang et al.(2022)
                #print (f'{ls.at[x, 'serial']-1} : {nList.index(x)}')

                return ls.at[x, 'rank'] if assessor else exam_score
                return nList.index(x) if assessor else 100*nList.index(x)/total_executable_elements
            
            for bugl in buglines:
                url, no =bugl.split(':')
                # create range of buggy lines 
                
                if url == key and class_notifier==0:
                    class_notifier=ls.at[x, 'rank'] if assessor else 'C'

                    
                    #for class granularity return f'Success Match'
                    # To improve the localization to cover range of lines 
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
                        df.replace([np.inf, -np.inf], [-100000,-100000], inplace=True)
                    if abs(df.loc[x, "suspiciousness_value"])==0 and check=='processed':
                        #df.drop(df.loc[x])
                        df.replace(0, -10000, inplace=True)
                        
                        
                        
                df.insert(0,"rank", df['suspiciousness_value'].rank(ascending=False, method='dense', na_option='bottom'))
                df.sort_values(by='rank', inplace= True, ascending=True)       
                #df['serial'] = range(1, len(df) + 1)
                df.insert(0,'serial',range(1, len(df) + 1))
                #print (df)
                #df.dropna()
            
                if check=='processed':
                    df.dropna()
                
                
                score = splitListContent(df, buggy_line, fl_metric)
                
                
                
                
                result.append(score)
                if fl_metric:
                    print(f'{p}-{e}-{m} Bug is Located and rank at:{score}')
                else:
                    print(f'{p}-{e}-{m} Bug Exam_Score is:{score}')

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
    
