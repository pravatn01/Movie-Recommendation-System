import streamlit as st
import pickle

with open('cosine_similarity.pkl', 'rb') as file:
    cosine_sim = pickle.load(file)

with open('movies_df.pkl', 'rb') as file:
    df = pickle.load(file)

# function to get similar movies
def get_similar_movies(title, top_n=5):
    try:
        idx = df[df['title'] == title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        similar_movies = [df.iloc[i[0]]['title'] for i in sim_scores]
        return similar_movies
    except IndexError:
        return ["Movie not found in database"]

st.set_page_config(page_title="Movie Recommendation System", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommendation System 🍿</h1>",
    unsafe_allow_html=True
)

movie_title = st.selectbox("🎥 Select a Movie:", df['title'].unique())

top_n = st.slider("🔢 Number of Recommendations:", min_value=1, max_value=10, value=5)

if st.button("Get Recommendations"):
    with st.spinner("🔍 Searching for similar movies..."):
        recommendations = get_similar_movies(movie_title, top_n)

    st.markdown("## 🔥 Recommended Movies:")

    if recommendations[0] == "Movie not found in database":
        st.error("❌ Movie not found in database. Please try another title.")
    else:
        for i, movie in enumerate(recommendations, start=1):
            st.markdown(f"**{i}. {movie}**")


