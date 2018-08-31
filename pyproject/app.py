
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
    conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='1234', db='pythondb',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
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
    # 로그인이 이미 되어있는 경우(search로 바로 넘어가야함)
    try : 
        session['logged_in']

    # 로그인이 되어있지 않은 경우(로그인창 띄워야함))
    except:
        return render_template('login/login.html')

    # 로그인이 되어있는 경우
    if session['logged_in'] == True:
        conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='1234',
                db='pythondb',charset='utf8', cursorclass=pymysql.cursors.DictCursor)

        # 검색 내역 데이터를 넘겨주기 위하여 DB에서 검색
        # 실행자 생성
        cursor = conn.cursor()   

        execute_str = 'select p_code from want where e_mail = "' + session['ID'] + '"'
        cursor.execute(execute_str) 
        park_data = cursor.fetchall()
        # want list는 e_mail 사용자가 방문했던 주차장 이름
        park_want_list = list()
            
        # want list는 e_mail 사용자가 방문했던 주차장 코드(하이퍼링크에 필요)
        park_code_list = list()

        for park_code in park_data:
            execute_str = "select p_name from parkinglot where p_code = " + str(park_code['p_code'])
            cursor.execute(execute_str) 
            park_name = cursor.fetchall()
            park_want_list.append(park_name[0]['p_name'])
            park_code_list.append(park_code['p_code'])

        sql = "select * from member where e_mail=%s"
        cursor.execute(sql, session['ID'])
        member_data = cursor.fetchone()

        return render_template('search/index.html', member_data=member_data,
                park_want_list = park_want_list, park_want_len = len(park_want_list), park_code_list =park_code_list)
    
    else:
        return render_template('login/login.html')

@app.route("/login_result", methods=['POST'])
def login_result():
    
    # 검색 내역 데이터를 넘겨주기 위하여 DB에서 검색
    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                    password='1234', db='pythondb',charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    # 실행자 생성
    cursor = conn.cursor()  
    user_email = request.form['email']
                    
    # 이메일 중복 시!
    execute_str = 'select * from member where e_mail = "' + user_email + '"'
    cursor.execute(execute_str) 
    park_data = cursor.fetchall()
    if park_data != ():
        return redirect('/')


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
    
    session['logged_in'] = True


 

    execute_str = 'select p_code from want where e_mail = "' + user_email + '"'
    cursor.execute(execute_str) 
    park_data = cursor.fetchall()
    # want list는 e_mail 사용자가 방문했던 주차장 이름
    park_want_list = list()
        
    # want list는 e_mail 사용자가 방문했던 주차장 코드(하이퍼링크에 필요)
    park_code_list = list()


    for park_code in park_data:
        execute_str = "select p_name from parkinglot where p_code = " + str(park_code['p_code'])
        cursor.execute(execute_str) 
        park_name = cursor.fetchall()
        park_want_list.append(park_name[0]['p_name'])
        park_code_list.append(park_code['p_code'])

    return render_template('search/index.html', member_data=member_data,
            park_want_list = park_want_list, park_want_len = len(park_want_list), park_code_list =park_code_list)

@app.route("/member")
def member():
    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                    password='1234', db='pythondb',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 실행자 생성
    cursor = conn.cursor()   

    email = session['ID']
    
    sql = "select * from member where e_mail=%s"
    cursor.execute(sql, email)
    member_data = cursor.fetchone()
    session['logged_in'] = True

    return render_template('member/member.html', member_data = member_data)

@app.route("/member/update", methods=['POST'])
def member_update():
    email = session['ID']
    update_pnum = request.form['phone']
    update_address = request.form['address']
    update_age = request.form['age']
    update_sex = request.form['gender']
    update_family = request.form['family']

    conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='1234',
             db='pythondb',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    # e_mail, phone_number, address, age, sex, family
    sql = "update member set phone_number=%s, address=%s, age =%s, sex =%s, family =%s where e_mail=%s"
    cursor.execute(sql,(update_pnum, update_address, update_age, update_sex, update_family,email))
    
     # 검색 내역 데이터를 넘겨주기 위하여 DB에서 검색
    # 실행자 생성
    cursor = conn.cursor()   

    execute_str = 'select p_code from want where e_mail = "' + email + '"'
    cursor.execute(execute_str) 
    park_data = cursor.fetchall()
    # want list는 e_mail 사용자가 방문했던 주차장 이름
    park_want_list = list()
        
    # want list는 e_mail 사용자가 방문했던 주차장 코드(하이퍼링크에 필요)
    park_code_list = list()

    for park_code in park_data:
        execute_str = "select p_name from parkinglot where p_code = " + str(park_code['p_code'])
        cursor.execute(execute_str) 
        park_name = cursor.fetchall()
        park_want_list.append(park_name[0]['p_name'])
        park_code_list.append(park_code['p_code'])

    sql = "select * from member where e_mail=%s"
    cursor.execute(sql, email)
    member_data = cursor.fetchone()

    conn.commit()
    
    session['logged_in'] = True

    return render_template('search/index.html', member_data=member_data,
            park_want_list = park_want_list, park_want_len = len(park_want_list), park_code_list =park_code_list)

@app.route("/signup_com")
def signup_com():
    return render_template('login/signup_com.html')

app.register_blueprint(search,url_prefix = '/search')
app.register_blueprint(details,url_prefix = '/details')
app.register_blueprint(datalab,url_prefix = '/datalab')

# app 실행
if __name__ == "__main__":
    app.run(debug=True)