import streamlit as st
import pandas as pd

from bookworm import Card

CSV = pd.read_csv('pg_catalog.csv')
check = st.multiselect("Rechercher produits :", CSV["Title"])

if check :
    result = CSV[CSV["Title"].isin(check)].iloc[0]
    schema = Card(result["Text#"])

    st.write(schema)