from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker,declarative_base
from config import postgresql as settings
import pandas as pd

#------------------------------------------
def store_articles_in_database(articles: pd.DataFrame):
    for i,article in articles.iterrows():
        # Check for duplicates before adding to the database
        existing_article = session.query(NewsArticle).filter_by(title=article['link']).first()
        if not existing_article:
            db_article = NewsArticle(**article.to_dict())
            session.add(db_article)
    session.commit()

def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, pool_size=50, echo=False)
    return engine

#------------------------------------------
Base = declarative_base()
class NewsArticle(Base):
    __tablename__ = 'news_articles'

    link = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    content = Column(String)
    pub_date = Column(DateTime)
    class_label = Column(String)
engine = get_engine(settings['pguser'],
                    settings['pgpasswd'],
                    settings['pghost'],
                    settings['pgport'],
                    settings['pgdb'])
Base.metadata.drop_all(bind=engine, tables=[NewsArticle.__table__])
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
#------------------------------------------

    



