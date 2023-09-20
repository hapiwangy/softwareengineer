import sqlite3
import logging
# 這裡處理和記帳有關的資料庫操作
# 初始化需要用到的table
def dbshowinitial()->None:
    logging.debug("initial showcontent table")
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS Accounting (
            date TEXT,
            thing TEXT,
            expense TEXT,
            member TEXT,
            groupname TEXT,
            isDanger INTEGER
        )''')
    con.commit()
    con.close()
    logging.debug("initial Successful")
# 初始化comment table
def dbcommentitial()->None:
    logging.debug('initial comment table')
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS comments (
        postcontent TEXT,
        groupname TEXT,
        username TEXT,
        comment TEXT        
        )''')
    con.commit()
    con.close()
# 獲得所有的comment
def getallcomment(postcontent: str)-> list[tuple]:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    data = cur.execute(f'''
        SELECT * FROM comments WHERE postcontent='{postcontent}' 
    ''')
    data = data.fetchall()
    con.close()
    return data
# 新增一個comment
def addnewcomment(postcontent: str, groupname: str, username: str, comment: str)-> None:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute(f'''
       INSERT INTO comments VALUES('{postcontent}', '{groupname}', '{username}','{comment}')         
    ''')
    con.commit()
    con.close()

# 刪除掉一個comment
def deletecomment(postcontent: str, groupname: str, username: str, comment: str)-> None:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute(f'''
        DELETE FROM comments
        WHERE groupname='{groupname}' AND username='{username}' AND postcontent='{postcontent}' AND comment='{comment}'       
    ''')
    con.commit()
    con.close()
# 初始化post table
def dbpostinitial()->None:
    logging.debug("initial postcontent table")
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS posts (
            groupname TEXT,
            username TEXT,
            postcontent TEXT
        )''')
    con.commit()
    con.close()
    logging.debug("initial Successful")
# 增加一個post
def addpost(groupname:str, username:str, postcontent:str)->None:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute(f'''
                INSERT INTO posts (groupname, username, postcontent)
                VALUES ('{groupname}', '{username}', '{postcontent}')
                ''')
    con.commit()
    con.close()
# 獲得目前所有的posts
def getposts()-> list[dict]:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    values = cur.execute(f'''
                SELECT * from posts
                         ''')
    values = values.fetchall()
    con.close()
    return values   
# 刪除某個post
def deleteposts(groupname:str, username:str, postcontent:str):
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute(f'''
        DELETE FROM posts
        WHERE groupname='{groupname}' AND username='{username}' AND postcontent='{postcontent}'
    ''')
    con.commit()
    con.close()  



# 製造出可以用的句子
def addingdata()->None:
    informations = [
        [ '2023/07/07', 'heart','1000','happy123','happy'],
        [ '2023/08/07', 'square','1000','tom123','tom'],
        [ '2023/09/07', 'spade','1000','kevin123','happy'],
        [ '2023/10/07', 'clubs','1000','sherry123','tom']
    ]
    for info in informations:
        print(f'''INSERT INTO Accounting VALUES('{info[0]}','{info[1]}','{info[2]}','{info[3]}','{info[4]}',0)''')

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
                    INSERT INTO Accounting 
                    (date, thing, expense, member, groupname, isDanger)            
                    VALUES(?, ?, ?, ?, ?, ?)
                    ''', (date, thing, expense, member, groupname, 0))
        con.commit()
        con.close()
        return True
    except:
        return False
# 更新某個東西的狀態
def updatestatus(form_data:list)-> None:
    new_state = not int(form_data[4])
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute(f'''
        UPDATE Accounting
        SET isDanger = {new_state}
        WHERE date='{form_data[0]}' AND thing='{form_data[1]}' AND expense='{form_data[2]}' AND member='{form_data[3]}'
    ''')
    con.commit()
    con.close()
# 刪除某個項目
def deleteitem(form_data:list)->None:
    con = sqlite3.connect('./static/data.db')
    cur = con.cursor()
    cur.execute(f'''
        DELETE FROM Accounting
        WHERE date='{form_data[0]}' AND thing='{form_data[1]}' AND expense='{form_data[2]}' AND member='{form_data[3]}' AND groupname='{form_data[5]}'
    ''')
    con.commit()
    con.close()