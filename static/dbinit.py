# 這裡初始化資料庫和資料
import sqlite3
import account_functions as saf
import showcontent_functions as ssf
import os
# 要先把db關閉掉才用這個檔案進行清除(不然會找不到那檔案)
# logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    try:
        os.remove("./static/data.db")
        print('file removed successful')
    except:
        print('no such file')
    saf.dbaccountinitial()
    ssf.dbshowinitial()
    ssf.dbpostinitial()
    ssf.dbcommentitial()
    con = sqlite3.connect("./static/data.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (groupname, username, password, admin) VALUES('happy', 'happy123', 'happy123', 1)")
    cur.execute("INSERT INTO users (groupname, username, password, admin) VALUES('tom', 'tom123', 'tom123',1)")
    cur.execute("INSERT INTO users (groupname, username, password, admin) VALUES('happy', 'kevin123', 'kevin123', 0)")
    cur.execute("INSERT INTO users (groupname, username, password, admin) VALUES('tom', 'sherry123', 'sherry123', 0)")
    cur.execute("INSERT INTO Accounting (date, thing, expense, member, groupname, isDanger) VALUES('2023-07-07','heart','1000','happy123','happy',1)")
    cur.execute("INSERT INTO Accounting (date, thing, expense, member, groupname, isDanger) VALUES('2023-08-07','square','1000','tom123','tom',0)")
    cur.execute("INSERT INTO Accounting (date, thing, expense, member, groupname, isDanger) VALUES('2023-09-07','spade','1000','kevin123','happy',0)")
    cur.execute("INSERT INTO Accounting (date, thing, expense, member, groupname, isDanger) VALUES('2023-10-07','clubs','1000','sherry123','tom',0)")
    cur.execute("INSERT INTO posts (groupname, username, postcontent) VALUES ('happy', 'happy123', 'today is a good day to die owo')")
    cur.execute("INSERT INTO posts (groupname, username, postcontent) VALUES ('happy', 'happy123', 'from today i am a broken dog woo, woo.')")
    cur.execute("INSERT INTO posts (groupname, username, postcontent) VALUES ('tom', 'tom123', 'today is a good day to die dddddd owo')")
    cur.execute("INSERT INTO comments (postcontent, groupname, username, comment) VALUES ('today is a good day to die owo', 'happy', 'kevin123', 'cool bro')")
    cur.execute("INSERT INTO comments (postcontent, groupname, username, comment) VALUES ('today is a good day to die owo', 'tom', 'tom123', 'lol')")
    cur.execute("INSERT INTO comments (postcontent, groupname, username, comment) VALUES ('today is a good day to die owo', 'happy', 'kevin123', 'ha ha!')")
    con.commit()
    con.close()