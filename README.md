# Documentation

## Files and Functions

- database_storage.py (Responsible for storage of parsed data to database without dupicates)
- feed_parser.py (Responsible for parsing links async using celery and RabbitMQ)
- news_processing.py (Responsible for classifying news into categories using gensim and spacy)
- main.py (main file for bringing code together)
- config files have configs related to celery and postgresql database


## Running
RabbitMQ and postgresql service must be running in background

Runnign celery worker on terminal
```
celery -A feed_parser worker -P gevent --loglevel=info
```
Running Program
```sh
python main.py
```




