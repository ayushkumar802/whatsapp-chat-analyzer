import re
import pandas as pd
import numpy as np

def preprocessor(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}[\u202f\s]?[AP]M\s-\s"
    message = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': message, 'message_date': date})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M %p - ")
    df['day'] = df['message_date'].dt.day
    df['month'] = df['message_date'].dt.month_name()
    df['year'] = df['message_date'].dt.year
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    user = []
    mes = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            user.append(entry[1])
            mes.append(entry[2])
        else:
            user.append("group_notification")
            mes.append(entry[0])
    df['user'] = user
    df['message'] = mes
    df.drop(columns=['user_message'], inplace=True)
    if 'You deleted this message\n' in df['message'].tolist():
        user_name = df[df['message'] == 'You deleted this message\n']['user'].tolist()[0]
        df['user']=df['user'].apply(lambda x: "You" if x==user_name else x)

    return df

