# Import required libraries and dependencies
import os
import json
from web3 import Web3
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from pathlib import Path
import numpy as np
from PIL import Image
import base64
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text
from sqlalchemy import insert

############Streamlit Code #########################

## Load the environment variables 
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

## Load the Contract
@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path('/Users/anushasundararajan-tzpc-lm00031/final_code/LCA/code_for_NFTs/contracts/compiled/tokens_abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract = load_contract()


##Write Cap table to CSV 
def captableToCSV(_asset, _fullname, _walletAddress, _contribution):
    data = {'Asset': _asset, 'fullName': _fullname, 'walletAddress' : _walletAddress, 'contribution': _contribution}
    df = pd.DataFrame(data,  index=[0])
    df.to_csv('captable.csv', encoding='utf-8', index=False)
      
## select cap table info 
def view_cap_table_data():
    df = pd.read_csv('captable.csv')
    st.table(df)

def main_page():
    ##Function to set up background image 
    @st.cache(allow_output_mutation=True)
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def set_png_as_page_bg(png_file):
            bin_str = get_base64_of_bin_file(png_file) 
            page_bg_img = '''
            <style>
            .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: scroll; # doesn't work
            }
            </style>
            ''' % bin_str
    
            st.markdown(page_bg_img, unsafe_allow_html=True)
            return

    # Set up Background Image 
    set_png_as_page_bg('image_2.png')

    ##Function to display PDF
    def show_pdf(file_path):
        with open(file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="600" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)


    # Load the data into a Pandas DataFrame
    df_movie_data = pd.read_csv(
        Path("Movie-Projects.csv"), index_col = 'Name')

    ## Set up the title in black
    st.markdown(f'<h1 style="color:#FF5733;font-size:40px;">{"Lights Camera Action"}</h1>', unsafe_allow_html=True)
    ## Set up the subtitle in black
    st.markdown(f'<h2 style="color:#F78066;font-size:24px;">{"Movie funding made easy!"}</h2>', unsafe_allow_html=True)

    ## Set up image for Movie 1
    image_1 = Image.open('film_projects/bgro/bgro.png')
    st.image(image_1, width=400)

    st.markdown(f'<p style="color:#c5b9cd;font-size:20px;">{"Bach Gaye Re Obama (BGRO) is a sequel to the hit film Phas Gaye Re Obama (PGRO). BGRO is a fast paced, fun-filled , hilarious gangster based satirical comedy, larger in scale and scope than its prequel. The story deals with the problems faced by a maid who is ‘used’ by the powerful diplomats abroad and how her challenging their might shakes the corridors of power both in India and the US."}</p>', unsafe_allow_html=True)

    ## Table with artist details for Movie-1
    st.table(df_movie_data.iloc[0])

    ## More details - Display PDF                  
    if st.button('Get Details on Movie-1 >>'):
        show_pdf('film_projects/bgro/synopsis.pdf')

    ## Set up image for Movie 2
    image_2 = Image.open('film_projects/pgro/pgro.png')
    st.image(image_2, width=400)

    st.markdown(f'<p style="color:#c5b9cd;font-size:20px;">{"The movie is a comedy with satire on recession. The story revolves around a Non-resident- Indian (NRI), Om Shashtri, who lived the American dream and made it big in the US. Then one day, as it happened in America, US economy went into recession and overnight big businesses, banks, and financial institutions crashed."}</p>', unsafe_allow_html=True)

    ## Table with artist details for Movie-2
    st.table(df_movie_data.iloc[1])

    if st.button('Get Details on Movie-2 >>'):
        show_pdf('film_projects/pgro/synopsis.pdf')

    ## Set up image for movie 3
    image_3 = Image.open('film_projects/sjsm/sjsm.png')
    st.image(image_3, width=400)

    def show_pdf(file_path):
        if st.button('Get Details on Movie-3 >>'):
            show_pdf('film_projects/sjsm/synopsis.pdf')


##### Side bar nav for filling out contribution 
def page2():

    @st.cache
    def get_table(table: str, filename:str) :
        table_name = pd.read_csv(filename)
        return table

    df = get_table( 'df', 'captable.csv')
    df = pd.read_csv('captable.csv')

    def write_to_file(df1) :
        df1.to_csv('captable.csv', encoding='utf-8', index=False)
        st.write(df1)

    def collectinfo():
    ##with st.form ("Collecting User Information"):
        option = st.selectbox('Which movie you would like to fund?', ('bgro', 'pgro', 'sjsm'))
        full_name= st.text_input("Full Name")
        wallet_address= st.text_input("Ethereum wallet address")
        amount= st.number_input("USD/ETH")
        submit = st.button("submit") 
        if submit: 
             st.write( "Deposit to 0x19b5d8DaBC9e08eE422D01FF1e7D1bA6aA81B704")
             new_data = {'Asset': option, 'fullname':full_name, 'wallet_address': wallet_address, 'amount': amount, 'deposit_to_address': '0x19b5d8DaBC9e08eE422D01FF1e7D1bA6aA81B704' }
             df1 = df.append(new_data, ignore_index=True)
             write_to_file(df1)
        else : 
            st. write("Please fill form")
         

    collectinfo()
  


page_names_to_funcs = {
    "Movie Project Information": main_page,
    "Contribution": page2
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()








