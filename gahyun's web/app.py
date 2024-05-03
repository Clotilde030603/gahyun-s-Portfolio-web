from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/awards')
def awards():
    return render_template('awards.html')

@app.route('/board')
def board():
    return render_template('board.html')

@app.route('/qna')
def qna():
    return render_template('qna.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
