import pickle
import streamlit as st
import requests
import gzip

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Add custom CSS for justified text
st.markdown("""
    <style>
    .justified-text {
        text-align: justify;
    }
    .main-header {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# MovieMingle heading
st.markdown('<h1 class="main-header">MovieMingle</h1>', unsafe_allow_html=True)

# Movie Recommendation System heading
st.header('Movie Recommendation System Using Machine Learning')

# Load the movie list without compression
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))

# Load the similarity matrix with gzip compression
with gzip.open('artifacts/similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or Select a Movie from the dropdown menu",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="justified-text">{recommended_movie_names[0]}</div>', unsafe_allow_html=True)
        st.image(recommended_movie_posters[0])
    with col2:
        st.markdown(f'<div class="justified-text">{recommended_movie_names[1]}</div>', unsafe_allow_html=True)
        st.image(recommended_movie_posters[1])
    with col3:
        st.markdown(f'<div class="justified-text">{recommended_movie_names[2]}</div>', unsafe_allow_html=True)
        st.image(recommended_movie_posters[2])
    with col4:
        st.markdown(f'<div class="justified-text">{recommended_movie_names[3]}</div>', unsafe_allow_html=True)
        st.image(recommended_movie_posters[3])
    with col5:
        st.markdown(f'<div class="justified-text">{recommended_movie_names[4]}</div>', unsafe_allow_html=True)
        st.image(recommended_movie_posters[4])
