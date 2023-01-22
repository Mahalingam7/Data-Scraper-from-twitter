import streamlit as st
import numpy as np
import pymongo
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date
from datetime import timedelta
import json
 
# Get today's date
today = date.today()
print("Today is: ", today)
 
# Yesterday date
yesterday = today - timedelta(days = 1)
print("Yesterday was: ", yesterday)

# Making a Connection with MongoClient
client = pymongo.MongoClient("mongodb://localhost:27017/")
# database
db = client["tweet_scrape"]
# collection
data= db["tweet_data"]

st.header("Data Scraper from Twitter", anchor=None)


search=st.text_input("Hashtag", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None,
            on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False, label_visibility="visible")

from_date=st.date_input('From Date', value=yesterday, min_value=None, max_value=None, key=None, help=None,
              on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")

till_date=st.date_input('Till Date', value=None, min_value=None, max_value=None, key=None, help=None,
              on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")

tweet_count=st.number_input('Tweet Count', min_value=None, max_value=None, value=1, step=None, format=None, key=None,
                help=None, on_change=None, args=None, kwargs=None,  disabled=False, label_visibility="visible")

st.write(search,from_date,till_date,tweet_count)
hashtag=f'"{search} since:{from_date} until:{till_date}"'
if search != '':
    # Creating list to append tweet data 
    tweets_list1 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(hashtag).get_items()): #declare a username 
        if i>(tweet_count-1): #number of tweets you want to scrape
            break
        tweets_list1.append([tweet.date, tweet.id, tweet.url,tweet.content, tweet.user.username,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source,tweet.likeCount]) #declare the attributes to be returned
    
    # Creating a dataframe from the tweets list above 
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Id','Url', 'Text', 'Username','Reply_count','Retweet_count','Lang','Source','Like_count'])
    st.write(tweets_df1)
    
    upload=st.button('Upload data to DATABASE', key=None, help=None, on_click=None, args=None, kwargs=None,  type="secondary", disabled=False)
    data_dict = tweets_df1.to_dict("records")
    data.insert_many(tweets_df1.to_dict('records'))
    
    csv = tweets_df1.to_csv().encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='data.csv',
        mime='text/csv',
    )

    json_string = tweets_df1.to_json()
    st.download_button(
        label="Download data as JSON",
        file_name="data.json",
        mime="application/json",
        data=json_string,
    )

