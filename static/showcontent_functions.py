import sqlite3
import logging
# 這裡處理和記帳有關的資料庫操作
# 初始化需要用到的table
def dbshowinitial()->None:
    logging.debug("initial showconten table")
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS Accounting (
            date TEXT,
            thing TEXT,
            expense TEXT,
            member TEXT,
            groupname TEXT
        )''')
    con.commit()
    con.close()
    logging.debug("initial Successful")
# 製造出可以用的句子
def addingdata()->None:
    informations = [
        [ '2023/07/07', 'heart','1000','happy123','happy'],
        [ '2023/08/07', 'square','1000','tom123','tom'],
        [ '2023/09/07', 'spade','1000','kevin123','happy'],
        [ '2023/10/07', 'clubs','1000','sherry123','tom']
    ]
    for info in informations:
        print(f'''INSERT INTO Accounting VALUES('{info[0]}','{info[1]}','{info[2]}','{info[3]}','{info[4]}')''')

# 取得某個組織的所有資料
def getgroupdata(groupname: str)->list:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    values = cur.execute(f'''
                SELECT * from Accounting WHERE groupname='{groupname}'
                         ''')
    values = values.fetchall()
    con.close()
    return values
# 增加一項新的東西到記帳本裡面
def addthing(date:str, thing:str, expense:str, member:str, groupname:str)->bool:
    try :
        con = sqlite3.connect('./static/data.db')
        cur = con.cursor()
        cur.execute(f'''
                    INSERT INTO Accounting VALUES(?, ?, ?, ?, ?)
                    ''', (date, thing, expense, member, groupname))
        con.commit()
        con.close()
        return True
    except:
        return False
