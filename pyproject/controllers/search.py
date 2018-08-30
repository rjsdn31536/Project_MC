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
                    password='1234', db='pythondb1',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    # 실행자 생성
    cursor = conn.cursor()   

    # 로그인을 안하고 /search/에 강제 접속할 경우 return redirect
    try:
        e_mail = request.form['email']
    except:
        return redirect('/')

    execute_str = 'select * from member where e_mail = "' + e_mail + '"'

    cursor.execute(execute_str)
    member_data = cursor.fetchall()

    # 로그인에 실패한 경우
    if member_data == ():
        return redirect('/')

    # 로그인에 성공한 경우
    else:
        session['ID'] = e_mail
        return render_template('search/index.html', member_data=member_data)

@search.route("/result/", methods=['POST'])
def searchResult():
    # DB 연동 - 연결
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
                    password='1234', db='pythondb1',charset='utf8')
    # 실행자 생성
    cursor = conn.cursor()   

    address = request.form['address']
    addr_ll = gmaps.geocode(address, language='ko')[0]['geometry']['location']
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
    return render_template('search_result/search_result.html', address=str(address), addr_x=addr_x, addr_y=addr_y, park = park, p_count=p_count)

