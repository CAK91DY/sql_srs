# pylint: disable=missing-module-docstring
import streamlit as st
import pandas as pd
import duckdb
import ast

con = duckdb.connect(database='data/exercises_sql_tables.duckdb', read_only=False)


with st.sidebar:
    option = st.selectbox(
        "What would you like review ?",
        ("cross_joins", "GroupBy", "windows_functions"),
        index=None,
        placeholder="Select a option...",
    )
    st.write("You selected:", option)
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{option}' ").df()
    st.write(exercise)

st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)



tab1, tab2 = st.tabs(["Tables", "Solution"])
with tab1:
    #st.write(exercise.loc[0, "tables"])
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"tables : {table}")
        df_table = con.sql(f" SELECT * FROM {table} ")
        st.dataframe(df_table)

with tab2:
    answer_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{answer_name }.sql", "r") as f:
        answer = f.read()
        solution = con.execute(answer)
    st.write(answer)
    st.dataframe(solution)
