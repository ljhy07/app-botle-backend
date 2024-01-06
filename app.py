from flask import Flask, request, session, render_template, redirect
from markupsafe import escape
from db import DB
import base64

app = Flask(__name__)
db = DB()
app.secret_key = '1qaz2wsx3edc'

@app.route('/signup', methods=['POST', 'GET'])
def Signup():
    if request.method == 'POST':
        id = request.form['id']
        nickname = request.form['nickname']
        pwd = request.form['pwd']
        photo = request.files['image']
        
        if photo:
            save_path = base64.b64encode(photo.read())
            db.UserCreateP(id=id, nickname=nickname, pwd=pwd, photo=save_path)
        else:
            db.UserCreate(id=id, nickname=nickname, pwd=pwd)

@app.route('/login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        id = request.form['id']
        pwd = request.form['pwd']
        
        if db.UserSearch(id=id, pwd=pwd):
            session["userId"] = id
            db.cursor.execute('select nickname from user where id=%s', (id))
            session["username"] = db.cursor.fetchall()
        else:
            indexError = 'id or password wrong'

@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.pop("userId", None)
        session.pop('username', None)

@app.route('/nick/modify', methods=['POST', 'GET'])
def nickModify():
    if request.method == 'POST':
        pwd = request.form['pwd']
        new_nick = request.form['newNickname']
        id = escape(session["userId"])

        if db.UserPwdSearch(pwd):
            db.UserNickUpdate(id=id ,nickname=new_nick)

@app.route('/diary/write', method=['POST', 'GET'])
def diaryWrite():
    if request.method == 'POST':
        id = escape(session('userid'))
        nick = escape(session('username'))

        title = request.form['title']
        contents = request.form['contents']
        private = request.form['private']
        category = request.form['category']
        photo = request.files['images']

        if photo:
            save_path = base64.b64encode(photo.read())
            db.DiaryCreateP(id=id, nickname=nick, title=title, contents=contents, private=private, category=category, photo=save_path)
        else:
            db.DiaryCreate(id=id, nickname=nick, title=title, contents=contents, private=private, category=category)

@app.route('/diary/modify', method=['POST', 'GET'])
def diaryModify():
    if request.method == 'POST':
        id = escape(session('userid'))

        title = request.form['title']
        contents = request.form['contents']
        private = request.form['private']
        category = request.form['category']
        photo = request.files['images']

        if photo:
            save_path = base64.b64encode(photo.read())
            db.DiaryUpdatep(id=id, title=title, contents=contents, private=private, category=category, photo=save_path)
        else:
            db.DiaryUpdate(id=id, title=title, contents=contents, private=private, category=category)

@app.route('/diary/search/{sort}/{category}', method=['POST', 'GET'])
def diarySearch():
    if request.method == 'GET':
        

if __name__ == '__main__':
    app.run(debug=True)