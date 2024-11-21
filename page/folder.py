import streamlit as st
import pandas as pd
import os
from io import BytesIO
import os
import time


def app():
    st.title('IBC Dashboard 📊')

    with st.expander('About this app'):
        st.markdown('**What can this app do?**')
        st.markdown('This app allows you to explore and analyze business data from folders and Excel files.')
        st.markdown('**How to use the app?**')
        st.warning('To engage with the app:\n'
                   '1. Upload your data\n'
                   '2. Navigate through different sections using the sidebar\n'
                   '3. Explore the dashboard')

    st.header("Introduction")
    st.write("Welcome to the IBC Dashboard web app! This tool is designed to help you review and analyze student business data from uploaded Excel files and folders. With a variety of data visualizations and comprehensive summaries, the app provides valuable insights into the key metrics of each student business, making it easier for you to assess their performance.")

    st.subheader("Upload Folder")   

    # Directory to store uploaded files
    uploaded_folder = "uploaded_folders"
    os.makedirs(uploaded_folder, exist_ok=True)

    # HTML input for folder selection (using webkitdirectory for Chrome/Edge)
    st.markdown("""
        <input type="file" id="file_uploader" multiple webkitdirectory directory>
        <script>
            const fileUploader = document.getElementById("file_uploader");
            fileUploader.addEventListener("change", (event) => {
                const files = event.target.files;
                let data = new FormData();
                for (let i = 0; i < files.length; i++) {
                    data.append("file" + i, files[i]);
                }
                fetch('/upload', { 
                    method: 'POST',
                    body: data 
                });
            });
        </script>
    """, unsafe_allow_html=True)

    def read_excel_from_folder(folder_path):
        # List all files in the folder
        files_wihtin_folder = os.listdir(folder_path)
        
        # Filter for Excel files
        excel_files = [file for file in files_wihtin_folder if file.endswith(('.xlsx', '.xls', '.xlsm'))]
        
        # If no Excel files found, return an empty list
        if not excel_files:
            print("No Excel files found in the folder.")
            return []
        
        # Read each Excel file into a dictionary of DataFrames (one per sheet)
        dataframes = {}
        for excel_file in excel_files:
            file_path = os.path.join(folder_path, excel_file)
            
            try:
                # Read all sheets from the Excel file into a dictionary of DataFrames
                sheets_dict = pd.read_excel(file_path, sheet_name=None)  # `sheet_name=None` reads all sheets
                dataframes[excel_file] = sheets_dict
                print(f"Successfully read: {excel_file} with {len(sheets_dict)} sheets.")
            except Exception as e:
                print(f"Error reading {excel_file}: {e}")
        
        return dataframes

    # Example usage
    folder_path = 'uploaded_folders'  # Replace with the path to your folder
    dataframes = read_excel_from_folder(folder_path)

    # Optionally, display the sheets in the first file
    if dataframes:
        for sheet_name, df in dataframes[list(dataframes.keys())[0]].items():
            print(f"Sheet: {sheet_name}")
            print(df.head())  # Display first few rows of each sheet



    # Title of the app
    st.subheader("Upload File")

    # File uploader widget
    uploaded_file = st.file_uploader("Select Excel File", type=['xlsx', 'xlsm', 'csv'])

    if uploaded_file is not None:
        # Get the file name
        file_path = os.path.join(uploaded_folder, uploaded_file.name)
        
        # Save the uploaded file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Store the file path in session state (optional, if you want to keep track in the session)
        st.session_state.uploaded_file = file_path

        # Read the file into a DataFrame
        if file_path.endswith(('.xlsx', '.xlsm')):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        
        # Display the dataframe (optional)
        st.write(df)

        # Show progress bar (optional)
        progress_bar = st.progress(0)

        for per_completed in range(100):
            time.sleep(0.0005)
            progress_bar.progress(per_completed + 1)

            if per_completed == 99:
                st.markdown("""
                <style>
                .stProgress > div > div > div > div {
                    background-color: green;
                }
                </style>
                """, unsafe_allow_html=True)
        
    else:
        # Check if there's an existing uploaded file from the session
        if 'uploaded_file' in st.session_state:
            file_path = st.session_state.uploaded_file
            # Check if file exists
            if os.path.exists(file_path):
                # Load the file back into a DataFrame
                if file_path.endswith(('.xlsx', '.xlsm')):
                    df = pd.read_excel(file_path)
                elif file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                
                # Display the DataFrame again
                st.write(df)



    




    

    # if uploaded_file1 is not None:
    #     # Store the file in session state
    #     st.session_state.uploaded_file = uploaded_file1
    #     df = pd.read_excel(uploaded_file1)
        
    #     progress_bar = st.progress(0)

    #     for per_completed in range(100):
    #         time.sleep(0.0005)
    #         progress_bar.progress(per_completed + 1)

    #         if per_completed == 99:
    #             st.markdown("""
    #             <style>
    #             .stProgress > div > div > div > div {
    #                 background-color: green;
    #             }
    #             </style>
    #             """, unsafe_allow_html=True)

    #     st.success("File Uploaded Successfully!")
    #     st.write("You can click on the different dashboards on the left under ***Navigation*** to see the different dashboards.")


    # st.markdown("[GitHub Repository](https://github.com/TylerEnglish/ibc-business-tracker)")

if __name__ == "__main__":
    app()