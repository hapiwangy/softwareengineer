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
    con = sqlite3.connect("./static/data.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES('happy', 'happy123', 'happy123')")
    cur.execute("INSERT INTO users VALUES('tom', 'tom123', 'tom123')")
    cur.execute("INSERT INTO users VALUES('happy', 'kevin123', 'kevin123')")
    cur.execute("INSERT INTO users VALUES('tom', 'sherry123', 'sherry123')")
    cur.execute("INSERT INTO Accounting VALUES('2023/07/07','heart','1000','happy123','happy')")
    cur.execute("INSERT INTO Accounting VALUES('2023/08/07','square','1000','tom123','tom')")
    cur.execute("INSERT INTO Accounting VALUES('2023/09/07','spade','1000','kevin123','happy')")
    cur.execute("INSERT INTO Accounting VALUES('2023/10/07','clubs','1000','sherry123','tom')")
    con.commit()
    con.close()