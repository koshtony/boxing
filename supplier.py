import streamlit as st
import sqlite3 as sq
import pandas as pd
# fetch orders made
def incoming():
    sc_data=pd.read_html("https://boxingsales.herokuapp.com/data")
    return sc_data
def download(data):
    return data.to_csv().encode('utf-8')
