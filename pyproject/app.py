
from flask import Flask, render_template, request, redirect, session
from controllers.search import search
from controllers.details import details
import pymysql

# app 객체 생성
app = Flask(__name__)
app.secret_key = "e21lr1or2AKO@2rkARKM@RAR@ANK2raar,SD2"

@app.route("/")
def login():
    return render_template('login/login.html')

@app.route("/login_result", methods=['POST'])
def login_result():
    return render_template('login/login_result.html')

@app.route("/member")
def member():
    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                    password='1234', db='pythondb',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
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

# app 실행
if __name__ == "__main__":
    app.run(debug=True)