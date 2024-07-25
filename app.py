import streamlit as st
import pandas as pd
import pyproj
from pathlib import Path
import os

# Funzione per convertire le coordinate
def convert_coordinates(df, longitude, latitude):
    proj = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
    df['UTM_Easting'], df['UTM_Northing'] = proj(longitude, latitude)
    return df

# Funzione per salvare il file convertito
def save_file(df, output_path):
    df.to_csv(output_path, index=False)

# Titolo dell'applicazione
st.title("Convertitore di File in CDR")

# Caricamento singolo file
uploaded_file = st.file_uploader("Scegli un file", type=["csv", "xls", "xlsx", "ods", "html"])

# Caricamento multipli file da una cartella
uploaded_files = st.file_uploader("Scegli file multipli", type=["csv", "xls", "xlsx", "ods", "html"], accept_multiple_files=True)

# Variabile di stato per il percorso della cartella di output
if 'output_dir' not in st.session_state:
    st.session_state.output_dir = "output"

# Pulsante per selezionare la cartella di output
if st.button("Seleziona Cartella di Output"):
    selected_folder = st.text_input("Inserisci il percorso della cartella di output")
    if selected_folder:
        st.session_state.output_dir = selected_folder
        st.success(f"Cartella di output selezionata: {st.session_state.output_dir}")

# Casella di testo per la cartella di output
output_dir = st.text_input("Cartella di Output", value=st.session_state.output_dir)

# Input per specificare le coordinate geografiche
longitude = st.number_input("Inserisci la longitudine", format="%.6f")
latitude = st.number_input("Inserisci la latitudine", format="%.6f")

# Pulsante per convertire i file
if st.button("Converti"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Selezione del file singolo
    if uploaded_file is not None:
        file_ext = Path(uploaded_file.name).suffix.lower()
        if file_ext == '.csv':
            df = pd.read_csv(uploaded_file)
        elif file_ext in ['.xls', '.xlsx', '.ods']:
            df = pd.read_excel(uploaded_file)
        elif file_ext == '.html':
            df = pd.read_html(uploaded_file)[0]

        df = convert_coordinates(df, longitude, latitude)
        output_file_path = os.path.join(output_dir, f"{Path(uploaded_file.name).stem}.cdr")
        save_file(df, output_file_path)
        st.success(f"File convertito e salvato in {output_file_path}")

    # Selezione di file multipli
    if uploaded_files is not None:
        for file in uploaded_files:
            file_ext = Path(file.name).suffix.lower()
            if file_ext == '.csv':
                df = pd.read_csv(file)
            elif file_ext in ['.xls', '.xlsx', '.ods']:
                df = pd.read_excel(file)
            elif file_ext == '.html':
                df = pd.read_html(file)[0]

            df = convert_coordinates(df, longitude, latitude)
            output_file_path = os.path.join(output_dir, f"{Path(file.name).stem}.cdr")
            save_file(df, output_file_path)
            st.success(f"File {file.name} convertito e salvato in {output_file_path}")
