import streamlit as st
import sqlite3 as sq
import pandas as pd
# fetch orders made
def incoming():
    db=sq.connect("suppliers.db")
    con=db.cursor()
    con.execute("select *from orders")
    values=con.fetchall()
    names=["Order Id","emp id","name","phone","item","shop","region","quantity","Order Date","Type","User"]
    return pd.DataFrame(values,columns=names)
def download(data):
    return data.to_csv().encode('utf-8')
