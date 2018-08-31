import googlemaps
import pymysql
import numpy as np
import pandas as pd
gmaps = googlemaps.Client(key='AIzaSyCoLfrAJNvN7zqZpqNGby1xYuZTOzkOGf0')

def find_do(do):
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
         password='1234', db='pythondb1',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    execute_str = 'select count(*) cnt from parkinglot where p_province like %s'
    arg = ( do + '%' )
    cursor.execute(execute_str, arg)
    b = cursor.fetchone()
    conn.close()
    return b['cnt']

# print(a, b, c)

# sido = ['전라남도', '울산광역시', '충청북도','강원도', '대구광역시', '광주광역시', '경상남도', '인천광역시', '부산광역시', '대전광역시', '서울특별시', '충청남도', '제주특별자치도', '세종특별자치시', '서울특별시', '경상북도', '전라북도', '경기도']
# sidoset = set(sido)
# sido_list = list(sidoset)

sido_list = ['광주광역시', '경상남도', '세종특별자치시', '강원도', '대전광역시', '대구광역시', '인천광역시', '충청북도', '전라북도', '충청남도', '서울특별시', '경기도', '부산광역시', '제주특별자치도', '경상북도', '울산광역시', '전라남도']

sido_count = []
for i in sido_list:
    a = find_do(i)
    sido_count.append(a)
sido_percent = []
for i in sido_count:
    a = (i/sum(sido_count))*100
    sido_percent.append(a)

print(sido_percent)

sido = []
for i in sido_list:
    address = i
    addr_ll = gmaps.geocode(address, language='ko')[0]['geometry']['location']
    sido.append(addr_ll)

print(sido)

c = []
for i in range(len(sido_list)):
    # print(i)
    x = { "weight": sido_percent[i], "location": sido[i] }
    c.append(x)
print(c)
