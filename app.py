from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('root.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username, password = ["admin", "123456"]
    if request.method == 'POST':
        user = request.form.get('username')
        psw = request.form.get('password')
        if user == username and psw == password:
            return render_template('admin.html')
    return render_template('login.html')


@app.route('/admin',methods = ['GET','POST'])
def admin():
    return render_template('admin.html')


@app.route('/display')
def display():
    db = 'test.db'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = 'SELECT * FROM studentList'
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('display.html', content=rows)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        id = int(request.form['id'])
        name = request.form['name']
        major = request.form['major']
        year = request.form['year']
        math = int(request.form['math'])
        physics = int(request.form['physics'])
        python = int(request.form['python'])

        db = 'test.db'
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'insert into studentList(学号,姓名,专业,年级,高等数学,大学物理,Python程序设计基础) values (?,?,?,?,?,?,?)'
        cur.execute(sql, (id, name, major, year, math, physics, python))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/admin')
    return render_template('add.html')


if __name__ == '__main__':
    app.run()
