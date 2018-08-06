from sklearn.datasets import make_blobs
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

filepath=''
def doKMeanAnalysis():
    filepath=input("Please enter the complete file path of csv file for which you want to do k-means analysis ")
    demoprint(filepath)  


def demoprint(filepath):
    kvalue=input('Please enter k value:')
    df=pd.read_csv(filepath)
#df=df.drop('day',axis=1)
    cols = df.columns
    num_cols = df._get_numeric_data().columns
    num_cols
    categories=list(set(cols) - set(num_cols))
    df_tr=df
    df_tr = pd.get_dummies(df_tr, columns=categories)
    df_tr.head()
    scalar =StandardScaler()
    scalar.fit(df_tr)
    scaled_features=scalar.transform(df_tr)
    df2=pd.DataFrame(scaled_features,columns=df_tr.columns)
    model=KMeans(n_clusters=int(kvalue))
    model=model.fit(df2)
    labels = model.labels_
    df_tr['clusters'] = labels
# analyze the clusters
    print('The mean values of each attribute are shown below for each cluster')
    print (df_tr.groupby('clusters').mean())

    print('now in the demo file,kvalue=',kvalue)
    answer=input("Do you wish to enter a new k-value for the same file(y/n)")
    if(str.lower(answer)=='y'):
        demoprint(filepath)
    else:
        doKMeanAnalysis()