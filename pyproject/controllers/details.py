from flask import Blueprint, render_template, request, session, redirect
import googlemaps
import pymysql
import numpy as np
import pandas as pd
# 문자열에서 숫자만 추출하는 모듈
import re

# 주차장 개방 날짜 구현
# date_num(1, p_code) 을 입력하면 want DB에서의 go_date1을 검색하여 가고싶은 사람의 개수를 return한다.
def date_num(day, p_code):
    conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()   

    sql = 'select * from want where go_date' + str(day) + ' = 1 and p_code = ' + str(p_code) 
    cursor.execute(sql)
    data = cursor.fetchall()

    conn.close()
    
    return len(data)

def like_num(p_code):
    conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()   

    sql = 'select * from want where go_like= 2 and p_code = ' + str(p_code) 
    cursor.execute(sql)
    data2 = cursor.fetchall()
    
    sql = 'select * from want where go_like= 1 and p_code = ' + str(p_code) 
    cursor.execute(sql)
    data1 = cursor.fetchall()
    
    sql = 'select * from want where go_like= 0 and p_code = ' + str(p_code) 
    cursor.execute(sql)
    data0 = cursor.fetchall()

    data_sum = len(data2) + len(data1) + len(data0)
    
    like_data = [
        {
            'value' : len(data2),
            'label': 'Like',
            'color': '#3399FF'
        },
        {
            'value' : len(data1),
            'label': 'Soso',
            'color': '#FFC575'
        },
        {
            'value' : len(data0),
            'label': 'Bad',
            'color': '#99CC00'
        },
    ]

    conn.close()

    return like_data, len(data2), len(data1), len(data0)
    
    



details = Blueprint('details', __name__, template_folder='details')

@details.route("/")
def detailpage():
    
    # 로그인을 안하고 /detail/에 강제 접속할 경우 return redirect
    try:
        session['logged_in']
    except:
        return redirect('/')

    return redirect('/')

@details.route("/<p_code>")
def detailpage2(p_code):
    try :
        session['ID']
    except:
        return redirect('/')

    p_code_num = int(re.findall('\d+', p_code)[0])

    # DB 연동 - 연결
    conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()   
    execute_str = "select * from parkinglot where p_code = " + '"' + str(p_code_num) + '"'

    cursor.execute(execute_str)

    park_data = cursor.fetchall()


    # initialize park(반복될때마다 데이터가 축적되면 안되므로))
    park = dict()
    
    # park를 json 형식으로 저장
    for i in park_data:
        park_num = 'p_' +str(i[0])

        park[park_num] = {                 
            'p_province' : i[1], 
            'p_name' : i[2],
            'p_type' : i[3],
            'p_address' : i[4],
            'p_lat' : float(i[5]),
            'p_long' : float(i[6]),
            'p_admit' : i[7],
            'p_number' : i[8],
            'p_desp' : i[9],
            'p_date1' : i[10][3:],
            'p_date2' : i[11][3:],
            'p_date3' : i[12][3:],
            'p_date4' : i[13][3:],
            'p_date5' : i[14][3:]
        }

        for key in park[park_num]:
            if 'date' in key:
                if type(park[park_num][key]) == float or park[park_num][key] == '':
                    park[park_num][key] = '정보없음'
            if 'desp' in key:
                print(park[park_num][key])
                if park[park_num][key] == None:
                    park[park_num][key] = '정보없음'

    # 한줄평 데이터 받아오기
    sql = "select e_mail, go_comment from want where p_code = " + str(p_code_num)
    cursor.execute(sql)
    comment_data = cursor.fetchall()

    comment_str = list()
    comment_email = list()
    comment_len = 0

    for comm in comment_data:
        if not comm[1] == None:
            a, b = comm[0].split('@')
            comment_email.append(a[0 : len(a)-3] + '***@'+b)
            comment_str.append(comm[1])
            comment_len += 1

    
    # 가고싶은 날짜 데이터를 ( , , ) 튜플형태로 저장 및 템플릿에 보내기
    go_date = (date_num(1,p_code_num), date_num(2,p_code_num), 
                date_num(3,p_code_num), date_num(4,p_code_num), date_num(5,p_code_num))

    like_day, day_like2, day_like1, day_like0 = like_num(p_code_num)

    try:
        sql =  "select * from want where p_code = " + '"' + str(p_code_num) + '" and e_mail = "' + session['ID'] + '"'
        if cursor.execute(sql):
            return render_template('details/details.html', park=park, p_num = park_num, p_code = i[0], comment_email=comment_email, comment_str = comment_str, comment_len= comment_len, go_date = go_date, 
            like_data = like_day, day_like2 = day_like2, day_like1 = day_like1, day_like0 = day_like0)
        check_data= cursor.fetchall()
    except:
        return render_template('details/details.html', park=park, p_num = park_num, p_code = i[0], comment_email=comment_email, comment_str = comment_str, comment_len= comment_len, go_date = go_date, 
        like_data = like_day, day_like2 = day_like2, day_like1 = day_like1, day_like0 = day_like0)


    if check_data == ():
        sql = "insert into want(e_mail, p_code) values(%s, %s)"        
        data = (session['ID'], p_code_num)
        cursor.execute(sql,data)


    conn.commit()
    return render_template('details/details.html', 
                        park=park, p_num = park_num, p_code = i[0], comment_email=comment_email, comment_str = comment_str, comment_len= comment_len, go_date = go_date, 
                        like_data = like_day, day_like2 = day_like2, day_like1 = day_like1, day_like0 = day_like0)

