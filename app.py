# pylint: disable=missing-module-docstring
import streamlit as st
import pandas as pd
import duckdb

con = duckdb.connect(database='data/exercises_sql_tables.duckdb', read_only=False)


#ANSWER_STR = """
    #SELECT * FROM client
    #JOIN commands
    #USING(client_id)
#"""
#solution_df = duckdb.sql(ANSWER_STR).df()


with st.sidebar:
    option = st.selectbox(
        "What would you like review ?",
        ("cross_joins", "GroupBy", "windows_functions"),
        index=None,
        placeholder="Select a option...",
    )
    st.write("You selected:", option)
    exercise = con.sql(f"SELECT * FROM memory_state WHERE theme = '{option}' ").df()
    st.write(exercise)

st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="user_input")
