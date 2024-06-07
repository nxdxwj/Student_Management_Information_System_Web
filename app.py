from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from scipy.stats import norm

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('root.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username, password = ["admin", "2024"]
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


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        id = int(request.form['id'])

        db = 'test.db'
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'select * from studentList where 学号=? '
        cur.execute(sql, (id,))
        data = cur.fetchall()
        if data:
            return render_template('display.html', content=data)
    return render_template('search.html')


@app.route('/delete', methods=['GET', 'POST'])
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


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = int(request.form['id'])

        db = 'test.db'
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'select * from studentList where 学号=? '
        cur.execute(sql, (id,))
        data = cur.fetchall()
        if data:
            return render_template('update.html', student=data[0])
    return render_template('update_search.html')


@app.route('/update_student', methods=['POST'])
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


@app.route('/sort/sort_math')
def sort_math():
    db = 'test.db'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()
    columns = ["序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"]
    df = pd.DataFrame(data=data, columns=columns)
    df.sort_values(by="高等数学", ascending=False, inplace=True)
    data = df.values.tolist()
    return render_template('display.html',content = data)

@app.route('/sort/sort_physics')
def sort_physics():
    db = 'test.db'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()
    columns = ["序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"]
    df = pd.DataFrame(data=data, columns=columns)
    df.sort_values(by="大学物理", ascending=False, inplace=True)
    data = df.values.tolist()
    return render_template('display.html',content = data)

@app.route('/sort/sort_python')
def sort_python():
    db = 'test.db'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()
    columns = ["序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"]
    df = pd.DataFrame(data=data, columns=columns)
    df.sort_values(by="Python程序设计基础", ascending=False, inplace=True)
    data = df.values.tolist()
    return render_template('display.html',content = data)

@app.route('/graph')
def graph():
    return render_template('graph.html')

def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf


@app.route('/graph/math')
def graphMath():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()
    columns = ["序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"]
    df = pd.DataFrame(data=data, columns=columns)
    math_score = df["高等数学"]
    mean = math_score.mean()
    std = math_score.std()

    plt.subplot(221)
    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.title('分数分布(5档)')
    x = np.linspace(0, 100, 1000)
    y = norm.pdf(x, mean, std)
    plt.plot(x, y, label='拟合曲线')

    plt.hist(math_score, bins=20, alpha=0.7, color='b', edgecolor='black', density=True)
    plt.xlabel('分数')
    plt.ylabel('概率')

    # 将图表保存为PNG图片
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    conn.close()

    # 将图片编码为base64
    graph = base64.b64encode(image_png).decode('utf-8')

    return render_template('graph_math.html', graph=graph)



if __name__ == '__main__':
    app.run()
