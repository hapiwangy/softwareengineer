# 這裡負責和帳號有關的資料庫操作
import sqlite3
import logging
# 製造出可以用的sql sentence
def addingUser()-> None:
    informations = [
        ['happy', 'happy123','happy123'],
        ['tom', 'tom123', 'tom123'],
        ['happy','kevin123', 'kevin123'],
        ['tom','sherry123','sherry123']
    ]
    for info in informations:
        print(f'''INSERT INTO users VALUES('{info[0]}', '{info[1]}', '{info[2]}')''')
# 建置資料庫
def dbaccountinitial()-> None:
    logging.debug("database initializing")
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    # 創建一個table用來存放使用者資料
    cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
            groupname TEXT,
            username TEXT,
            password TEXT,
            admin INTEGER
        )
        ''')
    con.commit()
    con.close()
    logging.debug("database initialize successful")
# 增加資料
def add_account(groupname: str, username: str, password: str, isAdmin: int):
    con = sqlite3.connect("./static/data.db")
    cur = con.cursor()
    # 尋找和現在group相同的所有username
    samegusername = cur.execute(f"SELECT username FROM users WHERE groupname='{groupname}'")
    samegusername = fixfetch(samegusername)
    if username in samegusername:
        con.close()
        return False
    cur.execute(f'''
        INSERT INTO users (groupname, username, password, admin) VALUES ('{groupname}', '{username}', '{password}', {isAdmin})
    ''')
    con.commit()
    con.close()
    return True
# 把fecth的資料做一下整理
def fixfetch(beingfetch:list[tuple])-> list[str]:
    return [x[0]for x in beingfetch]
# 確認是否登入成功
def logincheck(groupname:str, username: str, password:str)-> (bool, bool):
    # 回傳(登入成功, 是否是admin)
    con = sqlite3.connect("./static/data.db")
    cur = con.cursor()
    specificaccount = cur.execute(f"SELECT password, admin FROM users WHERE groupname='{groupname}' AND username='{username}' ")
    specificaccount = list(specificaccount.fetchall())
    if not specificaccount:
        con.close()
        return False, False
    if  password != specificaccount[0][0]:
        con.close()
        return False, False
    else:
        con.close()
        return True, bool(specificaccount[0][1])

# 確認group的是否存在
def check_group_exist(groupname: str)->bool:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    det = cur.execute(f'''
        SELECT groupname from users
    ''')
    det = [x[0] for x in list(det.fetchall())]
    con.close()
    return groupname in det
# 獲得所有的group
def get_all_group()-> list[str]:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    det = cur.execute(f'''
        SELECT groupname from users
    ''')
    det = [x[0] for x in list(det.fetchall())]
    return list(set(det))

