import sqlite3
import pandas as pd
def logs(name,username,password):
        conn=sqlite3.connect("logs.db")
        con=conn.cursor()
        con.execute("create table if not exists log(name string,empid string,password string)")
        con.execute("insert into log (name,empid,password) values (?,?,?)",(name,username,password,))
        conn.commit()
def retrv_log():
    conn=sqlite3.connect("logs.db")
    con=conn.cursor()
    con.execute("select *from log")
    values=con.fetchall()
    names=["name","empid","password"]

    auths=pd.DataFrame(values,columns=names)
    return list(auths.name),list(auths.empid),list(auths.password)
