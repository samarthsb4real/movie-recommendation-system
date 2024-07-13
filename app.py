import streamlit as st
import pickle
import requests

# Creating the API function
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Creating the recommend function
def recommend(movie, num_recommendations):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:num_recommendations + 1]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances:
        movie_id = movies.iloc[i[0]]['id']
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]]['title'])

    return recommended_movie_names, recommended_movie_posters

st.title('Movie Recommendation System')

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))

selected = st.selectbox('Enter a movie title', movies['title'].values)
num_recommendations = st.number_input(label='How many similar movies do you want to recommend?', min_value=1, max_value=10, value=5)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected, num_recommendations)
    columns = st.columns(num_recommendations)
    for idx, col in enumerate(columns):
        col.text(recommended_movie_names[idx])
        col.image(recommended_movie_posters[idx])
