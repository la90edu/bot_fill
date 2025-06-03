import streamlit as st
import pandas as pd
import connect_to_google_sheet



def init():
    # st.set_page_config(
    #     layout="wide",
    #     page_title="דאשבורד ניתוח נתונים",
    #     page_icon="📊",
    #     initial_sidebar_state="expanded",
    #     menu_items={
    #         'About': "אפליקציה לניתוח נתונים פסיכולוגיים של תלמידים"
    #     }
    # )
    st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6 {
        text-align: right;
        direction: rtl;
    }

    .css-1d391kg { 
        text-align: right; 
    }
    p {
        text-align: right;
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True)
    

   
    data=connect_to_google_sheet.return_data()
    df=pd.DataFrame(data)
    # st.session_state.df=df
   
    return df

