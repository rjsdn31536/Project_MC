from flask import Blueprint, render_template, request, session, redirect
import googlemaps
import pymysql
import numpy as np
import pandas as pd

datalab = Blueprint('datalab', __name__, template_folder='dataLab')


@datalab.route('/')
def dataLab():
    return render_template('dataLab/datalab.html')


# 마커클러스터 표시 실패
# @datalab.route("/")
# def dataLab():
    # DB 연동 - 연결
    # conn = pymysql.connect(host='127.0.0.1',user = 'root',
    #                 password='1234', db='pythondb1',charset='utf8')
    # cursor = conn.cursor()   
    # execute_str = "select * from parkinglot"

    # cursor.execute(execute_str)
        
    # park_data = cursor.fetchall()
    # conn.commit()
    # # print(park_data)
    # # park를 json 형식으로 저장
    # park = dict()

    # for i in park_data:
    #     park_num = 'p_' +str(i[0])

    #     park[park_num] = {                 
    #         'p_province' : i[1], 
    #         'p_name' : i[2],
    #         'p_type' : i[3],
    #         'p_address' : i[4],
    #         'p_lat' : float(i[5]),
    #         'p_long' : float(i[6]),
    #         'p_admit' : i[7],
    #         'p_number' : i[8],
    #         'p_desp' : i[9],
    #         'p_date1' : i[10],
    #         'p_date2' : i[11],
    #         'p_date3' : i[12],
    #         'p_date4' : i[13],
    #         'p_date5' : i[14]
    #     }
    # conn.close()
    # # 실행자 생성
    # return render_template('dataLab/markercluster.html',park=park)