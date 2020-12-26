# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:10:38 2020

@author: ABHIJIT SHOW
"""


import tweepy
import re
from textblob import TextBlob
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import time
from configparser import ConfigParser
import os

def tweet():

    #clear the contents of wordcloud folder
    clear_folder()

    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")
    
    twitter_cred = config_object["TWITTER"]
    
    access_token = twitter_cred["access_token"]
    access_token_secret = twitter_cred["access_token_secret"]
    consumer_key = twitter_cred["consumer_key"]
    consumer_secret = twitter_cred["consumer_secret"]
    
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # Create API object
    api = tweepy.API(auth)
    
    tweets = api.search(q=["coronavirus","covid19"], lang="en", count=100, tweet_mode = 'extended',
                        result_type = "recent")

    tweets_list = []
    sentences = []
    count = 0
    for tweet in tweets:
        count = count + 1
        clean_tweet = tweet.full_text
        clean_tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', clean_tweet)
        clean_tweet = re.sub("(@[A-Za-z0-9_]+)","", clean_tweet)
        sentences.append(clean_tweet[5:])
        if TextBlob(clean_tweet).sentiment.polarity > 0:
            testimonial = "Positive"
        elif TextBlob(clean_tweet).sentiment.polarity == 0:
            testimonial = "Neutral"
        elif TextBlob(clean_tweet).sentiment.polarity < 0:
            testimonial = "Negative"  
        tweets_list.append({"count":count,"name":tweet.user.name,"tweet":clean_tweet,
                            "tweet_sentiment":testimonial})
            
    papers = pd.DataFrame(sentences)
    papers.columns=['paper_text_processed']
    
    # Convert the titles to lowercase
    papers['paper_text_processed'] = papers['paper_text_processed'].map(lambda x: x.lower())
    
    # Join the different processed titles together.
    long_string = ','.join(list(papers['paper_text_processed'].values))

    #Create set of Stopwords
    stopwords = set(STOPWORDS)

    # Create a WordCloud object
    word_cloud = WordCloud(stopwords=stopwords, background_color="white", max_words=5000, contour_width=3, 
                           contour_color='steelblue',width = 1000,height = 600)
    # Generate a word cloud
    word_cloud.generate(long_string)
    # Visualize the word cloud
    location = "static/img/wordcloud/wordcloud" + str(int(time.time()*1000000)) + ".png"
    word_cloud.to_file(location)
        
    return [{"image_location":location}] + tweets_list

def india_tweet():
    #clear the contents of wordcloud folder
    clear_folder()

    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")
    
    twitter_cred = config_object["TWITTER"]
    
    access_token = twitter_cred["access_token"]
    access_token_secret = twitter_cred["access_token_secret"]
    consumer_key = twitter_cred["consumer_key"]
    consumer_secret = twitter_cred["consumer_secret"]
    
    
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # Create API object
    api = tweepy.API(auth)
    
    tweets = api.search(q=["coronavirus","covid19"], lang="en", count=100, tweet_mode = 'extended',
                        result_type = "recent",geocode="21.7679,78.8718,1400km")

    tweets_list = []
    sentences = []
    count = 0
    for tweet in tweets:
        count = count + 1
        clean_tweet = tweet.full_text
        clean_tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', clean_tweet)
        clean_tweet = re.sub("(@[A-Za-z0-9_]+)","", clean_tweet)
        sentences.append(clean_tweet[5:])
        if TextBlob(clean_tweet).sentiment.polarity > 0:
            testimonial = "Positive"
        elif TextBlob(clean_tweet).sentiment.polarity == 0:
            testimonial = "Neutral"
        elif TextBlob(clean_tweet).sentiment.polarity < 0:
            testimonial = "Negative"  
        tweets_list.append({"count":count,"name":tweet.user.name,"tweet":clean_tweet,
                            "tweet_sentiment":testimonial})
        
    papers = pd.DataFrame(sentences)
    papers.columns=['paper_text_processed']
    
    # Convert the titles to lowercase
    papers['paper_text_processed'] = papers['paper_text_processed'].map(lambda x: x.lower())
    
    # Join the different processed titles together.
    long_string = ','.join(list(papers['paper_text_processed'].values))

    #Create set of Stopwords
    stopwords = set(STOPWORDS)

    # Create a WordCloud object
    word_cloud = WordCloud(stopwords=stopwords, background_color="white", max_words=5000, contour_width=3, 
                           contour_color='steelblue',width = 1000,height = 600)
    # Generate a word cloud
    word_cloud.generate(long_string)
    # Visualize the word cloud
    location = "static/img/wordcloud/wordcloud" + str(int(time.time()*1000000)) + ".png"
    word_cloud.to_file(location)
        
    return [{"image_location":location}] + tweets_list

def clear_folder():
    mydir = "static/img/wordcloud/"
    filelist = [ f for f in os.listdir(mydir)]
    for f in filelist:
        os.remove(os.path.join(mydir, f))

# tweet()
india_tweet()