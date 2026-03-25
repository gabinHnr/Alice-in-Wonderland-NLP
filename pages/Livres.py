import streamlit as st
import pandas as pd

from bookworm import Card


@st.cache_data
def load_data(ID):
    return Card(ID)

CSV = pd.read_csv('pg_catalog.csv')
check = st.multiselect("Rechercher produits :", CSV["Title"])

st.markdown(
    """
    <style>
    .montexte {
        text-align : center
    }
    </style>
    """,
    unsafe_allow_html=True
)

col_menu, col_main = st.columns([1,2], gap="large")

if check :
    result = CSV[CSV["Title"].isin(check)].iloc[0]
    schema = load_data(result["Text#"])
    st.write(schema)
    with col_menu:
        st.image(f'https://www.gutenberg.org/cache/epub/{result["Text#"]}/images/cover.jpg')
    with col_main:
        st.header("Titre")
        st.subheader(schema["info"]["title"])
        st.header("Auteur")
        st.subheader(schema["info"]["authors"])
        st.header("Résumé")        
        st.markdown(f'<p class="montexte">{schema["summary"]}</p>', unsafe_allow_html=True)

def load_custom_css():
    st.markdown("""
    <style>
    /* Customiser les boutons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    """)