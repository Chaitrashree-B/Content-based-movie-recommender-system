#!/usr/bin/env python
# coding: utf-8

# In[53]:


import numpy as np
import pandas as pd


# In[54]:


movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


# In[55]:


movies.head(5)


# In[56]:


credits.head(1)


# In[60]:


movies=movies.merge(credits,on='title')


# In[61]:


movies.head(1)


# In[62]:


# genres
# id
# keywords
# title
# overview
# cast
# crew
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[95]:


movies.info()


# In[64]:


movies.head()


# In[65]:


movies.isnull().sum()


# In[66]:


movies.dropna(inplace=True)


# In[67]:


movies.duplicated().sum()


# In[68]:


# '[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'
# ['Action','Adventure','Fantasy','SciFi']


# In[71]:


def convert(obj):
   L = []
   for i in ast.literal_eval(obj):
        L.append(i['name'])
   return L


# In[70]:


import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')


# In[73]:


movies['genres']=movies['genres'].apply(convert)


# In[74]:


movies.head()


# In[76]:


movies['keywords']=movies['keywords'].apply(convert)


# In[77]:


movies.head()


# In[78]:


movies['cast'][0]


# In[79]:


def convert3(obj):
    L = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
          L.append(i['name'])
          counter+=1
        else:
            break
    return L


# In[81]:


movies['cast']=movies['cast'].apply(convert3)


# In[82]:


movies.head()


# In[83]:


movies['crew'][0]


# In[86]:


def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
          L.append(i['name'])
          break
    return L


# In[94]:


movies['crew']=movies['crew'].apply(fetch_director)


# In[96]:


movies.head()


# In[97]:


movies['overview'][0]


# In[100]:


movies['overview']=movies['overview'].apply(lambda x:x.split())


# In[101]:


movies.head()


# In[102]:


movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


# In[103]:


movies.head()


# In[105]:


movies['tags']=movies['overview'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[106]:


movies.head()


# In[108]:


new_df=movies[['movie_id','title','tags']]


# In[109]:


new_df


# In[111]:


new_df['tags']=new_df['tags'].apply(lambda x:" ".join(x))


# In[112]:


new_df.head()


# In[113]:


new_df['tags'][0]


# In[115]:


new_df['tags']=new_df['tags'].apply(lambda x:x.lower())


# In[116]:


new_df.head()


# In[117]:


get_ipython().system('pip install nltk')


# In[118]:


import nltk


# In[119]:


from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[120]:


def stem(text):
    y=[]
    
    for i in text.split():
        y.append(ps.stem(i))
    return  " ".join(y)


# In[122]:


new_df['tags']=new_df['tags'].apply(stem)


# In[123]:


new_df['tags'][0]


# In[124]:


new_df['tags'][1]


# In[125]:


get_ipython().system('pip install scikit-learn')


# In[126]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')


# In[129]:


vectors = cv.fit_transform(new_df['tags']).toarray()


# In[130]:


vectors


# In[131]:


vectors[0]


# In[132]:


cv.get_feature_names_out()


# In[133]:


len(cv.get_feature_names_out())


# In[134]:


['loved','loving','love']
['love','love','love']


# In[135]:


ps.stem('dancing')


# In[136]:


stem('in the 22nd century, a paraplegic marine is dispatched to the moon pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d samworthington zoesaldana sigourneyweaver jamescameron')


# In[137]:


from sklearn.metrics.pairwise import cosine_similarity


# In[139]:


similarity = cosine_similarity(vectors)


# In[140]:


sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]


# In[141]:


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        print(new_df.iloc[i[0]].title)


# In[142]:


recommend('Batman Begins')


# In[143]:


new_df.iloc[3608].title


# In[144]:


import pickle


# In[145]:


pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))
new_df['title'].values


# In[147]:


new_df.to_dict()


# In[148]:


pickle.dump(similarity,open('similarity.pkl','wb'))


# In[ ]:




