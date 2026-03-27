import streamlit as st
import pandas as pd

from bookworm import Card


@st.cache_data
def load_data(ID, modele_large):
    if modele_large:
        return Card(ID, True)
    else:
        return Card(ID)
    
st.markdown('<div class="bandeaubleu">''</div>', unsafe_allow_html=True)
st.markdown('<div class="bandeaubleuclair">''</div>', unsafe_allow_html=True)
col1_top, col2_top, col3_top = st.columns([1,2,1], gap="large")
col_illu, col_carte = st.columns([1,2], gap="large")

CSV = pd.read_csv('pg_catalog.csv')

st.markdown("""
            <style>

                .stApp {
                    background-color: white;
                    margin : 0;
                }
            
                .bandeaubleu{
                    position: absolute;
                    background-color : #7ebed0;
                    width : 100vw;
                    height : 8vh;
                    right : -80px;
                    top : -40px;
                }
            
                .bandeaubleuclair{
                    position: absolute;
                    background-color : #c7dde3;
                    width : 100vw;
                    height : 8vh;
                    top : 1.9vh;
                    right : -80px;
                }
            
                .montexte, .montextegras {
                    margin: -20px 0 0 0  !important;
                    padding : 20px;
                    text-align : center;
                    font-size: 20px !important;
                    color : black;
                    background-color: #ACB7BF;
                    border-radius : 10px;
                }
            
                .montextegras{
                    text-transform : uppercase;
                }
            

                .montitre {
                    margin: -20px 0 0 0  !important;
                    padding : 20px;
                    text-align : center;
                    font-size: 40px !important;
                    font-weight : bold;
                    color : black;
                    background-color: #ACB7BF;
                    border-radius : 10px;
                }
                .divisioncarte {
                    position: relative;
                    padding : 20px 0 0 0;
                    display : flex;
                    justify-content : center;
                    align-items : center;
                }

                .emplacementcarte {
                    position: absolute;
                    width: 105%;
                    height: 120vh;
                    background-color: #F0F0F0;
                    border-radius: 15px;
                    z-index: 0;
                    left : -20px;
                }

                .Carte {
                    position: relative;
                    z-index: 1;
                    padding: 0 40px;
                    background-color : red;
                }
            
                .recherche{
                    color: black;
                }
            
                .noshow {
                    display: none;
                }
            </style>""",unsafe_allow_html=True)

with col2_top:
    check = st.text_input("")
with col3_top:
    modèlelarge = st.checkbox("Modèle large ?", value=False)

if check:
    filtered = CSV[CSV["Title"].str.contains(check, case=False, na=False)] 

    st.markdown('<div class="noshow">', unsafe_allow_html=True)
    choice = st.selectbox(
        "Résultats :",
        filtered["Title"].head(20),
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    result = CSV[CSV["Title"] == choice].iloc[0]
    schema = load_data(result["Text#"], modèlelarge)
    with col_illu:
        st.markdown('<div class="divisioncarteillu">', unsafe_allow_html=True)
        st.image(f'https://www.gutenberg.org/cache/epub/{result["Text#"]}/images/cover.jpg')
        st.markdown('', unsafe_allow_html=True)
    with col_carte:
        st.markdown('<div class="divisioncarte">', unsafe_allow_html=True)

        st.markdown('<div class="Carte">', unsafe_allow_html=True)

        st.markdown('<p class="montitre">Titre du livre</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="montextegras">{schema["info"]["title"]}</p>', unsafe_allow_html=True)
        st.markdown('<p class="montitre">Auteur(e)(s)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="montextegras">{schema["info"]["authors"]}</p>', unsafe_allow_html=True)
        st.markdown('<p class="montitre">Résumé</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="montexte">{schema["summary"]}</p>', unsafe_allow_html=True)
        st.markdown('<p class="montitre">Personnages</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="montexte">{schema["entities"]["characters"]}</p>', unsafe_allow_html=True)
        st.markdown('<p class="montitre">Lieux</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="montexte">{schema["entities"]["locations"]}</p>', unsafe_allow_html=True)
        st.markdown('<p class="montitre">Livre similaire</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="montexte">{schema["similar"]}</p>', unsafe_allow_html=True)

        st.markdown('</div></div>', unsafe_allow_html=True)
else:
    filtered = CSV