import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import itertools
import pandas as pd
import datetime
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

def scraper(search_alph):
    
    df_list = []
    n=len(search_alph)
    time_start = datetime.datetime.now()
    
    for i in range(n):

        print(i)
        time_elapsed = datetime.datetime.now() - time_start
        print('time elapsed: '+str(time_elapsed))
        print('estimated time remaining: '+ str(time_elapsed*(n-i)/20))
        time_start = datetime.datetime.now()
        
        url = 'https://www.genealogy.math.ndsu.nodak.edu/letter.php?letter=' + search_alph[i] + '&fShow=1'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get table of mathematicians
        table = soup.find('table')
        table_rows = table.find_all('tr')

        # Get IDs
        text = soup.find_all('a', href=True)

        res = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text.strip() for tr in td]
            if row:
                res.append(row)

        df_math = pd.DataFrame(res, columns=["Mathematician", "School", "Year"])
        df_math['id'] = [x['href'].split('=')[1] for x in text if 'id.php?id' in x['href']]        
        df_list.append(df_math)
    
    df_final = pd.concat(df_list,axis=0).reset_index(drop=True)
    
    return(df_final) 


alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


# Parallelize Scraping
chunks = divide_chunks(alphabet,4)
pool = Pool(cpu_count() * 2)
results = pool.map(scraper, chunks)
pool.close()

df_output = pd.concat(results,axis=0).reset_index(drop=True)

df_output.to_csv('mathematicians.csv', index=False)