from flask import Flask, render_template, request, redirect, url_for
import static.account_functions as saf
import static.showcontent_functions as ssf
import os
import logging
logging.basicConfig(level=logging.DEBUG)

# 如果之後沒有要default data的話要把下面兩行反註解
# 測試時透過python ./static/dbinit.py來做初始化
# saf.dbaccountinitial()
# ssf.dbshowinitial()

app = Flask(__name__)
# login page
@app.route('/', methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        from_data = request.form
        # 確認是否有登入成功
        groupname = from_data.get('groupname')
        username = from_data.get('username')
        password = from_data.get('password')
        check = saf.logincheck(groupname, username, password)
        if check:
            # 如果登入成功的話要先去資料庫拿該組織的記帳資料，然後傳給。
            return redirect(url_for('showcontent', username=username, groupname=groupname))
        else:
            return render_template('login.html', show='Login Fail')
    return render_template('login.html')

# sign up page
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        form_data = request.form
        groupname = form_data.get('groupname')
        username = form_data.get('username')
        password = form_data.get('password')
        # 設定一個變數紀錄是不是創建成功
        check = saf.add_account(groupname, username, password)
        if check:
            return render_template('signup.html', show='Successful')
        else:
            return render_template('signup.html', show="Fail")
    return render_template('signup.html')

# show accounting table
@app.route('/showcontent/<username>/<groupname>', methods=['GET','POST'])
def showcontent(username, groupname):
    dbdata = ssf.getgroupdata(groupname)
    # dbdata = [list(db) for db in dbdata]
    if request.method == "POST":
        form_data = request.form
        check = ssf.addthing(form_data['date'], form_data['thing'], form_data['expense'], form_data['username'], form_data['groupname'])
        dbdata = ssf.getgroupdata(groupname)
        if check:
            return render_template('showcontent.html', username=form_data['username'], groupname=form_data['groupname'], dbdata=dbdata)
    print(dbdata)
    return render_template('showcontent.html', username=username, groupname=groupname, dbdata=dbdata)

if __name__ == '__main__':
    app.run(debug=True)