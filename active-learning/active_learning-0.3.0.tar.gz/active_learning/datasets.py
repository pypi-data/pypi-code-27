import pickle
import pandas as pd
import os

def twentynews_tfidf(file_path):
    twd = os.path.dirname(os.path.abspath(__file__))
    with open(file_path, 'rb') as f:
        dataset = pickle.load(f)
    # dataset
    sentences = dataset['raw']
    X_tfidf = dataset['data']
    y = dataset['target']
    names = dataset['features']
    X = pd.DataFrame(X_tfidf)
    X.columns = names

    return X, y, sentences
