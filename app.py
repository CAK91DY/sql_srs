import streamlit as st
import pandas as pd
import duckdb

# Table 1 : Exemple de données des clients
client = {
    "client_id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
}
client = pd.DataFrame(client)

# Table 2 : Exemple de données des commands
commands = {
    "order_id": [101, 102, 103],
    "client_id": [1, 2, 4],  # Remarque : le client_id 4 ne correspond pas à la table df1
    "amount": [250, 150, 300],
}
commands = pd.DataFrame(commands)

answer = ("""
    SELECT * FROM client l
    JOIN commands c
    ON l.client_id = c.client_id
""")
solution = duckdb.sql(answer).df()


with st.sidebar:
    option = st.selectbox(
        "What would you like review ?",
        ("Joins", "GroupBy", "Windows functions"),
        index=None,
        placeholder="Select a theme...",
    )

    st.write("You selected:", option)

st.header("Enter your code:")
query = st.text_area(label="Votre code SQL ici", key="user_input")
if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

tab1, tab2 = st.tabs(["Tables", "Solution"])
with tab1:
    st.write("table: clients")
    st.dataframe(client)
    st.write("table: commands")
    st.dataframe(commands)
    st.write("expected:")
    st.dataframe(solution)


with tab2:
    st.write(answer)

