
from flask import Flask, render_template, request, redirect, session
from controllers.search import search
from controllers.details import details
from controllers.datalab import datalab
import pymysql

# app 객체 생성
app = Flask(__name__)
app.secret_key = "e21lr1or2AKO@2rkARKM@RAR@ANK2raar,SD2"

def insertData(user_email,user_pnum,user_address,user_age,user_sex,user_family):
    # DB 연동 - 연결
    conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='1234', db='pythondb1',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    sql = "insert into member (e_mail,phone_number,address,age,sex,family)\
                     values (%s,%s,%s,%s,%s,%s);"
    cursor.execute(sql, (user_email,user_pnum,user_address,user_age,user_sex,user_family))
    conn.commit()

    execute_str = 'select * from member where e_mail = "' + user_email + '"'

    cursor.execute(execute_str)
    member_data = cursor.fetchall()

    return member_data

@app.route("/")
def login():
    return render_template('login/login.html')

@app.route("/login_result", methods=['POST'])
def login_result():
    
    # 폼필드 받은 값을 변수에 저장
    user_email = request.form['email']
    user_pnum = request.form['phone']
    user_address = request.form['address']
    user_age = request.form['age']
    user_age = int(user_age)
    user_sex = request.form['gender']
    user_family = request.form['family']
    user_family = int(user_family)
    # 함수 실행
    member_data = insertData(user_email,user_pnum,user_address,user_age,user_sex,user_family)

    session['ID'] = user_email

    return render_template('search/index.html', member_data=member_data)

@app.route("/member")
def member():
    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                    password='1234', db='pythondb1',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 실행자 생성
    cursor = conn.cursor()   

    email = session['ID']

    execute_str = 'select * from member where e_mail = "' + email + '"'

    cursor.execute(execute_str)
    member_data = cursor.fetchall()

    return render_template('member/member.html', member_data = member_data)

@app.route("/signup_com")
def signup_com():
    return render_template('login/signup_com.html')

app.register_blueprint(search,url_prefix = '/search')
app.register_blueprint(details,url_prefix = '/details')
app.register_blueprint(datalab,url_prefix = '/datalab')

# app 실행
if __name__ == "__main__":
    app.run(debug=True)