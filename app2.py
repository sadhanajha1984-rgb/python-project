import pickle

import pandas as pd
import streamlit as st
import requests
st.markdown("""
    <style>
    .stApp {
        background-color: black;  
        color: white;            
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    .stApp {
        background-color: black;
        color: white;

        /* Left-side vertical poster */
        background-image: 
            url("https://m.media-amazon.com/images/I/91vwVHABnZL._UF894,1000_QL80_.jpg"),  /* left poster */
            url("https://m.media-amazon.com/images/M/MV5BMjE5MjkwODI3Nl5BMl5BanBnXkFtZTcwNjcwMDk4NA@@._V1_.jpg");  /* right poster */
        background-repeat: no-repeat, no-repeat;
        background-position: left top, right top;  /* left poster on left, right poster on right */
        background-size: 400px 100%, 410px 100%;  /* both posters same width and full height */
        background-attachment: fixed, fixed;

        /* Padding to keep UI in the center */
        padding-left: 430px;   /* space for left poster */
        padding-right: 430px;  /* space for right poster */
        padding-top: 20px;
    }

    h1 { color: white !important; text-align: center; }
    h3 { color: white !important; }

    /* Selectbox text in black */
    div.stSelectbox div[role="combobox"] > div > div > span { color: black !important; }

    .stSelectbox, .stButton { margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)





def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    for i in movies_list:
     recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies




movies_dict=pickle.load(open("movies_dict.pkl", "rb"))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open("similarity.pkl", "rb"))
st.markdown("<h1 style='text-align:center;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
genre_keywords = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama",
    "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance",
    "Science Fiction", "Sci-Fi", "Thriller", "War", "Western"
]
def extract_genres_from_tags(tags_list):
    genres_found = []
    for tag in tags_list:
        for genre in genre_keywords:
            if genre.lower() in str(tag).lower() and genre not in genres_found:
                genres_found.append(genre)
    return genres_found



all_genres_in_data = set()
for tags in movies['tags']:
    if isinstance(tags, list):
        all_genres_in_data.update(extract_genres_from_tags(tags))
    elif isinstance(tags, str):
        all_genres_in_data.update(extract_genres_from_tags([tags]))


selected_genre = st.selectbox(" Select Genre", ["All"] + sorted(all_genres_in_data))


if selected_genre != "All":
    filtered_movies = movies[movies['tags'].apply(
        lambda x: any(selected_genre.lower() in str(tag).lower() for tag in (x if isinstance(x, list) else [x]))
        if pd.notna(x) else False
    )]
else:
    filtered_movies = movies

def recommend_by_genre(filtered_movies, top_n=5):
        # Just pick top N movies in this genre (can sort by popularity if available)
        return filtered_movies['title'].head(top_n).tolist()

selected_movies_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)



col1, col2 = st.columns(2)

with col1:
    if st.button('Recommend by Movie'):
        recommendations = recommend(selected_movies_name)
        st.markdown("<h3>🎯 Recommendations Based on Movie:</h3>", unsafe_allow_html=True)
        for i in recommendations:
            st.write(i)

with col2:
    if st.button('Recommend by Genre'):
        recommendations_genre = recommend_by_genre(filtered_movies)
        st.markdown(f"<h3>🎯 Top Movies in Genre: {selected_genre}</h3>", unsafe_allow_html=True)
        for i in recommendations_genre:
            st.write(i)

