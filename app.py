import streamlit as st
import pandas as pd
import pyproj
from io import StringIO

# Funzione per convertire le coordinate
def convert_coordinates(df, longitude, latitude):
    proj = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
    df['UTM_Easting'], df['UTM_Northing'] = proj(longitude, latitude)
    return df

# Funzione per salvare il file convertito in formato CSV
def convert_df_to_csv(df):
    csv = StringIO()
    df.to_csv(csv, index=False)
    csv.seek(0)
    return csv.getvalue()

# Titolo dell'applicazione
st.title("Convertitore di File in CDR")

# Caricamento singolo file
uploaded_file = st.file_uploader("Scegli un file", type=["csv", "xls", "xlsx", "ods", "html"])

# Caricamento multipli file da una cartella
uploaded_files = st.file_uploader("Scegli file multipli", type=["csv", "xls", "xlsx", "ods", "html"], accept_multiple_files=True)

# Input per specificare le coordinate geografiche
longitude = st.number_input("Inserisci la longitudine", format="%.6f")
latitude = st.number_input("Inserisci la latitudine", format="%.6f")

if st.button("Converti"):
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        if file_ext == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_ext in ['xls', 'xlsx', 'ods']:
            df = pd.read_excel(uploaded_file)
        elif file_ext == 'html':
            df = pd.read_html(uploaded_file)[0]

        df = convert_coordinates(df, longitude, latitude)
        csv = convert_df_to_csv(df)
        st.download_button(label="Scarica il file convertito", data=csv, file_name=f"{uploaded_file.name.split('.')[0]}.cdr", mime='text/csv')

    if uploaded_files is not None:
        for file in uploaded_files:
            file_ext = file.name.split('.')[-1].lower()
            if file_ext == 'csv':
                df = pd.read_csv(file)
            elif file_ext in ['xls', 'xlsx', 'ods']:
                df = pd.read_excel(file)
            elif file_ext == 'html':
                df = pd.read_html(file)[0]

            df = convert_coordinates(df, longitude, latitude)
            csv = convert_df_to_csv(df)
            st.download_button(label=f"Scarica {file.name.split('.')[0]}.cdr", data=csv, file_name=f"{file.name.split('.')[0]}.cdr", mime='text/csv')
