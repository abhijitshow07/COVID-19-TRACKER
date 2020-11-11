# -*- coding: utf-8 -*-
"""
Created on Mon May  4 15:13:11 2020

@author: ABHIJIT SHOW
"""

import requests
import json
import calendar

def get_time_series():
    response = requests.get("https://disease.sh/v3/covid-19/countries")
    live_data = json.loads(response.text)
    
    long_string = ''
    for i in live_data:
        long_string = long_string + ',' + str(i['country'])
    long_string = long_string[1:]
    
    response = requests.get("https://corona.lmao.ninja/v3/covid-19/historical/"+long_string+"?lastdays=all")
    hist_data = json.loads(response.text)
    
    dates = list(hist_data[0]['timeline']['cases'].keys())
    
    data_sequence = []
    for i in dates[::3]:
        data = []
        date_split = i.split('/')
        new_date = date_split[1]+ ' '+ calendar.month_abbr[int(date_split[0])] + ' 20'+ date_split[2]
        for j in range(len(hist_data)):
            if list(hist_data[j].keys())[0] != 'message':
                if hist_data[j]["timeline"]["cases"][i] != 0:
                    data.append({"code3":live_data[j]["countryInfo"]["iso3"],
                                 "code":live_data[j]["countryInfo"]["iso2"],
                                 "name":live_data[j]["country"],
                                 "value":hist_data[j]["timeline"]["cases"][i]})
        data_sequence.append({"name":new_date,"data":data})
        
    with open('json_data/world_time_series.json', 'w') as json_file:
        json.dump(data_sequence, json_file)
        
#get_time_series()