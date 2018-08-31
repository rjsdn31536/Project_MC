import pymysql

def find_do(do):
    conn = pymysql.connect(host='127.0.0.1',user = 'root',
         password='1234', db='project_mc',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    execute_str = 'select count(*) cnt from parkinglot where p_province like %s'
    arg = ( do + '%' )
    cursor.execute(execute_str, arg)
    b = cursor.fetchone()
    conn.close()
    return b['cnt']

# print(a, b, c)

sido = ['전라남도', '울산광역시', '충청북도','강원도', '대구광역시', '광주광역시', '경상남도', '인천광역시', '부산광역시', '대전광역시', '서울특별시', '충청남도', '제주특별자치도', '세종특별자치시', '서울특별시', '경상북도', '전라북도', '경기도']
sidoset = set(sido)
sido_list = list(sidoset)


sido_count = []
for i in sido_list:
    a = find_do(i)
    sido_count.append(a)



"""
conn = pymysql.connect(host='127.0.0.1',user = 'root',
         password='1234', db='pythondb1',charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    
cursor = conn.cursor()
    
execute_str = 'select p_province from parkinglot;'
    
cursor.execute(execute_str)
    
sido_data = cursor.fetchall()
# print(type(sido_data))


sido_data[0]['p_province']
sido =[]

for i in range(0,len(sido_data)):
    sido.append(sido_data[i]['p_province'])

sidoset = set(sido)
sido_list = list(sidoset)



sido_count = []

for i in sido_list:
    c = 0
    for j in sido:
        if j == i:
            c += 1
    sido_count.append(c)

print(sido_list)
print(sido_count)



conn.commit()
    
# print(sido)

conn.close()
    # set_sido = set(sido_data)
    # sido_list = list(set_sido)
    
    # sido_count = []
    # for i in sido_list:
    #     c = 0
    #     for j in sido_data:
    #         if j == i:
    #             c += 1
    #     sido_count.append(c)
    # sidolist = sido_list
    # sidocount = sido_count
"""