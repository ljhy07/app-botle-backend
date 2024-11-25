import pymysql

class DB:
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='root', password='', db='AppJam', charset='utf8') # 보안상 비밀번호는 제거(.env로 수정 필요)
        self.cursor = self.db.cursor()
    
    def UserCreate(self, id, nickname, pwd):
        cmd = "insert into user(id, nickname, pwd) values (%s, %s, %s)"
        self.cursor.execute(cmd, (id, nickname, pwd))

        self.db.commit()
    
    def UserSearch(self, id, pwd): # select
        try:
            cmd = "select id, pwd from user where id=%s"
            self.cursor.execute(cmd, (id))
            data = self.cursor.fetchone()
            print(data)
            db_id, db_pwd = data[0]
            
            if db_id == id and db_pwd == pwd:
                return True
            return False
        except IndexError:
            return False
    
    def UserPwdSearch(self, pwd): # select
        try:
            cmd = "select id, pwd from user where pwd=%s"
            self.cursor.execute(cmd, (id))
            data = self.cursor.fetchone()
            db_id, db_pwd = data[0]
            
            if db_pwd == pwd:
                return True
            return False
        except IndexError:
            return False

    def UserNickUpdate(self, id, nickname): # update
        cmd = "update user set nickname=%s where id=%s"
        self.cursor.execute(cmd, (nickname, id))

        self.db.commit()
    
    # def UserPwdUpdate(self, id, pwd, new_pwd): # update
    #     cmd = "update user set pwd=%s where id=%s and pwd=%s"
    #     self.cursor.execute(cmd, (new_pwd, id, pwd))
    #     self.db.commit()
    
    # def UserDelete(self): # delete, 탈퇴

    def DiaryCreate(self, id, nickname, title, contents, private, category):
        reset = 0

        cmd = "insert into diary(id, writer, title, contents, Private, category, happy, sad, angry, surprised) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(cmd, (id, nickname, title, contents, private, category, reset, reset, reset, reset))

        self.db.commit()

    def DiaryCreateP(self, id, nickname, title, contents, private, category, photo):
        reset = 0

        cmd = "insert into diary(id, writer, title, contents, Private, category, photo, happy, sad, angry, surprised) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(cmd, (id, nickname, title, contents, private, category, photo, reset, reset, reset, reset))

        self.db.commit()
    
    def MyDiarySearch(self, id):
        cmd = "select writer, title, contents, Private, category, photo, day, happy, sad, angry, surprised from diary where id=%s"
        self.cursor.execute(cmd, (id))
        return self.cursor.fetchmany(10)
    
    def DiarySearch(self, sort, category):
        if category == 'all':
            if sort == 'recent':
                cmd = 'select writer, title, contents, category, photo, day, happy, sad, angry, surprised from diary order by day desc'
                self.cursor.execute(cmd)
                return self.cursor.fetchmany(25)
            elif sort == 'popular':
                cmd = 'select writer, title, contents, category, photo, day, happy, sad, angry, surprised from diary order by (happy+sad+angry+surprised)'
                self.cursor.execute(cmd)
                return self.cursor.fetchmany(25)
        else:
            if sort == 'recent':
                cmd = 'select writer, title, contents, category, photo, day, happy, sad, angry, surprised from diary where category=%s order by day desc'
                self.cursor.execute(cmd, (category))
                return self.cursor.fetchmany(25)
            elif sort == 'popular':
                cmd = 'select writer, title, contents, category, photo, day, happy, sad, angry, surprised from diary where category=%s order by (happy+sad+angry+surprised)'
                self.cursor.execute(cmd, (category))
                return self.cursor.fetchmany(25)

    def DiaryUpdateP(self, id, title, contents, private, category, photo):
        cmd = "update diary set title=%s, contents=%s, Private=%s, category=%s, photo=%s"
        self.cursor.execute(cmd, (id, title, contents, private, category, photo))

        self.db.commit()

    def DiaryUpdate(self, id, title, contents, private, category):
        cmd = "update diary set title=%s, contents=%s, Private=%s, category=%s"
        self.cursor.execute(cmd, (id, title, contents, private, category))

        self.db.commit()
    
    def DiaryDelete(self, id, title):
        cmd = "delete from diary where id=%s and title=%s"
        self.cursor.execute(cmd, (id, title))

        self.db.commit()
    
    def Sympathy(self, nickname, writer, title, category):
        cmd = 'insert into sympathyList value (%s, %s, %s, %s)'
        self.cursor.execute(cmd, (nickname, writer, title, category))

        self.db.commit()
