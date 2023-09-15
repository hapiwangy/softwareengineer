import sqlite3
import logging
# 建置資料庫
def databaseinitial()-> None:
    logging.debug("database initializing")
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    # 創建一個table用來存放使用者資料
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            groupname TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    con.commit()
    con.close()
    logging.debug("database initialize successful")
# 增加資料
def add_account(groupname: str, username: str, password: str):
    con = sqlite3.connect("./static/data.db")
    cur = con.cursor()
    # 尋找和現在group相同的所有username
    samegusername = cur.execute(f"SELECT username FROM users WHERE groupname='{groupname}'")
    samegusername = fixfetch(samegusername)
    if username in samegusername:
        con.close()
        return False
    cur.execute(f'''
        INSERT INTO users VALUES ('{groupname}', '{username}', '{password}')
    ''')
    con.commit()
    con.close()
    return True
# 把fecth的資料做一下整理
def fixfetch(beingfetch:list[tuple])-> list[str]:
    return [x[0]for x in beingfetch]
# 確認是否登入成功
def logincheck(groupname:str, username: str, password:str)-> bool:
    con = sqlite3.connect("./static/data.db")
    cur = con.cursor()
    specificaccount = cur.execute(f"SELECT password FROM users WHERE groupname='{groupname}' AND username='{username}' ")
    specificaccount = list(specificaccount.fetchall())
    if not specificaccount:
        con.close()
        return False
    specificaccount = specificaccount[0]
    if  password != specificaccount[0]:
        con.close()
        return False
    else:
        con.close()
        return True
    
