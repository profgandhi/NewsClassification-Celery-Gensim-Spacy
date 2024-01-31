from celery import group
from feed_parser import item_parser
import pandas as pd
from news_processing import get_classes
from database_storage import store_articles_in_database
from time import sleep

if __name__ == "__main__":
    links = [
        "http://rss.cnn.com/rss/cnn_topstories.rss",
        "http://qz.com/feed",
        "http://feeds.foxnews.com/foxnews/politics",
      #  "http://feeds.reuters.com/reuters/businessNews",
        "http://feeds.feedburner.com/NewshourWorld",
        "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
    ]

    # Use Celery group to run tasks asynchronously
    tasks = group(item_parser.s(feed_url) for feed_url in links).delay()

    results = tasks.get()
    print(results)

    # Retrieve results from the tasks
    print(results)
    parsed_articles = pd.concat(results,axis=0)
    parsed_articles.dropna(inplace=True)
    print(2)
    #Predict classes using gensim and spacy
    parsed_articles['class_label'] = get_classes(parsed_articles.copy())


    # Store parsed articles in the database
    store_articles_in_database(parsed_articles)