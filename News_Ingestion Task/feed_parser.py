import pandas as pd
import requests
from bs4 import BeautifulSoup
from celery import Celery
import logging
from config import postgresql as settings

logging.basicConfig(filename='news_processing.log', level=logging.INFO)
user = settings['pguser']                            
passwd = settings['pgpasswd']
host = settings['pghost']
port = settings['pgport']
db = settings['pgdb']
app = Celery('feed_parser', broker='pyamqp://guest:guest@localhost//',backend=f'db+postgresql://{user}:{passwd}@{host}:{port}/{db}')


@app.task()
def item_parser(link):
    a = pd.DataFrame(columns=['title','link','pub_date','description','content'])
    articles = []
    try:
        r = requests.get(link) 
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')

        
        for item in items:
            title = item.title.text
            link = item.link.text
            try:
                pub_date = item.pubDate.text
            except:
                pub_date = None
            try:
                description = item.description.text
            except:
                description = None
            try:
                content = item.description.text
            except:
                content = None
            article = {
                'title' : title,
                'link': link,
                'pub_date': pub_date ,
                'description': description,
                'content':content
            }
            articles.append(article)

        a = pd.DataFrame(articles)
        return a

    except Exception as e:
        logging.error(f"Error parsing feed {link}: {e}")
        return a

    