# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 16:53:41 2022

@author: mypc
"""

import pandas as pd
from outlierdetection import cleaning,outexter

def describeDF(x):
    print('analyzing Dataframe')
    print('Dataframe has',x.shape[1],' columns')
    print('\nThese columns are:', x.keys())
    for i in x.keys():
        print('column ',i,' has values that are the type of', x[i].dtype)
    print('\nDataframe has ',x.shape[0],' rows\n\n')

books= pd.read_csv ('BX-Books.csv', \
                    names=['bid','title','author','year','publisher', \
                           'urls','urlm','urll'],sep=';', \
                    on_bad_lines='skip', skiprows=1, encoding='latin-1')

books=cleaning(books,'year')
books=outexter(books,0.8,'year')
describeDF(books)

users=pd.read_csv ('BX-Users.csv', names=['uid','loc','age'], \
                   sep=';', skiprows=1, encoding='latin-1')
    
users=cleaning(users,'age')
users=outexter(users,0.4,'age')
describeDF(users)

ratings= pd.read_csv ('BX-Book-Ratings.csv', names=['uid','bid','rating'], \
                      sep=';', skiprows=1, encoding='latin-1')
    
ratings=cleaning(ratings,'rating')
ratings=outexter(ratings,0.6,'rating')
describeDF(ratings)

#Measure popularity by average rating

#book popularity
group1 = ratings[['bid','rating']].groupby(ratings['bid']).mean()
result1=pd.merge(books[['bid','title']],group1,how='inner',left_on='bid', \
                 right_on='bid')
result1=result1.drop(['bid'],axis=1)
result1.rename(columns = {'rating':'popularity'}, inplace = True)
result1=result1.sort_values(by=['popularity'],ascending=False)
print(result1)

#author popularity
group2=pd.merge(books[['bid','author']],group1,how='inner',left_on='bid', \
                right_on='bid')
result2=group2.drop(['bid'], axis=1)
result2.rename(columns={'rating':'popularity'},inplace=True)
result2=result2.groupby('author').mean()
result2=result2.sort_values(by=['popularity'],ascending=False)
print(result2)

#age range by reading activity
#prints the number of books read by each age group
group3=pd.merge(users[['uid','age']],ratings[['uid','rating']])
group3=group3.dropna()
result3=group3.drop(['uid'],axis=1)
result3.rename(columns = {'rating':'books read'}, inplace = True)
result3=result3[result3['age']>0]
result3=result3.groupby('age').sum()
result3['books read'].plot(title='BOOKS READ BY AGE GROUP',kind='line')


    