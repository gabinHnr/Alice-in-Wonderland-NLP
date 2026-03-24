import streamlit as st

st.set_page_config(layout="wide")

Livre = st.Page(
    page="pages/Livres.py",
    title="Exploration des données",
    default=True,
)
pg = st.navigation(pages=[Livre])
pg.run()


footer = """<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Gabin Hannier | Bastian Hanart<br>2026 - Alice's Adventures In Wonderland - { EPITECH }</p>

</div>
"""
st.markdown(footer, unsafe_allow_html=True)