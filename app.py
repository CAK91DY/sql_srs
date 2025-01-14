import streamlit as st
import pandas as pd
import duckdb

st.write("Mon app")

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    sql_query = st.text_area(label="Entrez votre requête SQL")

    if sql_query.strip():  # Vérification si une requête est entrée
        try:
            # Exécution de la requête SQL
            result = duckdb.query(sql_query).to_df()
            st.dataframe(result)
        except Exception as e:
            # Gestion des erreurs SQL
            st.error(f"Erreur dans la requête SQL : {e}")
    else:
        st.warning(f"Veuillez entrer une requête SQL.")

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")