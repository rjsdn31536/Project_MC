
from flask import Flask, render_template
from controllers.search import search
from controllers.details import details

# app 객체 생성
app = Flask(__name__)

@app.route("/")
def login():
    return render_template('login/login.html')

@app.route("/login_result", methods=['POST'])
def login_result():
    return render_template('login/login_result.html')

@app.route("/member")
def member():
    return render_template('member/member.html')


@app.route("/signup_com")
def signup_com():
    return render_template('login/signup_com.html')

app.register_blueprint(search,url_prefix = '/search')
app.register_blueprint(details,url_prefix = '/details')

# app 실행
if __name__ == "__main__":
    app.run(debug=True)