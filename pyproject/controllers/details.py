import pymysql
from flask import Blueprint, render_template, request
# db연동
# conn = pymysql.connect( host='localhost',  port=5000, user='root',  passwd='1234', db='pythondb', charset='utf8')


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

# 날짜 선택 값이 db로 저장
# @details.route("회원관리 page", methods = ["POST"])
# def memberpage():
#     cursor  = conn.curosr()
#     cursor.execute("insert into ")
#     conn.commit
#     conn.close()
#     return render_template()


