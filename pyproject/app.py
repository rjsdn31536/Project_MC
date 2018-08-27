
from flask import Flask, render_template
from controllers.search import search
from controllers.details import details

# app 객체 생성
app = Flask(__name__)

# 라우터 설정
@app.route('/')
def main():
    return "main page"

app.register_blueprint(search,url_prefix = '/search')
app.register_blueprint(details,url_prefix = '/details')

# app 실행
if __name__ == "__main__":
    app.run(debug=True)