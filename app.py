from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

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
    db = 'students.db'
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

        db = 'students.db'
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'insert into studentList(id,name,major,year,AdvancedMath,CollegePhysics,PythonProgramming) values (?,?,?,?,?,?,?)'
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

        db = 'students.db'
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'select * from studentList where id=? '
        cur.execute(sql, (id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        if data:
            return render_template('display.html', content=data)
    return render_template('search.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    db = 'students.db'
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
            db = 'students.db'
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            sql = 'DELETE FROM studentList WHERE id = ?'  # 使用学生ID来编写DELETE SQL语句
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

        db = 'students.db'
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        sql = 'select * from studentList where id=? '
        cur.execute(sql, (id,))
        data = cur.fetchall()
        cur.close()
        conn.close()
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
            db = 'students.db'
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            sql = 'update studentList set name=?, major=?, year=?, AdvancedMath=?, CollegePhysics=?, PythonProgramming=? where id=?'
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
    db = 'students.db'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()
    columns = ["order", "id", "name", "major", "year", "math", "physics", "python"]
    df = pd.DataFrame(data=data, columns=columns)
    df.sort_values(by="math", ascending=False, inplace=True)
    data = df.values.tolist()

    cur.close()
    conn.close()
    return render_template('display.html',content = data)

@app.route('/sort/sort_physics')
def sort_physics():
    db = 'students.db'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()
    columns = ["order", "id", "name", "major", "year", "math", "physics", "python"]
    df = pd.DataFrame(data=data, columns=columns)
    df.sort_values(by="physics", ascending=False, inplace=True)
    data = df.values.tolist()

    cur.close()
    conn.close()
    return render_template('display.html',content = data)

@app.route('/sort/sort_python')
def sort_python():
    db = 'students.db'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()
    columns = ["order", "id", "name", "major", "year", "math", "physics", "python"]
    df = pd.DataFrame(data=data, columns=columns)
    df.sort_values(by="python", ascending=False, inplace=True)
    data = df.values.tolist()

    cur.close()
    conn.close()
    return render_template('display.html',content = data)

@app.route('/graph')
def graph():
    return render_template('graph.html')

def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf


@app.route('/graph/graph_math')
def graph_math():
    plt.clf()     #清除原来matplotlib样式
    plt.figure(figsize=(9.5,7.5))
    # 声明变量
    a = 0  # 90分以上数量
    b = 0  # 80-90分以上数量
    c = 0  # 70-80分以上数量
    d = 0  # 60-70分以上数量
    e = 0  # 60分以下数量
    score_max = 0
    score_min = 100
    score_avg = 0
    score_sum = 0

    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()

    columns = ["order", "id", "name", "major", "year", "math", "physics", "python"]
    df = pd.DataFrame(data=data, columns=columns)

    math_score = df['math']  # 获得分数数据集
    physics_score = df['physics']
    mean = math_score.mean()  # 获得分数数据集的平均值
    std = math_score.std()  # 获得分数数据集的标准差

    # 计算分数总和、各分数区间数量统计
    for i in range(0, len(math_score)):
        score0 = int(math_score[i])
        score_sum = score_sum + score0  # 计算分数之和，为求平均数做准备
        if score0 > score_max:
            score_max = score0
        if score0 < score_min:
            score_min = score0
        if score0 >= 90:  # 统计90分以上数量
            a = a + 1
        elif score0 >= 80:  # 统计80分以上数量
            b = b + 1
        elif score0 >= 70:  # 统计70分以上数量
            c = c + 1
        elif score0 >= 60:  # 统计60分以上数量
            d = d + 1
        else:  # 统计60分以下数量
            e = e + 1

    score_avg = score_sum / len(math_score)  # 平均分
    scores = [a, b, c, d, e]  # 分数区间统计

    # 柱形图柱形的宽度
    bar_width = 0.3
    # 设定X轴：前两个数字是x轴的起止范围，第三个数字表示步长，步长设定得越小，画出来的正态分布曲线越平滑
    x = np.arange(0, 100, 1)
    # 设定Y轴，正态分布函数
    y = normfun(x, mean, std)

    # 设定柱状图x轴、Y轴数组
    x3 = np.arange(3)
    y3 = np.array([score_avg, score_max, score_min])

    # 绘制分数数据集的正态分布曲线和直方图（5分档）
    plt.subplot(221)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数分布(5档)')
    plt.plot(x, y)
    plt.hist(math_score, bins=5, rwidth=0.9, density=True)
    plt.xlabel('分数')
    plt.ylabel('概率')

    # 绘制分数数据集的散点图，每个点代表一个学生
    plt.subplot(222)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('Math vs Physics')
    plt.scatter(physics_score, math_score, c='blue', alpha=0.5, label='Physics vs Math')
    plt.xlabel('physics')
    plt.ylabel('math')

    plt.xlim(60, 100)  # Set x-axis range
    plt.ylim(60, 100)  # Set y-axis range

    # 绘制柱形图
    plt.subplot(223)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数统计')
    plt.bar(x3, y3, tick_label=['平均分', '最高分', '最低分'], width=bar_width)

    # 绘制饼状图
    plt.subplot(224)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数段饼图')
    plt.pie(scores, labels=['90分以上', '80-90分', '70-80分', '60-70分', '60分以下'], autopct='%1.1f%%')
    # 输出四幅图
    plt.tight_layout()

    # 将图表保存为PNG图片
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    cur.close()
    conn.close()

    # 将图片编码为base64
    graph = base64.b64encode(image_png).decode('utf-8')

    return render_template('graph_math.html', graph=graph)

@app.route('/graph/graph_physics')
def graph_physics():
    plt.clf()
    plt.figure(figsize=(9.5, 7.5))
    # 声明变量
    a = 0  # 90分以上数量
    b = 0  # 80-90分以上数量
    c = 0  # 70-80分以上数量
    d = 0  # 60-70分以上数量
    e = 0  # 60分以下数量
    score_max = 0
    score_min = 100
    score_avg = 0
    score_sum = 0

    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()

    columns = ["order", "id", "name", "major", "year", "math", "physics", "python"]
    df = pd.DataFrame(data=data, columns=columns)
    # 获得分数数据集
    physics_score = df['physics']
    python_score = df["python"]
    mean = physics_score.mean()  # 获得分数数据集的平均值
    std = physics_score.std()  # 获得分数数据集的标准差

    # 计算分数总和、各分数区间数量统计
    for i in range(0, len(physics_score)):
        score0 = int(physics_score[i])
        score_sum = score_sum + score0  # 计算分数之和，为求平均数做准备
        if score0 > score_max:
            score_max = score0
        if score0 < score_min:
            score_min = score0
        if score0 >= 90:  # 统计90分以上数量
            a = a + 1
        elif score0 >= 80:  # 统计80分以上数量
            b = b + 1
        elif score0 >= 70:  # 统计70分以上数量
            c = c + 1
        elif score0 >= 60:  # 统计60分以上数量
            d = d + 1
        else:  # 统计60分以下数量
            e = e + 1

    score_avg = score_sum / len(physics_score)  # 平均分
    scores = [a, b, c, d, e]  # 分数区间统计

    # 柱形图柱形的宽度
    bar_width = 0.3
    # 设定X轴：前两个数字是x轴的起止范围，第三个数字表示步长，步长设定得越小，画出来的正态分布曲线越平滑
    x = np.arange(0, 100, 1)
    # 设定Y轴，正态分布函数
    y = normfun(x, mean, std)

    # 设定柱状图x轴、Y轴数组
    x3 = np.arange(3)
    y3 = np.array([score_avg, score_max, score_min])

    # 绘制分数数据集的正态分布曲线和直方图（5分档）
    plt.subplot(221)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数分布(5档)')
    plt.plot(x, y)
    plt.hist(physics_score, bins=5, rwidth=0.9, density=True)
    plt.xlabel('分数')
    plt.ylabel('概率')

    # 绘制分数数据集的散点图，每个点代表一个学生
    plt.subplot(222)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('Physics vs Python')
    plt.scatter(physics_score, python_score, c='blue', alpha=0.5, label='Physics vs Python')
    plt.xlabel('Python')
    plt.ylabel('Physics')

    plt.xlim(60, 100)  # Set x-axis range
    plt.ylim(60, 100)  # Set y-axis range

    # 绘制柱形图
    plt.subplot(223)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数统计')
    plt.bar(x3, y3, tick_label=['平均分', '最高分', '最低分'], width=bar_width)

    # 绘制饼状图
    plt.subplot(224)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数段饼图')
    plt.pie(scores, labels=['90分以上', '80-90分', '70-80分', '60-70分', '60分以下'], autopct='%1.1f%%')
    # 输出四幅图
    plt.tight_layout()

    # 将图表保存为PNG图片
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    cur.close()
    conn.close()

    # 将图片编码为base64
    graph = base64.b64encode(image_png).decode('utf-8')

    return render_template('graph_physics.html', graph=graph)

@app.route('/graph/graph_python')
def graph_python():
    plt.clf()
    plt.figure(figsize=(9.5, 7.5))
    # 声明变量
    a = 0  # 90分以上数量
    b = 0  # 80-90分以上数量
    c = 0  # 70-80分以上数量
    d = 0  # 60-70分以上数量
    e = 0  # 60分以下数量
    score_max = 0
    score_min = 100
    score_avg = 0
    score_sum = 0

    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()

    columns = ["order", "id", "name", "major", "year", "math", "physics", "python"]
    df = pd.DataFrame(data=data, columns=columns)
    # 获得分数数据集
    python_score = df["python"]
    math_score = df['math']
    mean = python_score.mean()  # 获得分数数据集的平均值
    std = python_score.std()  # 获得分数数据集的标准差

    # 计算分数总和、各分数区间数量统计
    for i in range(0, len(python_score)):
        score0 = int(python_score[i])
        score_sum = score_sum + score0  # 计算分数之和，为求平均数做准备
        if score0 > score_max:
            score_max = score0
        if score0 < score_min:
            score_min = score0
        if score0 >= 90:  # 统计90分以上数量
            a = a + 1
        elif score0 >= 80:  # 统计80分以上数量
            b = b + 1
        elif score0 >= 70:  # 统计70分以上数量
            c = c + 1
        elif score0 >= 60:  # 统计60分以上数量
            d = d + 1
        else:  # 统计60分以下数量
            e = e + 1

    score_avg = score_sum / len(python_score)  # 平均分
    scores = [a, b, c, d, e]  # 分数区间统计

    # 柱形图柱形的宽度
    bar_width = 0.3
    # 设定X轴：前两个数字是x轴的起止范围，第三个数字表示步长，步长设定得越小，画出来的正态分布曲线越平滑
    x = np.arange(0, 100, 1)
    # 设定Y轴，正态分布函数
    y = normfun(x, mean, std)

    # 设定柱状图x轴、Y轴数组
    x3 = np.arange(3)
    y3 = np.array([score_avg, score_max, score_min])

    # 绘制分数数据集的正态分布曲线和直方图（5分档）
    plt.subplot(221)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数分布(5档)')
    plt.plot(x, y)
    plt.hist(python_score, bins=5, rwidth=0.9, density=True)
    plt.xlabel('分数')
    plt.ylabel('概率')

    # 绘制分数数据集的散点图，每个点代表一个学生
    plt.subplot(222)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('Python vs Math')
    plt.scatter(python_score, python_score, c='blue', alpha=0.5, label='Python vs Math')
    plt.xlabel('Math')
    plt.ylabel('Python')

    plt.xlim(60, 100)  # Set x-axis range
    plt.ylim(60, 100)  # Set y-axis range

    # 绘制柱形图
    plt.subplot(223)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数统计')
    plt.bar(x3, y3, tick_label=['平均分', '最高分', '最低分'], width=bar_width)

    # 绘制饼状图
    plt.subplot(224)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('分数段饼图')
    plt.pie(scores, labels=['90分以上', '80-90分', '70-80分', '60-70分', '60分以下'], autopct='%1.1f%%')
    # 输出四幅图
    plt.tight_layout()

    # 将图表保存为PNG图片
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    cur.close()
    conn.close()

    # 将图片编码为base64
    graph = base64.b64encode(image_png).decode('utf-8')

    return render_template('graph_python.html', graph=graph)


if __name__ == '__main__':
    app.run()
