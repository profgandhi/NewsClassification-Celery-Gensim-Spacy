import numpy as np
import spacy
import string
from gensim.models import KeyedVectors
import re
#-------------------
nlp = spacy.load("en_core_web_sm")
stop_words = nlp.Defaults.stop_words
punctuations = string.punctuation
class_names = ['Political_Unreset','Positive/Uplifting','Natural_Disaster']
classes = [
    ["terrorism", "protest"],
    ["positive","uplifting"],
    ["earthquake", "floods"] , # natural disasters
]
try:
    wv = KeyedVectors.load('vectors.kv')
except:
    print("Downloading KeyedVectors")
    import gensim.downloader as api
    wv = api.load('glove-twitter-50')
    wv.save('vectors.kv')

#-------------------

def sent_vec(sent):
    vector_size = wv.vector_size
    wv_res = np.zeros(vector_size)
    ctr = 1
    for w in sent:
        if w in wv:
            ctr += 1
            wv_res += wv[w]
    wv_res = wv_res/ctr
    return wv_res

def spacy_tokenizer(sentence):
    # Creating our token object, which is used to create documents with linguistic annotations.
    doc = nlp(sentence)

    # Lemmatizing each token and converting each token into lowercase
    mytokens = [ word.lemma_.lower().strip() for word in doc ]

    # print(mytokens)

    # Removing stop words
    mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]

    # return preprocessed list of tokens
    return mytokens


def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

def get_class(vector):
    similarity = KeyedVectors.cosine_similarities(vector, vectors)
    if(max(similarity)) >= 0.65:
        return class_names[np.argmax(similarity)]
    return 'other'

#------------------------------------------------------------------------------------------------------------------
vectors = np.array([sent_vec(i) for i in classes])
#Main Functions
def get_classes(df):
    df['content'] = df['content'].str.lower()
    df['content'] = df['content'].apply(remove_html)
    df['tokens'] = df['content'].apply(spacy_tokenizer)
    df['vec'] = df['tokens'].apply(sent_vec)
    return df['vec'].apply(get_class)
