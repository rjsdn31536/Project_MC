from flask import Blueprint, render_template, request, session, redirect
import googlemaps
import pymysql
import numpy as np
import pandas as pd

gmaps = googlemaps.Client(key='AIzaSyCoLfrAJNvN7zqZpqNGby1xYuZTOzkOGf0')


datalab = Blueprint('datalab', __name__, template_folder='dataLab')

def find_do(do):
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
         password='1234', db='pythondb1',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    execute_str = 'select count(*) cnt from parkinglot where p_province like %s'
    arg = ( do + '%' )
    cursor.execute(execute_str, arg)
    num = cursor.fetchone()
    conn.close()
    return num['cnt']


@datalab.route('/')
def dataLab():
    # 막대 그래프
    sido = ['전라남도', '울산광역시', '충청북도','강원도', '대구광역시', '광주광역시', '경상남도', '인천광역시', '부산광역시', '대전광역시', '서울특별시', '충청남도', '제주특별자치도', '세종특별자치시', '서울특별시', '경상북도', '전라북도', '경기도']
    sidoset = set(sido)
    sido_list = list(sidoset)

    sido_count = []
    for i in sido_list:
        a = find_do(i)
        sido_count.append(a)
    
    # 점지도를 위해 json 형태로 만들기
    sido_percent = []
    for i in sido_count:
        a = (i/sum(sido_count))*100
        sido_percent.append(a)
    sido_addr = []
    for i in sido_list:
        address = i
        addr = gmaps.geocode(address, language='ko')[0]['geometry']['location']
        sido_addr.append(addr)
    sido_json = []
    for i in range(len(sido_list)):
        x = { "weight": sido_percent[i], "location": sido_addr[i] }
        sido_json.append(x)
    
    sidolist = sido_list
    sidocount  = sido_count

    return render_template('dataLab/datalab.html',sidolist=sidolist,sidocount=sidocount,sido_json=sido_json)
