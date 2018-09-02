# 공공주차장 웹 서비스 프로젝트

1. 데이터 전처리
1) data 폴더에 있는 2018_parking_free.csv와 2018_parking_school.csv를 다운 받는다.

2) Read_data.py로 위의 두 csv 파일을 전처리하여 combine 해서 final.csv를 만들어 준다. 그리고 Insert_RandomDATA.py를 통해 임의의 회원을 생성한 후 member.csv로 출력한다.

3) database 생성을 위해 create_code.txt 파일의 database 정보를 쿼리로 돌려준다. (database를 mysql 혹은 mariadb에서 실행한다.)

4) final.csv를 parkinglot 테이블에 입력한 후, memeber.csv를 member 테이블에 입력해준다.



2. 데이터 시각화
- 공공주차장 데이터를 활용한 시각화는 두가지로 진행했는데 하나는 막대그래프, 다른 하나는 네이버 지도를 이용한 점지도를 만들었다.

- 요구되는 정보는 각 시도별 공공주차장 수였다.

- datalab.py를 생성, Blueprint 클래스로 app.py에 연동,db에 연동한 후 각 시도별 주차장 수 카운트 하는 find_do 함수 생성, find_do 함수를 통해 각 시도별 주차장 수 카운트, 필요한 정보 추출 후 저장, sido_list(시도별 리스트), sido_count(시도별 주차장수), sido_percent(시도별 주차장수 퍼센트), sido_addr(시도별 중심위경도 리스트), sido_json(sido_percent와 sido_addr를 json 형태로 저장)

- 막대그래프
    1) chart.js를 활용, sido_list를 label, sido_count를 data로 넣어서 막대그래프 출력하였다.
    2) for문과 if문을 통해 data가 1000이 넘는 부분과 그렇지 않은 부분은 막대그래프 색상으로 구분지었다.

- 점지도
    1) 네이버 지도를 이용하기에 naver map api key가 필요하다.
    2) 등록된 자신의 아이디를 html head 영역에 가져오는데 중요한 것은 점지도를 만드는 것이기에 geocoder 뒤에 drawings, visualization를 붙여야한다. 그렇지 않으면 생성이 안됀다.
    3) new naver.maps.Map를 통해 기본 맵, 기본줌과 중심이 될 위경도 설정한다.
    4) datalab.py에서 만든 sido_json를 data에 넣어준다.
    5) naver.maps.visualizaiton.DotMap 인스턴스로 점지도를 출력한다.

3. pyproject 폴더를 들어가 app.py를 실행한다. 웹으로 가서 사이트 구경하길 바란다.

4. 오류있으면 feedback 부탁합니다.



