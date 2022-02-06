import pandas as pd
import sqlite3
def display():
    con=sqlite3.connect("suppliers.db")
    df=pd.read_sql_query("select *from orders",con)
    print(df)
def incoming():
    sc_data=pd.read_html("http://127.0.0.1:5000/data")
    return sc_data
print(incoming())
