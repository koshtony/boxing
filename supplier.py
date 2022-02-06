import streamlit as st
import sqlite3 as sq
import pandas as pd
# fetch orders made
def incoming():
    sc_data=pd.read_html("https://boxingsales.herokuapp.com/data")
    return sc_data
def download(data):
    return data.to_csv().encode('utf-8')
def dispatch(data,sel):
    sel_data=data.loc[data["id"]==sel]
    con=sq.connect("dispatch.db")
    sel_data.to_sql(name="dispatch",con=con,if_exists="append")
    con2=sq.connect("dispatch.db")
    sel_data=pd.read_sql_query('select *from dispatch',con2)
    # delete from incoming
    return sel_data
