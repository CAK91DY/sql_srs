# pylint: disable=missing-module-docstring
import os
import logging
import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.debug(os.listdir())
    logging.debug("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run(["python", "init_db.py"])

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

    answer_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{answer_name}.sql", "r") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()



st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution"
        )



tab1, tab2 = st.tabs(["Tables", "Solution"])
with tab1:
    #st.write(exercise.loc[0, "tables"])
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"tables : {table}")
        df_table = con.sql(f" SELECT * FROM {table} ")
        st.dataframe(df_table)
    st.write("expected:")
    st.dataframe(solution_df)

with tab2:
    st.write(answer)
