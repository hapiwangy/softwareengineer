from flask import Flask, render_template, request
import sqlite3
import static.functions as sf

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

sf.databaseinitial()


# login page
@app.route('/', methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        from_data = request.form
        # 確認是否有登入成功
        groupname = from_data.get('groupname')
        username = from_data.get('username')
        password = from_data.get('password')
        check = sf.logincheck(groupname, username, password)
        if check:
            return render_template('showcontent.html')
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
        check = sf.add_account(groupname, username, password)
        if check:
            return render_template('signup.html', show='Successful')
        else:
            return render_template('signup.html', show="Fail")
    return render_template('signup.html')

# show accounting table
@app.route('/showcontent', methods=['GET','POST'])
def showcontent():
    return render_template('showcontent.html')

if __name__ == '__main__':
    app.run(debug=True)