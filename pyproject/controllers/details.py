import pymysql
from flask import Blueprint, render_template
# db연동
# conn = pymysql.connect( host='localhost',  port=5000, user='root',  passwd='1234', db='pythondb', charset='utf8')


details = Blueprint('details', __name__, template_folder='details')



@details.route("/")
def detailpage():
    # db연동으로 해당 주차장의 날짜 리스트 불러오기
    dateList = ["14일","15일","16일","17일"]
    return render_template('details/index.html',dateList=dateList)

# 날짜 선택 값이 db로 저장
# @details.route("회원관리 page", methods = ["POST"])
# def memberpage():
#     cursor  = conn.curosr()
#     cursor.execute("insert into ")
#     conn.commit
#     conn.close()
#     return render_template()


