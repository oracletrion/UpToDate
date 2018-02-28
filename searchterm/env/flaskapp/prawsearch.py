import praw
import datetime
import sqlite3
import time
from datetime import date

reddit = praw.Reddit(client_id ="iWuKrG6a3LP0JA",
                    client_secret ="U2OP49DBu9EXk7wqA0lIwSpkB7g",
                    username="trqanees",
                    password = "Iammuslim1-",
                    user_agent ="prawsearchterm")

conn = sqlite3.connect('prawsearchterm.db')
c = conn.cursor()


def insert_user_topic(searchTerm, startDate):
    c.execute("INSERT INTO userTopics VALUES (?, ?)",(searchTerm, startDate))
    conn.commit()

def add_topic():
    trackingDate = date.today()
    insert_user_topic('DACA', trackingDate)


def create_tables():
    c.execute('''CREATE TABLE searchTable(submDatePosted DATE, submTitle text, submSearchTerm text, submURL text )''')
    c.execute('''CREATE TABLE userTopics(topic text, submTrackingDate DATE )''')

def database_crawl():
    iterator = conn.cursor()
    iterator.execute("select topic from userTopics")
    for row in iterator:
        topic = row[0]
        stack = []
        for post in reddit.subreddit('DonaldTrump').new(limit=5):

            time = post.created
            submDatePosted = datetime.date.fromtimestamp(time)
            submTitle = post.title
            submTerm = topic
            submURL = post.url
            urlCheck = verifyURL(submURL)

            data = {
                'submDatePosted': submDatePosted,
                'submTitle': submTitle,
                'submTerm': submTerm,
                'submURL': submURL
            }
            if not urlCheck:
                stack.append(data)
                #c.execute("INSERT INTO searchTable VALUES (?, ?, ?, ?)",(submDatePosted, submTitle, submTerm, submURL))
                conn.commit()
        insertToDB(stack)

def insertToDB(stack):
    # print('The length of stack is ' + len(stack))
    for item in stack:
        data = stack.pop()
        print(data['submTitle'])
        c.execute("INSERT INTO searchTable VALUES (?, ?, ?, ?)",(data['submDatePosted'], data['submTitle'], data['submTerm'], data['submURL']))
        conn.commit()


def verifyURL(postURL):
    if 'reddit.com' in postURL:
        return True

def checkTableEmpty():
        c.execute('SELECT exists(SELECT 1 FROM searchTable LIMIT 1)' )
        check = c.fetchone()
        if 0 in check:
            return True
        else:
            return False

def retrieve_latest_posts():
    c = conn.cursor()
    c.execute('SELECT submURL FROM searchTable ORDER BY submURL DESC LIMIT 1' )
    lastentry = c.fetchone()
    print(lastentry)
    return lastentry




#insert_user_topic()
database_crawl()
#add_topic()
#create_tables()
#termURL = retrieve_latest_posts()
#data_entry()
#retrieve_latest_posts()