# get과 post방식 둘다 사용하기 get 화면 post 가고싶어요 받기
@details.route("/date/<p_code>", methods=['POST'])
def park_date(p_code):
    dates = request.form.getlist('checkdate')
    date1 = 0
    date2 = 0
    date3 = 0
    date4 = 0
    date5 = 0
    for i in dates:
        if i == 'date1':
            date1 = 1
        if i == 'date2':
            date2 = 1
        if i == 'date3':
            date3 = 1
        if i == 'date4':
            date4 = 1
        if i == 'date5':
            date5 = 1

    # DB 연동 - 연결
    conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()   
    sql = "update want set go_date1=%s, go_date2=%s, go_date3=%s, go_date4=%s, go_date5=%s where e_mail = %s and p_code = %s"     
    data = (date1, date2, date3, date4, date5, session['ID'], p_code)
    cursor.execute(sql,data)
    conn.commit()
    
    str_return = "/details/" + str(p_code)
    return  redirect(str_return)

# 만족도 좋아요, 보통, 싫어요 Insert(To want DB, 가고싶어요)
@details.route("/like/<p_code>", methods=['POST'])
def likeside(p_code):
    like = request.form['like']
        
    # DB 연동 - 연결
    conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()
    email = session['ID']
    sql = 'update want set go_like=%s where e_mail ="'+ email + '" and p_code=' + str(p_code)
    cursor.execute(sql,like)
    conn.commit()
    conn.close()
    str_return = "/details/" + str(p_code)
    return  redirect(str_return)

@details.route("/normal/<p_code>", methods=['POST'])
def normalside(p_code):
    normal = request.form['normal']
        
    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
            password='1234', db='project_mc',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()  
    email = session['ID']
    sql = 'update want set go_like=%s where e_mail ="'+ email + '" and p_code=' + str(p_code)
    cursor.execute(sql,normal)
    conn.commit()
    conn.close()
    str_return = "/details/" + str(p_code)
    return  redirect(str_return)
    

@details.route("/hate/<p_code>", methods=['POST'])
def hateside(p_code):
    hate = request.form['hate']
    # DB 연동 - 연결
    conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()  
    email = session['ID']
    sql = 'update want set go_like=%s where e_mail ="'+ email + '" and p_code=' + str(p_code)
    cursor.execute(sql,hate)
    conn.commit()
    conn.close()
    str_return = "/details/" + str(p_code)
    return  redirect(str_return)

@details.route("/comment/<p_code>", methods=['POST'])
def comment(p_code):    
    # DB 연동 - 연결
    conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8')

    comment_str= request.form['comment']
    
    # 실행자 생성
    cursor = conn.cursor()  
    email = session['ID']
    sql = 'update want set go_comment=%s where e_mail ="'+ email + '" and p_code=' + str(p_code)
    cursor.execute(sql,comment_str)
    conn.commit()
    conn.close()

    str_return = "/details/" + str(p_code)
    return  redirect(str_return)