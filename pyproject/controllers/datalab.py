from flask import Blueprint, render_template, request, session, redirect
import googlemaps
import pymysql
import numpy as np
import pandas as pd
# googlemap api key
gmaps = googlemaps.Client(key='AIzaSyCoLfrAJNvN7zqZpqNGby1xYuZTOzkOGf0')

# Blueprint 클래스를 통한 모듈별 협업
# datalab의 변수에 Blueprint 인스턴스 생성
datalab = Blueprint('datalab', __name__, template_folder='dataLab')

# find_do 함수 생성
# db연동 후  execute_str문을 통해 각 도별 주차장수 카운트
def find_do(do):
    conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    execute_str = 'select count(*) cnt from parkinglot where p_province like %s'
    arg = ( do + '%' )
    cursor.execute(execute_str, arg)
    num = cursor.fetchone()
    conn.close()
    return num['cnt']

# datalab 라우터 설정
@datalab.route('/')
def dataLab():
    # 막대 그래프
    sido = ['전라남도', '울산광역시', '충청북도','강원도', '대구광역시', '광주광역시', '경상남도', '인천광역시', '부산광역시', '대전광역시', '서울특별시', '충청남도', '제주특별자치도', '세종특별자치시', '서울특별시', '경상북도', '전라북도', '경기도']
    sidoset = set(sido) # sido의 중복리스트를 없애기 위해 집합 변환
    sido_list = list(sidoset) # 다시 sido_list로 리스트 변환

    # 시도별 주차장 수 카운트 후 sido_count 리스트로 저장
    sido_count = []
    for i in sido_list:
        a = find_do(i)
        sido_count.append(a)
    
    # 점지도를 위해 json 형태로 만들기

    # 시도별 점의 가중치를 주기위해 동일한 비율로 변환
    sido_percent = []
    for i in sido_count:
        a = (i/sum(sido_count))*100
        sido_percent.append(a)
    
    # 구글을 통해 각 시도별 중심 위경도를 sido_addr 리스트로 저장
    sido_addr = []
    for i in sido_list:
        address = i
        addr = gmaps.geocode(address, language='ko')[0]['geometry']['location']
        sido_addr.append(addr)
    # sido_percent와 sido_addr리스트를 sido_json에 json의 형태로 저장
    sido_json = []
    for i in range(len(sido_list)):
        x = { "weight": sido_percent[i], "location": sido_addr[i] }
        sido_json.append(x)
    
    sidolist = sido_list
    sidocount  = sido_count

    return render_template('dataLab/datalab.html',sidolist=sidolist,sidocount=sidocount,sido_json=sido_json)
