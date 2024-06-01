from flask import Flask, render_template, request, redirect, url_for, jsonify
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
            return redirect(url_for('admin'))
    return render_template('login.html')


@app.route('/admin', methods=['GET'])
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
        return redirect(url_for('display'))
    return render_template('add.html')

@app.route('/search',methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        id = int(request.form['id'])

        db = 'test.db'
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'select * from studentList where 学号=? '
        cur.execute(sql, (id, ))
        data = cur.fetchall()
        if data:
            return render_template('display.html', content=data)
    return render_template('search.html')

@app.route('/delete',methods = ['GET','POST'])
def delete():
    db = 'test.db'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = 'SELECT * FROM studentList'
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('delete.html', content=rows)


@app.route('/delete_student', methods=['POST'])
def delete_student():
    if request.method == 'POST':
        student_id = request.json.get('student_id')  # 从前端获取要删除的学生ID
        try:
            student_id = int(student_id)  # 尝试将学生ID转换为整数
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'Invalid student_id format'})  # 如果转换失败则返回错误响应

        if student_id:
            db = 'test.db'
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            sql = 'DELETE FROM studentList WHERE 学号 = ?'  # 使用学生ID来编写DELETE SQL语句
            cur.execute(sql, (student_id,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'success': True})  # 返回一个JSON响应，表示删除成功
        else:
            return jsonify({'success': False, 'error': 'Invalid student_id format'})  # 返回一个JSON响应，表示删除失败（学生ID格式无效）
    else:
        return jsonify({'success': False, 'error': 'Invalid request method'})  # 返回一个JSON响应，表示删除失败（请求方法无效）

@app.route('/update',methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        id = int(request.form['id'])

        db = 'test.db'
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'select * from studentList where 学号=? '
        cur.execute(sql, (id, ))
        data = cur.fetchall()
        if data:
            return render_template('update.html', student=data[0])
    return render_template('update_search.html')

@app.route('/update_student',methods = ['POST'])
def update_student():
    if request.method == 'POST':
        id = int(request.json.get('student_id'))
        name = request.json.get('student_name')
        major = request.json.get('student_major')
        year = request.json.get('student_year')
        math = int(request.json.get('student_math'))
        physics = int(request.json.get('student_physics'))
        python = int(request.json.get('student_python'))

        if id:
            db = 'test.db'
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            sql = 'update studentList set 姓名=?, 专业=?, 年级=?, 高等数学=?, 大学物理=?, Python程序设计基础=? where 学号=?'
            cur.execute(sql, (name, major, year, math, physics, python, id))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Invalid student_id format'})  # 返回一个JSON响应，表示删除失败（学生ID格式无效）
    return jsonify({'success': False, 'error': 'Invalid request method'})

@app.route('/sort')
def sort():
    return render_template('sort.html')

if __name__ == '__main__':
    app.run()
