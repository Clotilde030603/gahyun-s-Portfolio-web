from flask import Flask, render_template, session, request, url_for, redirect
from datetime import timedelta
import sqlite3
import secrets

app = Flask(__name__)
# 키값 설정
app.secret_key = secrets.token_hex(256)
# 세션 타임 설정
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)
# 세션 타입 설정
app.config['SESSION_TYPE'] = 'filesystem'


db_path = "main.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
cur = conn.cursor() 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/awards')
def awards():
    return render_template('awards.html')

@app.route('/board_write', methods=['GET', 'POST'])
def board_write():
    if request.method == 'GET' :
        return render_template('board_write.html')
    elif request.method == 'POST' :
        try :
            title = request.form['title']
            contents = request.form['contents']
            u_id = session['id']
            username = session['username']
            status = 1
            insert_query = """
                INSERT INTO board (u_id, username, title, contents, status) 
                VALUES (?, ?, ?, ?, ?)
                """
            cur.execute(insert_query, (u_id, username, title, contents, status))
            conn.commit()
            return redirect(url_for('board_list'))
        except sqlite3.IntegrityError:
            msg = "게시글 작성 실패"
            return render_template('board_write.html', msg=msg)

@app.route('/board_list', methods=['GET'])
def board_list():
    if request.method == 'GET' :
        select_query = """
        SELECT id, username, title, mdate FROM board WHERE status = 1
        """
        cur.execute(select_query)
        posts = cur.fetchall()
        return render_template('board_list.html', posts=posts)
    
@app.route('/board_view', methods=['GET'])
def board_view():
    id = request.args.get('id')
    status = 1
    select_query = """
    SELECT id, username, title, contents FROM board WHERE id = ? and status = ?
    """
    cur.execute(select_query, (id, status))
    post = cur.fetchone() 
    return render_template('board_view.html', post=post)
    
    

@app.route('/qna_write', methods=['GET', 'POST'])
def qna_write():
    if request.method == 'GET' :
        return render_template('qna_write.html')
    elif request.method == 'POST' :
        try :
            title = request.form['title']
            contents = request.form['contents']
            u_id = session['id']
            username = session['username']
            status = 1
            insert_query = """
                INSERT INTO qna (u_id, username, title, contents, status) 
                VALUES (?, ?, ?, ?, ?)
                """
            cur.execute(insert_query, (u_id, username, title, contents, status))
            conn.commit()
            return redirect(url_for('qna_list'))
        except sqlite3.IntegrityError:
            msg = "게시글 작성 실패"
            return render_template('qna_write.html', msg=msg)


@app.route('/qna_list', methods=['GET'])
def qna_list():
    if request.method == 'GET' :
        select_query = """
        SELECT id, username, title, mdate FROM qna WHERE status = 1
        """
        cur.execute(select_query)
        posts = cur.fetchall()
        return render_template('qna_list.html', posts=posts)

@app.route('/qna_view', methods=['GET'])
def qna_view():
    id = request.args.get('id')
    status = 1
    select_query = """
    SELECT id, username, title, contents FROM qna WHERE id = ? and status = ?
    """
    cur.execute(select_query, (id, status))
    post = cur.fetchone() 
    return render_template('qna_view.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        try:
            id = request.form['id']
            password = request.form['password']
            insert_query = """
            SELECT id, username, authority FROM user WHERE id = ? AND pw = ?
            """
            cur.execute(insert_query, (id, password))
            user = cur.fetchone()
            session['id'] = user[0]
            session['username'] = user[1]
            session['authority'] = user[2]
            return render_template('index.html')
        except sqlite3.IntegrityError:
            msg = "로그인 실패"
            return render_template('login.html', msg=msg)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        try:
            id = request.form['id']
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            email = request.form['email']
            phone_number = request.form['phone_number']
            authority = 0
            status = 1
            if password == confirm_password:
                insert_query = """
                INSERT INTO user (id, username, name, pw, email, phone, authority, status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
            cur.execute(insert_query, (id, username, name, password, email, phone_number, authority, status))
            conn.commit()
            return render_template('login.html')
        except sqlite3.IntegrityError:
            msg = "회원가입 실패"
            return render_template('signup.html', msg=msg)

@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
