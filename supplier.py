import streamlit as st
import sqlite3 as sq
import pandas as pd
import requests
import json
# fetch orders made
def incoming():
    res=requests.get("https://boxingsales.herokuapp.com/incoming")
    j_data=json.loads(res.json())
    return pd.DataFrame(j_data)
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
def delete_inc(id):
    conn=sq.connect("dispatch.db")
    con=conn.cursor()
    con.execute("delete from dispatch where id=?",(id,))
    conn.commit()
