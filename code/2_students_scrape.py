import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import itertools
import pandas as pd
import datetime
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

def scraper(ids):

    print('# of ids: ' + str(len(ids)))
    df_list = []

    time_start = datetime.datetime.now()
    #df_dissert_advisor = pd.DataFrame([], columns=["id", "dissertation", "advisor"])

    n = len(ids)
    for i in range(n):

        if (i > 0) & (i % 20 == 0):
                print(i)
                time_elapsed = datetime.datetime.now() - time_start
                print('time elapsed: '+str(time_elapsed))
                print('estimated time remaining: '+ str(time_elapsed*(n-i)/20))
                time_start = datetime.datetime.now()

        url = 'https://www.genealogy.math.ndsu.nodak.edu/id.php?id=' + str(ids[i])
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table')
        if table:    
            table_rows = table.find_all('tr')
            res = []
            for tr in table_rows:
                td = tr.find_all('td')
                row = [tr for tr in td]
                if row:
                    res.append(row)

            df_math = pd.DataFrame(res, columns=["Mathematician", "School", "Year", "Descendants"])
            df_math['id'] = ids[i]
        else:
            df_math = pd.DataFrame([], columns=["Mathematician", "School", "Year", "Descendants",'id'])

        # ID, Dissertation, Advisor     
        # dissertation = soup.find_all('span', attrs={'id':'thesisTitle'})
        #advisor = soup.find_all('p', attrs={'style':'text-align: center; line-height: 2.75ex'})

        # df_dissert_advisor.loc[i,"id"] = ids[i]
        # df_dissert_advisor.loc[i,"dissertation"] = [i for i in dissertation[0]]
        # df_dissert_advisor.loc[i,"advisor"] = advisor

        df_list.append(df_math)
    
    df_output = pd.concat(df_list,axis=0).reset_index(drop=True)
    return(df_output)

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

# Load IDs
df = pd.read_csv('mathematicians.csv')
ids = df['id'].unique()

chunks = divide_chunks(ids,50000)
chunks_list = [x for x in chunks]

for i in range(len(chunks_list)):

    # Parallelize Scraping
    chunks = divide_chunks(chunks_list[i],200)
    pool = Pool(cpu_count() * 2)
    results = pool.map(scraper, chunks)
    pool.close()

    df_final = pd.concat(results,axis=0).reset_index(drop=True)

    df_final.to_csv('students'+str(i)+'.csv', index=False)   