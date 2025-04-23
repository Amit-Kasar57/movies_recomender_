import pickle
import pandas as pd
import streamlit as st
from auth_utils import load_users, save_user, user_exists, validate_user

# --- Page Config ---
st.set_page_config(page_title="Movie Recommender", layout="centered")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Header ---
st.markdown("<h1 style='color:#1f77b4;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# --- Auth Section ---
if not st.session_state.logged_in:
    mode = st.radio("Select Option", ["Login", "Create Account"], horizontal=True)

    with st.form("auth_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")

        mobile = st.text_input("Mobile Number (Username)")
        password = st.text_input("Password", type="password")

        submit_btn = st.form_submit_button("Submit")

        if submit_btn:
            if all([first_name, last_name, mobile, password]):
                if mode == "Create Account":
                    if user_exists(mobile):
                        st.error("🚫 Account already exists. Please log in.")
                    else:
                        save_user(first_name, last_name, mobile, password)
                        st.success("✅ Account created! Please log in.")
                else:  # Login
                    user_data = validate_user(mobile, password)
                    if user_data is not False:  # If validation succeeds
                        st.session_state.logged_in = True
                        st.session_state.first_name = user_data["first_name"]
                        st.session_state.last_name = user_data["last_name"]
                        st.success(f"Welcome back, {user_data['first_name']} 👋")
                    else:
                        st.error("❌ Invalid credentials.")
            else:
                st.warning("⚠️ Please fill in all fields to proceed.")

# --- Main App ---
if st.session_state.logged_in:
    # Load movie data
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    # Recommend function
    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        return [movies.iloc[i[0]].title for i in movie_list]

    # UI
    st.markdown("## Pick a movie you like and get 5 similar recommendations!")
    selected_movie = st.selectbox("🎥 Select a movie", movies['title'].values)

    if st.button("✨ Recommend"):
        recommended = recommend(selected_movie)
        st.subheader("📽️ Recommended Movies & Trailers:")
        for movie in recommended:
            st.markdown(f"**🎬 {movie}**")
            yt_link = f"https://www.youtube.com/results?search_query={movie.replace(' ', '+')}+trailer"
            st.markdown(f"[▶️ Watch Trailer]({yt_link})", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔒 Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
