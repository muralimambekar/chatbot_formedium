#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 04:00:20 2020

@author: murali
"""
class webscrap:
    def webscrap():
        import pandas as pd
        import seaborn as sns
        import requests 
        from bs4 import BeautifulSoup 
        # offical ministry of health website
        url = 'https://www.mohfw.gov.in/' 
        
        # make a GET request to fetch the raw HTML content
        web_content = requests.get(url).content
        
        # parse the html content
        soup = BeautifulSoup(web_content, "html.parser")
        
        # remove any newlines and extra spaces from left and right
        extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
        
        stats = [] # initialize stats
        all_rows = soup.find_all('tr') # find all table rows 
        
        for row in all_rows: 
            stat = extract_contents(row.find_all('td')) # find all data cells  
            # notice that the data that we require is now a list of length 5
            if len(stat) == 6: 
                stats.append(stat)
        
        # convert the data into a pandas dataframe and then to list for further processing
        new_cols = ["Sr.No", "States/UT","Active Cases","Recovered", "Deaths", "Confirmed",]
        state_data = pd.DataFrame(data = stats, columns = new_cols)
        state_data1=state_data.drop(['Sr.No'], axis=1)
        state_dic=state_data1.to_dict ("records")
        
        #Converting to list
        state=[state_data.columns.values.tolist()] + state_data.values.tolist()    
        return state, state_dic

