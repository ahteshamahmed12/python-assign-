import streamlit as st
import pandas as pd
import os
from io import BytesIO

#set up my page
st.set_page_config(page_title="Data sweeper app made by Ahtesham Ahmed", layout="wide", page_icon=":broom:")
st.title("Data Sweeper App")
st.write("Transform your files between csv and excel formats with built-in cleaning and visualizing. Creating the first project in quarter 3")

upload_file = st.file_uploader("Upload your files in CSV or XLSX", ["csv", "xlsx"], accept_multiple_files=True)

if upload_file:
    for file in upload_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("File type not supported")
            continue

        # File detail
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        st.subheader("Data Cleaning")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed")
            with col2:
                if st.button(f"Remove missing values from {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values replaced with column means")

        st.subheader("Select columns to keep")
        columns = st.multiselect(f"Choose columns to keep from {file.name}", df.columns, default=df.columns)
        df = df[columns]

        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])

        st.subheader("File conversion option")
        conversion_type = st.radio(f'Convert {file.name} to', ["csv", "xlsx"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "xlsx":
                df.to_excel(buffer, index=False)
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

            st.download_button(label=f"Click here to download {file_name}", data=buffer, file_name=file_name, mime=mime_type,)

        st.success("All files processed successfully")
