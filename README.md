# 공공주차장 웹 서비스 프로젝트

1. 데이터 전처리
1) data 폴더에 있는 2018_parking_free.csv와 2018_parking_school.csv를 다운 받는다.

2) Read_data.py로 위의 두 csv 파일을 전처리하여 combine 해서 final.csv를 만들어 준다. 그리고 Insert_RandomDATA.py를 통해 임의의 회원을 생성한 후 member.csv로 출력한다.

3) database 생성을 위해 create_code.txt 파일의 database 정보를 쿼리로 돌려준다. (database를 mysql 혹은 mariadb에서 실행한다.)

4) final.csv를 parkinglot 테이블에 입력한 후, memeber.csv를 member 테이블에 입력해준다.

2. pyproject 폴더를 들어가 app.py를 실행한다. 웹으로 가서 사이트 구경하길 바란다.

3. 오류있으면 feedback 부탁합니다.



