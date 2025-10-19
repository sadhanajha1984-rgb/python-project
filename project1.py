import pandas as pd
import numpy as np
import ast
credits_df=pd.read_csv("credits.csv")
movies_df=pd.read_csv("movies.csv")
print(movies_df.head())
print(credits_df.head())
movies_df=movies_df.merge(credits_df,on='title')
print(movies_df.head())
print(movies_df.head())
#generes
#id
##keywords
#original language
movies_df=movies_df[['id','title','overview','genres','keywords','cast','crew']]
print(movies_df.head())
print(movies_df.dropna(inplace=True))
print(movies_df.isnull().sum())
print(movies_df.duplicated().sum())
#for sorting the genres
def convert(obj):
    l=[]
    return [i['name'] for i in ast.literal_eval(obj)]

movies_df['genres'] = movies_df['genres'].apply(convert)
movies_df['keywords'] = movies_df['keywords'].apply(convert)


# print(movies_df.head())
# print(movies_df['cast'][0])
def convert3(obj):
    l=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter != 3:
           l.append(i['name'])
           counter+=1
        else:
           break
    return l
movies_df['cast']=movies_df['cast'].apply(convert3)
print(movies_df.head())
def fetch_director(obj):
    l=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            l.append(i['name'])
            break
    return l
movies_df['director']=movies_df['crew'].apply(fetch_director)
movies_df['overview']=movies_df['overview'].apply(lambda x:x.split())
movies_df['genres']=movies_df['genres'].apply(lambda x:[i.replace(" ","")for i in x])
movies_df['keywords']=movies_df['keywords'].apply(lambda x:[i.replace(" ","")for i in x])
movies_df['cast']=movies_df['cast'].apply(lambda x:[i.replace(" ","")for i in x])
movies_df['director']=movies_df['director'].apply(lambda x:[i.replace(" ","")for i in x])
movies_df['tags']=movies_df['overview']+movies_df['genres']+movies_df['keywords']+movies_df['cast']+movies_df['director']
new_df=movies_df[['id','title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())
movies_df.drop(columns=['crew'], inplace=True)
new_df.to_excel('project1.xlsx', index=False)
print(new_df.head())



