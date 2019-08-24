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

    n = len(search_alph)
    
    print('total # of searches: '+str(n))
    
    # Initialize DataFrame to store results
    df_results = pd.DataFrame({'search_alph':search_alph})
    df_results['too_many_math'] = None
    df_results['zero_math'] = None

    # Start Scraping
    time_start = datetime.datetime.now()
    for i in range(n):

        if (i > 0) & (i % 40 == 0):
            print(i)
            time_elapsed = datetime.datetime.now() - time_start
            print('time elapsed: '+str(time_elapsed))
            print('estimated time remaining: '+ str(time_elapsed*(n-i)/40))
            time_start = datetime.datetime.now()

        # Scrape html
        url = 'https://www.genealogy.math.ndsu.nodak.edu/letter.php?letter=' + search_alph[i]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.findAll('p')

        # Check if there are too many results or if there are no results
        df_results.loc[i,'too_many_math'] = "too large to be displayed" in str(text[1])
        df_results.loc[i,'zero_math'] = "There are 0 mathematicians" in str(text[1])
    
    return(df_results)

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 


df_list = []
too_many_math_sum = 1
alph_plus_apostrophe = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',"'"]
df_res_temp = None

while too_many_math_sum > 0:
    
    # New Alphabets to Search
    if df_res_temp is None:
        new_alph = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    else:
        new_alph = df_res_temp.loc[df_res_temp['too_many_math'] == True,'search_alph']        
    
    # Grid to search
    search_alph = [x for x in map(''.join, itertools.product(new_alph,alph_plus_apostrophe))]
    
    # Parallelize Scraping
    chunks = divide_chunks(search_alph,200)
    pool = Pool(cpu_count() * 2)
    results = pool.map(scraper, chunks)
    pool.close()
    df_res_temp = pd.concat(results,axis=0).reset_index(drop=True)
    print(df_res_temp.head())
    too_many_math_sum = sum(df_res_temp['too_many_math'])

    print('# of permutations with too_many_math: '+str(too_many_math_sum))
    
    # Add to list of results
    df_list.append(df_res_temp)
    
df_res = pd.concat(df_list,axis=0).reset_index(drop=True)

df_res.to_csv('math_geneology_search.csv',index=False)