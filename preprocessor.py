import re
import pandas as pd

def preprocess(data):
    # Pattern in chat (Splitting DataTime and Messages)
    patten = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s"
    
    # All messages we have
    message = re.split(patten, data)[1:]
    
    # All date we have
    dates = re.findall(patten, data)
    
    # Split date and time
    date = []
    times = []
    for i in dates:
        date.append(i.split(", ")[0])
        times.append(i.split(", ")[1])
    
    time = []
    for i in times:
        time.append(i.split("\u202f")[0])        
        
    # Create Dataframe
    df = pd.DataFrame({
    'user_msg' : message,
    'date' : date,
    'time' : time
    })

   # Splitting user name and msg
    user = []
    msg = []
    for i in df['user_msg']:
        x = re.split("([\w\W]+?):\s", i)
        if x[1:]:  # If username exists
            user.append(x[1])
            msg.append(x[2])
        else:
            user.append('Group Notification')
            msg.append(x[0])
            
    df['user'] = user
    df['msg'] = msg
    df.drop(columns=['user_msg'], inplace=True)

    # Identify media messages
    media_keywords = ['[Media omitted]', 'image omitted', 'video omitted']
    df['is_media'] = df['msg'].apply(lambda x: any(keyword in x for keyword in media_keywords))

    
    # Convert Date Column inti DateTime format
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = (df['date']).dt.year    
    df['month'] = (df['date']).dt.month_name()    
    df['day'] = (df['date']).dt.day_name()   
    
    
    return df 

