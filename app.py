import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

st.title("Registro")

def load_existing_data(worksheet_name):
    existing_data = conn.read(worksheet=worksheet_name, usecols=list(range(11)), ttl=5)
    return existing_data.dropna(how="all")
    
existing_data_reservations = load_existing_data("Folha")

with st.form(key="vendor_form"):
    name = st.text_input(label="Name")

    submit_button = st.form_submit_button(label="Submit Details")
    if submit_button:
        submission_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {
            "Name": name,
        }

        new_rows = existing_data_reservations.to_dict(orient="records")
        new_rows.append(new_row)

        conn.update(worksheet="Folha", data=new_rows)

        st.success("Details successfully submitted!")
