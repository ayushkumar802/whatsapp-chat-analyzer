import pandas as pd
from urlextract  import URLExtract
import re
from wordcloud import WordCloud
from collections import Counter
import emoji
def fetch_total(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]
    a=df.shape[0]


    b = df['message_date'].min()


    words=[]
    for messages in df['message']:
        for word in messages.split():
            words.append((word))

    d=df[df['message']=="<Media omitted>\n"].shape[0]

    link=[]
    extractor = URLExtract()
    for message in df['message']:
        link.extend(extractor.find_urls(message))
    e=len(link)

    return a,b.date(),len(words),d,e

def fetch_top_user(df):
    df = df[df['user'] != 'group_notification']
    new_df = round(100 * df['user'].value_counts() / df.shape[0], 2).reset_index().rename(columns={
        'user': 'name',
        'count': 'percentage'
    })
    return df['user'].value_counts().head(10),new_df.head(10)

def group_name(text):
    pattern = 'WhatsApp Chat with ([\w\W]+?).txt'
    m = re.split(pattern,text)[1]
    m = m.split()
    return " ".join(m[:3])

def top_words(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    temp = temp[temp['message'] != 'You deleted this message\n']

    file = open("stopword/hinenglish_stopwords.txt","r",encoding='utf-8')
    stopword = file.read()
    stopword = stopword.split("\n")

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopword:
                words.append(word)

    top_words=Counter(words).most_common(20)

    new_df=pd.DataFrame(top_words)
    new_df.rename(columns={
        0:'words',
        1:'frequency'
    },inplace=True)

    wc =WordCloud(width=700,height=700,min_font_size=9,background_color='white')
    df_wc = wc.generate(" ".join(words))

    return df_wc, new_df

def emojis_count(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]
    emojis=[]
    for message in df['message']:
        for letter in message:
            if letter in emoji.EMOJI_DATA:
                emojis.extend(letter)
    a=Counter(emojis).most_common(20)
    new_df = pd.DataFrame(a,columns=['Emojis','Frequency'])

    return new_df


def timeline(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]
    df['month_num'] = df['message_date'].dt.month
    tl=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(tl.shape[0]):
        time.append(tl['month'][i]+"-"+str(tl['year'][i]))

    tl['time'] = time
    tl.drop(columns=['year','month','month_num'],inplace=True)

    tl.rename(columns={
        'message' : 'no. of message',
        'time' : 'month'
    },inplace=True)

    tl=tl.reindex(columns=['month','no. of message'])

    return tl

def delete_messages(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    if len(df['user'].unique()) > 3:
        gh = df[df['message'].isin(['This message was deleted\n', 'You deleted this message\n'])][
            'user'].value_counts().reset_index()
        if gh['count'].mean() > 2:
            top404 = gh[gh['count'] > 4]['user']
            df['user'] = df['user'].apply(lambda x: 'other' if x not in top404.values else x)                         #8888888888888888

    return df[df['message'].isin(['This message was deleted\n', 'You deleted this message\n'])][
        'user'].value_counts().reset_index()

def weekly_timeline(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    df['day_name']=df['message_date'].dt.day_name()
    df['only_date'] = df['message_date'].dt.date


    return df['day_name'].value_counts(), df.groupby('only_date').count()['message']


def notification(df):
    temp=df[df['user']=='group_notification']

    group_noti=temp['message'].value_counts().reset_index()

    pinned_message = 0
    joined = 0
    added = 0
    removed = 0
    left = 0
    changed = 0
    other = 0
    for i in range(group_noti.shape[0]):
        if "pinned a message" in group_noti['message'][i]:
            pinned_message += group_noti['count'][i]
        elif "joined" in group_noti['message'][i]:
            joined += group_noti['count'][i]
        elif "added" in group_noti['message'][i]:
            added += group_noti['count'][i]
        elif "removed" in group_noti['message'][i]:
            removed += group_noti['count'][i]
        elif "left" in group_noti['message'][i]:
            left += group_noti['count'][i]
        elif "changed" in group_noti['message'][i]:
            changed += group_noti['count'][i]
        else:
            other += group_noti['count'][i]

    temp2 = pd.DataFrame([pinned_message, joined, added, removed, left, changed, other],
                         ["pinned\nmessages", "joining\nnotification", "adding\nnotification", "removing\nnotification",
                          "leaving\nnotification", "gc changes\nnotification", "other"]).reset_index()

    temp2.rename(
        columns={
            "index": "Group Notification",
            0: "Counts"
        }, inplace=True)

    temp2=temp2[temp2['Counts']!=0]

    return temp2

def monthlyactivity(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

        df['month_num'] = df['message_date'].dt.month

    return df.groupby(['month_num','month']).count()['message'].reset_index()

def heatmaps_(selected_user,df):
    if selected_user != "OverAll":
        df = df[df['user'] == selected_user]

    heat_df = df.pivot_table(index="day_name", columns="period",values="message",aggfunc="count").fillna(0)

    return heat_df



