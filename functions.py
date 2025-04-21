# Importing class URLExtract from urlextract
from urlextract import URLExtract

#  Importing class WordCloud from wordcloud
from wordcloud import WordCloud

# Importing emojis
import emoji
from collections import Counter

# Importing Textblob for NLP or for Sentiment Analysis
from textblob import TextBlob

import pandas as pd

# Creating object of URLExtract class
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
        
    # number of msgs
    num_msgs = df.shape[0]
    
    # number of words
    # words = []
    # for msg in df['user']:
    #     words.extend(msg.split())
    
    # number of media
    media_keywords = ["<Media omitted>", "image omitted", "image omitted", "[Media omitted]", "audio omitted", "video omitted"]

    num_med = df['msg'].apply(lambda x: any(keyword in x for keyword in media_keywords)).sum()

    
    # number of links
    link = []
    for msg in df['msg']:
        link.extend(extract.find_urls(msg))

    return num_msgs, num_med, len(link)

def monthly_timeline(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
        
    timeline = df.groupby(['year', 'month'])['msg'].count().reset_index()
    
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    
    timeline['time'] = time
    
    return timeline

# daily timeline
def daily_timeline(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
        
    timeline = df.groupby('date')['msg'].count().reset_index()
    return timeline

def activity_map(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
        
    active_month_df = df.groupby('month')['msg'].count().reset_index()
    month_list = active_month_df['month'].tolist()
    month_msg_list = active_month_df['msg'].tolist()
    
    active_day_df = df.groupby('day')['msg'].count().reset_index()
    day_list = active_day_df['day'].tolist()
    day_msg_list = active_day_df['msg'].tolist()

    return active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list

def most_chaty(df):
    x = df['user'].value_counts().head()
    
    percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2)
    return x, percent

def create_wordcloud(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]
        
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['msg'].str.cat(sep=' '))
    return df_wc
    
def emoji_analysis(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['msg']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_counts = Counter(emojis).most_common()
    emoji_df = pd.DataFrame(emoji_counts)

    return emoji_df

# Getting the sentiments
# def get_sentiment(text):
#     blob = TextBlob(text)
#     sentiment = blob.sentiment.polarity
#     if sentiment > 0:
#         return 'Positive'
#     elif sentiment < 0:
#         return 'Negative'
#     else:
#         return 'Neutral'
