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
    groups = saf.get_all_group()
    if request.method == 'POST':
        from_data = request.form
        # 確認是否有登入成功
        groupname = from_data.get('groupname')
        username = from_data.get('username')
        password = from_data.get('password')
        check, isAdmin = saf.logincheck(groupname, username, password)
        if check:
            # 如果登入成功的話要先去資料庫拿該組織的記帳資料，然後傳給。
            return redirect(url_for('showcontent', username=username, groupname=groupname, isAdmin = isAdmin))
        else:
            return render_template('login.html', show='Login Fail', groups=groups)
    return render_template('login.html', groups = groups)

# sign up page
@app.route('/signup', methods=['GET','POST'])
def signup():
    groups = saf.get_all_group()
    if request.method == 'POST':
        form_data = request.form
        groupname = form_data.get('groupname')
        username = form_data.get('username')
        password = form_data.get('password')
        # 設定一個變數紀錄是不是創建成功
        check = saf.add_account(groupname, username, password, 0)
        if check:
            return render_template('signup.html', show='Successful', groups=groups)
        else:
            return render_template('signup.html', show="Fail", groups=groups)
    return render_template('signup.html', groups=groups)

# show accounting table
@app.route('/showcontent/<username>/<groupname>/<int:isAdmin>', methods=['GET','POST'])
def showcontent(username, groupname, isAdmin):
    dbdata = ssf.getgroupdata(groupname)
    posts = ssf.getposts()
    if request.method == "POST":
        if 'addthing' in request.form:
            form_data = request.form
            check = ssf.addthing(form_data['date'], form_data['thing'], form_data['expense'], form_data['username'], form_data['groupname'])
            dbdata = ssf.getgroupdata(groupname)
            if check:
                return render_template('showcontent.html', username=form_data['username'], groupname=form_data['groupname'], dbdata=dbdata, isAdmin=isAdmin, posts=posts)
        elif 'switchbutton' in request.form:
            form_data = request.form
            # 更新狀態
            form_data = [x for x in form_data]
            ssf.updatestatus(form_data)
            dbdata = ssf.getgroupdata(groupname)
            return render_template('showcontent.html', username=username, groupname=groupname, dbdata=dbdata, isAdmin = isAdmin, posts=posts) 
        elif 'deletebutton' in request.form:
            form_data = request.form
            # 更新狀態
            form_data = [x for x in form_data]
            ssf.deleteitem(form_data)
            dbdata = ssf.getgroupdata(groupname)
            return render_template('showcontent.html', username=username, groupname=groupname, dbdata=dbdata, isAdmin = isAdmin, posts=posts) 
        elif 'addpost' in request.form:
            form_data = request.form
            ssf.addpost(form_data['groupname'], form_data['username'] ,form_data['postcontent'])
            # 獲得更新後的posts
            posts = ssf.getposts()
            return render_template('showcontent.html', username=username, groupname=groupname, dbdata=dbdata, isAdmin = isAdmin, posts=posts)
        elif 'deletepost' in request.form:
            form_data = request.form
            ssf.deleteposts(form_data['groupname'], form_data['username'] ,form_data['postcontent'])
            posts = ssf.getposts()
            return render_template('showcontent.html', username=username, groupname=groupname, dbdata=dbdata, isAdmin = isAdmin, posts=posts)
        elif 'showfullpost' in request.form:
            form_data = request.form
            print(form_data)
            return redirect(url_for('showallpost', groupname=form_data['groupname'], username=form_data['username'] ,postcontent=form_data['postcontent'],cgroupname=form_data['cgroupname'],cusername=form_data['cusername'], isAdmin=isAdmin))
        elif 'logout' in request.form:
            return redirect(url_for('home'))
        
    return render_template('showcontent.html', username=username, groupname=groupname, dbdata=dbdata, isAdmin = isAdmin, posts=posts)

# adding new admin (one group one admin)
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        form_data = request.form
        groupname = form_data.get('groupname')
        username = form_data.get('username')
        password = form_data.get('password')
        # 確定這個組織有沒有存在(是否已經有admin了)
        check_is_used = saf.check_group_exist(groupname)
        if not check_is_used:
            _ = saf.add_account(groupname, username, password, 1)
            return render_template('adminsignup.html', show='Successful')
        else:
            return render_template('adminsignup.html', show="Fail")
    return render_template('adminsignup.html')

# open comment page
@app.route('/showallpost/<groupname>/<username>/<postcontent>/<cgroupname>/<cusername>/<int:isAdmin>', methods=['GET','POST'])
def showallpost(groupname: str, username: str, postcontent: str, cgroupname: str, cusername: str, isAdmin: int):
    # 取得當前貼文相關的所有留言
    all_comments = ssf.getallcomment(postcontent)
    if request.method == 'POST':
        if 'addnewcomment' in request.form:
            form_data = request.form
            ssf.addnewcomment(postcontent, cgroupname, cusername, form_data['newcomment'])    
            all_comments = ssf.getallcomment(postcontent)
            return render_template('PostnComment.html',groupname=groupname, username=username, postcontent=postcontent, cgroupname=cgroupname, cusername=cusername, all_comments=all_comments, isAdmin=isAdmin)
        elif 'deletecomment' in request.form:
            form_data = request.form
            ssf.deletecomment(form_data['postcontent'], form_data['groupname'],form_data['username'],form_data['comment'])
            all_comments = ssf.getallcomment(postcontent)
            return render_template('PostnComment.html',groupname=groupname, username=username, postcontent=postcontent, cgroupname=cgroupname, cusername=cusername, all_comments=all_comments, isAdmin=isAdmin)
        elif 'backtoall' in request.form:
            form_data = request.form
            return redirect(url_for('showcontent', groupname=groupname, username=username, isAdmin=isAdmin))
    return render_template('PostnComment.html',groupname=groupname, username=username, postcontent=postcontent, cgroupname=cgroupname, cusername=cusername, all_comments=all_comments, isAdmin=isAdmin)

if __name__ == '__main__':
    app.run(debug=True)