# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:28:04 2020

@author: ABHIJIT SHOW
"""


from newsapi import NewsApiClient
from gtts import gTTS
import json
import re
from configparser import ConfigParser

def news_audio_save():
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")
    
    newsapi_cred = config_object["NEWS_API"]
    
    newsapi = NewsApiClient(api_key = newsapi_cred["api_key"])
    
    top_headlines_world = newsapi.get_top_headlines(q='coronavirus', language='en')
    top_headlines_india = newsapi.get_top_headlines(q='coronavirus', language='en', country='in')

    world_audio_locations = []
    count = 0
    for i in top_headlines_world["articles"]:
        count = count + 1
        language = 'en'
        name = re.split(',|-|:|\+|\.', i['publishedAt'])
        string = str(count) + '_'
        for j in name:
            string = string + j + str(top_headlines_world['totalResults'])
            
        if i["description"] == None:
            myobj = gTTS(text="Sorry no description of the news was available.", lang=language, slow=False)
            location = "static/audio/world_news_audio/audio_"+string+".mp3"
            myobj.save(location)
        else:
            myobj = gTTS(text=i["description"]+". by "+i["source"]["name"], lang=language, slow=False)
            location = "static/audio/world_news_audio/audio_"+string+".mp3"
            myobj.save(location)
        
        world_audio_locations = world_audio_locations + [location]
        
    with open('json_data/world_news_audio_locations.json', 'w') as json_file:
        json.dump(world_audio_locations, json_file)
            
    india_audio_locations = []
    count = 0
    for i in top_headlines_india["articles"]:
        count = count + 1
        language = 'en'
        name = re.split(',|-|:|\+|\.', i['publishedAt'])
        string = str(count) + '_'
        for j in name:
            string = string + j + str(top_headlines_india['totalResults'])
        if i["description"] == None:
            myobj = gTTS(text="Sorry no description of the news was available.", lang=language, slow=False)
            location = "static/audio/india_news_audio/audio_"+string+".mp3"
            myobj.save(location)
        else:
            myobj = gTTS(text=i["description"]+". by "+i["source"]["name"], lang=language, slow=False)
            location = "static/audio/india_news_audio/audio_"+string+".mp3"
            myobj.save(location)
        
        india_audio_locations = india_audio_locations + [location]
        
    with open('json_data/india_news_audio_locations.json', 'w') as json_file:
        json.dump(india_audio_locations, json_file)
    
    with open('json_data/news_world.json', 'w') as json_file:
        json.dump(top_headlines_world, json_file)
        
    with open('json_data/news_india.json', 'w') as json_file:
        json.dump(top_headlines_india, json_file)
        
def global_news():
    with open('json_data/news_world.json') as file:
        news = json.load(file)
        
    with open('json_data/world_news_audio_locations.json') as file:
        audio_locations = json.load(file)
        
    global_news_list = []
    for i in news["articles"]:
        global_news_list.append({"source":i["source"]["name"],
                                 "title":i["title"],"description":i["description"],
                                 "image_url":i["urlToImage"],"url":i["url"]})

    return global_news_list + [{"audio_locations":list(audio_locations)}]
    
def india_news():
    with open('json_data/news_india.json') as file:
        news = json.load(file)
        
    with open('json_data/india_news_audio_locations.json') as file:
        audio_locations = json.load(file)
        
    india_news_list = []
    for i in news["articles"]:
        india_news_list.append({"source":i["source"]["name"],
                                "title":i["title"],"description":i["description"],
                                "image_url":i["urlToImage"],"url":i["url"]})

    return india_news_list + [{"audio_locations":list(audio_locations)}]

#news_audio_save()