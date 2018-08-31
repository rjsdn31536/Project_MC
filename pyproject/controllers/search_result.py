import pymysql
# DB 연결
conn = pymysql.connect(host='mc-project.crzhz77savee.ap-northeast-2.rds.amazonaws.com',port=3306,user='mc_project',passwd='multicampus', db='pythondb',charset='utf8')
print('연결완료')

cursor = conn.cursor()

cursor.execute()

