import pandas as pd  # 引入panda工具集
import numpy as np  # 引入numpy核心库
import matplotlib.pyplot as plt  # 引入matplotlib数据可视化库
import sqlite3

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

# 正态分布的概率密度函数
#   x      数据集中的某一具体测量值
#   mu     数据集的平均值，反映测量值分布的集中趋势
#   sigma  数据集的标准差，反映测量值分布的分散程度

def normfun(x, mu, sigma):   #定义正态密度函数
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf


if __name__ == '__main__':
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    sql = 'select * from studentList'
    cur.execute(sql)
    data = cur.fetchall()

    columns = ["序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"]
    df = pd.DataFrame(data=data, columns=columns)

    math_score = df['高等数学']  # 获得分数数据集
    physics_score = df['大学物理']
    student_no = df['学号']  # 获得学号数据集
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
    plt.title('Physics vs Math')
    plt.scatter(physics_score, math_score, c='blue', alpha=0.5, label='Physics vs Math')
    plt.xlabel('大学物理')
    plt.ylabel('高等数学')

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
    plt.pie(scores, labels=['90分以上', '80-90分', '70-80分', '60-70分', '60分以下'],autopct='%1.1f%%')
    # 输出四幅图
plt.tight_layout()
plt.show()