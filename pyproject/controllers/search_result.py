import pymysql
# DB 연결
conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='12345',
    db='project_mc',charset='utf8')
print('연결완료')

cursor = conn.cursor()

cursor.execute()

