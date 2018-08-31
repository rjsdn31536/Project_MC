# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, session
import googlemaps
import pymysql
import numpy as np
import pandas as pd

gmaps = googlemaps.Client(key='AIzaSyCoLfrAJNvN7zqZpqNGby1xYuZTOzkOGf0')

search = Blueprint('search', __name__, template_folder='search')

park = dict()

# http://localhost:5000/search/
@search.route("/", methods=['GET', 'POST'])
def searchpage():
    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                    password='1234', db='project_mc',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 실행자 생성
    cursor = conn.cursor()   

    # 로그인을 안하고 /search/에 강제 접속할 경우 return redirect
    try:
        session['ID']
        e_mail = session['ID']
        
    # 로그인이 되어는 있지만 /search/로 강제 접속하는 경우
    except:
        try:
            e_mail = request.form['email']
        except:
            return redirect('/')
        



    execute_str = 'select * from member where e_mail = "' + e_mail + '"'

    cursor.execute(execute_str)
    member_data = cursor.fetchall()

    if member_data == ():
        return redirect('/')

    

    # 로그인에 성공한 경우
    session['ID'] = e_mail

    # 로그인 완료
    session['logged_in'] = True
    
    execute_str = 'select p_code from want where e_mail = "' + e_mail + '"'
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

@search.route("/result/", methods=['GET', 'POST'])
def searchResult():
    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                    password='1234', db='project_mc',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()   

    # 로그인을 안하고 /result/에 강제 접속할 경우 return redirect
    try:
        session['logged_in']
    except:
        return redirect('/')

    # 로그인을 한 상태에서 /result/에 강제 접속하는 경우(역삼역으로 초기값)
    # 본인 위치 확인이 가능하면 본인 위치 주변의 위치 찾으면 좋을듯!
    try:
        address = request.form['address']
    except:
        address = '서울역'

    # 아무것도 검색을 안했을 경우 서울역으로 초기값 설정하여 검색해줌
    # 본인 위치 확인이 가능하면 본인 위치 주변의 위치 찾으면 좋을듯!
    try:
        addr_ll = gmaps.geocode(address, language='ko')[0]['geometry']['location']
    except:
        addr_ll = gmaps.geocode('서울역', language='ko')[0]['geometry']['location']

    addr_x = addr_ll['lat']
    addr_y = addr_ll['lng']

    a = addr_x + 0.010
    b = addr_x - 0.010
    c = addr_y + 0.025
    d = addr_y - 0.025
    
    execute_str = "select * from parkinglot where (p_lat > " + str(b) + ") and (p_lat < " + str(a) + ") and (p_long > "+ str(d) + ") and (p_long < " + str(c)+ ")"

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
            'p_date1' : i[10],
            'p_date2' : i[11],
            'p_date3' : i[12],
            'p_date4' : i[13],
            'p_date5' : i[14]
        }
    p_count = len(park_data)

    conn.close()

    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                    password='1234', db='project_mc',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
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
    
    conn.close()


    return render_template('search_result/search_result.html', 
            address=str(address), addr_x=addr_x, addr_y=addr_y, park = park, p_count=p_count,
            park_want_list = park_want_list, park_want_len = len(park_want_list), park_code_list =park_code_list)


@search.route("/logout")
def logout():
    session.pop('ID', None)
    session.pop('logged_in', None)

    return redirect('/')
