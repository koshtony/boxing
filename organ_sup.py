import streamlit as st
import sqlite3
import pandas as pd
import time
def menu2(col1,col2,col3):
    exp=col3.expander("Supply field")
    exp.write("""**About**""")
    radc2=col3.selectbox("",["fetch","add","edit","delete"])
    if radc2=="add":
        # add product info
        name=col3.text_input("product name")
        desc=col3.text_input("product descriptions")
        if col3.button("add product"):
            col3.write("---Adding product--->")
            progress=col3.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            add_prod(name,desc)
            col3.write("product Added successfully")
    elif radc2=="fetch":
        # input search by product id
        search=col3.text_input("search by product id")
        if col3.button("fetch product"):
            col3.write("searching product")
            progress=col3.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            st.write(fetch_prod(search))

    elif radc2=="edit":
        # input edit by product id
        edit_p_id=col3.text_input("edit by product id")
        change=col3.selectbox("field to edit",["name","desc"])
        sets=col3.text_input("new value")
        if col3.butoon("edit product"):
            progress=col3.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            edit_prod(change,sets,edit,p_id)
    elif radc2=="delete":
        p_id=col3.text_input("product id to delete")
        if col3.button("delete product"):
            col3.write("----deleting product --->")
            progress=col3.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i+1)
            delete_prod(p_id)
def add_prod(name,desc):
    # sqlite add employee info code here
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    con.execute("create table if not exists orgsupply(pid integer primary key autoincrement,name text,description text)")
    con.execute("insert into orgsupply (name,description) values (?,?)",(name,desc,))
    conn.commit()


def fetch_prod(id):
    # sqlite fetch code here
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    con.execute("select *from orgsupply where pid=?",(id,))
    values=con.fetchall()
    names=["pid","name","description"]
    val_dict={}
    for i in range(len(names)):
        val_dict[names[i]]=values[0][i]

    return pd.DataFrame(val_dict,index=[0])

def edit_prod(val,set,id):
    # sqlite edit code
    conn=sqlite3.connect("organ.db")
    con=conn.cursor()
    cmd="update orgsupply set "+str(val)+" =? "+"where pid=?"
    con.execute(cmd,(set,id,))
    conn.commit()

def delete_prod(id):
     # delete products by id.
     conn=sqlite3.connect("organs.db")
     con=conn.cursor()
     con.execute("delete from orgsupply where pid=?",(id,))
