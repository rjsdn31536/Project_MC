from flask import Blueprint, render_template, request
import googlemaps
import pymysql
import numpy as np
import pandas as pd
# 문자열에서 숫자만 추출하는 모듈
import re




details = Blueprint('details', __name__, template_folder='details')



@details.route("/")
def detailpage():
    # db연동 -> 
    dateList = ["14일","15일","16일","17일"]
    addr_x = 37.3595704
    addr_y = 127.105399
    # 만족도 조사
    return render_template('details/details.html',
    dateList=dateList, addr_x=addr_x,addr_y=addr_y)

@details.route("/<p_code>")
def detailpage2(p_code):
    p_code_num = int(re.findall('\d+', p_code)[0])

    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                       password='1234', db='Project_MC',charset='utf8')
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
    return render_template('details/details.html', park=park, p_num = park_num)



