import streamlit as st
import pickle

#creating the recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:7]

    recommendations_list = []
    for i in movies_list:
        recommendations_list.append(movies.iloc[i[0]].title)

    return recommendations_list

st.title('Movie Recommendation System')

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))


selected = st.selectbox('Enter a movie title', movies['title'].values)

st.number_input(label='How many similar movies do you want to recommend?', min_value=1,max_value=10)

if st.button(label='Show Recommendations'):
    recommendations = recommend(selected)
    for i in recommendations:
        st.write(i)

