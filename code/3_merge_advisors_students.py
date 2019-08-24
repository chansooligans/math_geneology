import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import itertools
import pandas as pd
import datetime
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

# Students
files = ['students0.csv',
         'students1.csv',
         'students2.csv',
         'students3.csv',
         'students4.csv']
df_list = [pd.read_csv(file) for file in files]
df = pd.concat(df_list, axis = 0)
df = df.reset_index(drop=True)

df['student_id'] = [x.split('?id=')[1].split('">')[0] for x in df['Mathematician']]
df['student_name'] = [x.split(">")[2].split("<")[0] for x in df['Mathematician']]
df['student_school'] = [BeautifulSoup(x).text for x in df['School']]
df['student_year'] = [BeautifulSoup(x).text for x in df['Year']]
df['student_descendants'] = [BeautifulSoup(x).text for x in df['Descendants']]

df_students = df[['id','student_id','student_name','student_school','student_year','student_descendants']]

# Advisors
df_advisors = pd.read_csv('mathematicians.csv')
df_advisors = df_advisors[['Mathematician', 'School', 'Year', 'id']]
df_advisors.rename({'Mathematician':'advisor_name',
                    'School':'advisor_school',
                    'Year':'advisor_year'},
                  axis=1,
                  inplace=True)

# Merged
df_final = df_students.merge(df_advisors, on = 'id', how = 'left')
df_final.to_csv('math_geneology_final.csv')