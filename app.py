from flask import Flask, request, session, render_template, redirect, make_response
from markupsafe import escape
from db import DB
import base64

app = Flask(__name__)
db = DB()
app.secret_key = '1qaz2wsx3edc'

@app.route('/signup', methods=['POST', 'GET'])
def Signup():
    if request.method == 'POST':
        data = request.get_json()

        id = data['id']
        nickname = data['nickname']
        pwd = data['pwd']
        
        return db.UserCreate(id=id, nickname=nickname, pwd=pwd)

@app.route('/login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        data = request.get_json()

        id = data['id']
        pwd = data['pwd']
        
        if db.UserSearch(id=id, pwd=pwd):
            resp_id = make_response()
            resp_id.set_cookie('Id', id)

            db.cursor.execute('select nickname from user where id=%s', (id))
            nick = db.cursor.fetchone()

            resp_nick = make_response()
            resp_nick.set_cookie('Nick', nick)
        else:
            indexError = 'id or password wrong'
            return indexError

@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        request.cookies.pop('Id', None)
        request.cookies.pop('Nick', None)

@app.route('/nick/modify', methods=['POST', 'GET'])
def nickModify():
    if request.method == 'POST':
        data = request.get_json()

        pwd = data['pwd']
        new_nick = data['newNickname']
        id = request.cookies.get('Id')

        if db.UserPwdSearch(pwd):
            return db.UserNickUpdate(id=id ,nickname=new_nick)

@app.route('/diary/write', method=['POST', 'GET'])
def diaryWrite():
    if request.method == 'POST':
        data = request.get_json()

        id = request.cookies.get('Id')
        nick = request.cookies.get('Nick')

        title = data['title']
        contents = data['contents']
        private = data['private']
        category = data['category']
        photo = request.files['images']

        if photo:
            save_path = base64.b64encode(photo.read())
            return db.DiaryCreateP(id=id, nickname=nick, title=title, contents=contents, private=private, category=category, photo=save_path)
        else:
            return db.DiaryCreate(id=id, nickname=nick, title=title, contents=contents, private=private, category=category)

@app.route('/diary/modify', method=['POST', 'GET'])
def diaryModify():
    if request.method == 'POST':
        data = request.get_json()

        id = request.cookies.get('Id')

        title = data['title']
        contents = data['contents']
        private = data['private']
        category = data['category']
        photo = request.files['images']

        if photo:
            save_path = base64.b64encode(photo.read())
            return db.DiaryUpdatep(id=id, title=title, contents=contents, private=private, category=category, photo=save_path)
        else:
            return db.DiaryUpdate(id=id, title=title, contents=contents, private=private, category=category)

@app.route('/diarys/search', method=['POST', 'GET'])
def diarySearch():
    if request.method == 'GET':
        data = request.get_json()

        sort = data['sort']
        category = data['category']

        return db.DiarySearch(sort=sort, category=category)

@app.route('/sympathy', method=['POST', 'GET'])
def sympathyButton():
    if request.method == 'POST':
        nick = request.cookies.get('Nick')

        data = request.get_json()
        writer = data['writer']
        title = data['title']
        category = data['sympathy']

        return db.SympathyButton(nickname=nick, writer=writer, title=title, category=category)

if __name__ == '__main__':
    app.run(debug=True)