import streamlit as st
import pickle
import requests

def find_poster_with_url(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=fb1065e0d431f8d31b55ae47295bd36d&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+ data['poster_path'] , data['homepage']


def recommend(movie):
    movie_index = movies_data[movies_data['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)),reverse=True, key= lambda x: x[1])[1:6]
    
    recommed_movies = []
    movie_posters = []
    movie_url = []

    for data in movies_list:
        movie = movies_data.iloc[data[0]]
        recommed_movies.append(movie.title)
        img, url = find_poster_with_url(movie.movie_id)
        movie_posters.append(img)
        movie_url.append(url)

    return recommed_movies, movie_posters, movie_url

movies_data = pickle.load(open('movies.pkl', 'rb'))
movies_name = movies_data['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Need Some Movie Suggestions")


st.write('The algorithm is trained with 5 years old TMDB 5000 Movie Dataset, So please ask me some little old movies I will give you suggestions')
movie_selected = st.selectbox(
    'Please select the Your Favorite Movies, we will recommend the similar!',
    movies_name)

if st.button('Recommend',type="primary"):
    st.write('Our Recommendations:')
    names, images, url = recommend(movie_selected)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(images[0])
        st.caption(names[0])
        st.markdown("[Movie link](%s)" % url[0])

    with col2:
        st.image(images[1])
        st.caption(names[1])
        st.markdown("[Movie link](%s)" % url[1])

    with col3:
        st.image(images[2])
        st.caption(names[2])
        st.markdown("[Movie link](%s)" % url[2])

    with col4:
        st.image(images[3])
        st.caption(names[3])
        st.markdown("[Movie link](%s)" % url[3])

    with col5:
        st.image(images[4])
        st.caption(names[4])
        st.markdown("[Movie link](%s)" % url[4])
