import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import platform
from matplotlib import font_manager, rc
from insert_XY import insertXY

import googlemaps
gmaps = googlemaps.Client(key='AIzaSyCoLfrAJNvN7zqZpqNGby1xYuZTOzkOGf0')

# 자치단체 주차장 현황 data 삽입
park = pd.read_csv('./data/2018_parking_free.csv')

# column name을 보기 편하게 변경
park.rename(columns={"주차장유형 (노상/노외/부설)":"주차장유형",
                  "전화번호 (주차장관리자)":"전화번호"}, inplace=True)

# 주차장명이 없는 CASE
row, col = park.shape
for i in range(row):
    # 주차장명이 float(nan) 인 경우 해당 row를 삭제
    if type(park['주차장명'][i]) == float:
        park.drop([i], inplace=True)

# 개방시작, 개방종료 시간 양식 통일화
# ex1) 0:00 -> 00:00
# ex2) 미개방 -> nan
for cols in park.keys():
    if '개방' in cols:
        num = 0
        for i in park[cols]:
            try: 
                # Case i == nan (예외처리)
                len(i)
            except:
                1
            else:
                # ex1)
                if len(i) == 4:
                    park[cols][num] = '0' + i
            finally:
                num += 1
                # ex2)
                if i == '미개방':
                    park[cols][num] = np.nan


# 개방시작시간, 개방종료시간 combine
# 14일 00:00, 24:00 -> 14,00:00~24:00
# day_flag(개방시작시간) == 0
# day_flag(개방종료시간) == 1
day_flag = 0
for cols in park.keys():
    # 개방시작시간 읽으면서 종료시간까지 읽고 combine하여 새로운 column 생성
    if '개방' in cols and day_flag == 0:
        day_flag = 1
        days, tmp = cols.split(', ')
        year, month, day_week = days.split('.')
        new_cols = month+'.'+day_week
        day, week = day_week.split('(')
        
        park[new_cols] = day + ',' + park[cols] + '~' + park[days+', 개방종료시간']
        park.rename(columns={cols:days}, inplace=True)
        
    elif day_flag == 1:
        day_flag = 0

# 기존의 날짜 column 삭제
for cols in park.keys():
    if "'18" in cols or 'Unnamed' in cols:
        del park[cols]

# 위도가 비어있는 부분을 찾아 print하여 확인하는 작업
# print를 이제 dict에서 x, y에 저장해야 하지만 데이터를 못찾는 부분이 존재함
for i in park.index:
    # park의 위도, 경도가 nan이 아닌 경우
    if type(park['위도'][i]) == str:
        continue
    # park의 위도, 경도가 nan인 경우
    if np.isnan(park['위도'][i]) or park['위도'][i] < 30:
        # 네이버 api를 활용하여 1차 검색
        # 네이버 api는 주소로만 검색이 가능해서 건물명이 나오면 ERROR 발생
        # ERROR 발생하면 except 구문 안에서 gmap 활용하여 재 검색하여 확실한 위경도 확인
        try :
            addr_xy = insertXY(park['주소'][i])
            # naver api는 x축과 y축이 반대로 나와있음
            addr_x = str(addr_xy['y'])
            addr_y = str(addr_xy['x'])
        # 구글 api를 활용하여 2차 검색
        # 건물명으로도 확인이 가능하여 더 섬세한 검색 가능
        except:
            # 예외처리가 실질적으로 필요하지 않은 구문이지만 Index가 잘못됐다는 에러가 나옴
            # 분명 for i in park.index로 존재하는 index만 반복해야하는게 맞지만 메모리 처리상에서 충돌하는듯
            # 예외처리를 해두면 문제는 발생하지 않음! 한칸 넘어가서 데이터를 처리하는 것과 같은 문제 X
            # 나중에 다시 확인하여 확실하게 할것! 일단 데이터는 확실하게 잘 들어감.
            try :
                addr_ll = gmaps.geocode(park['주소'][i], language='ko')[0]['geometry']['location']
                addr_x = str(addr_ll['lat'])
                addr_y = str(addr_ll['lng'])
            except :
                1
        finally:
            park['위도'][i] = addr_x
            park['경도'][i] = addr_y

# 학교 무료 개방 주차장 현황 data 삽입
school = pd.read_csv('./data/2018_parking_school.csv')

# column name을 보기 편하게 변경
school.rename(columns={"교육청":"시도",
                       "주차장명(학교명)":"주차장명",
                       "주차장유형 (노상/노외/부설)":"주차장유형",
                       "전화번호 (주차장관리자)":"전화번호"}, inplace=True)                  

for i in school.index:
    # 관리기관의 data가 nan인 경우 어차피 교육청이 관리하므로 교육청을 복사해줌!
    if type(school.loc[i].관리기관) == float:
        school.loc[i].관리기관 = school.loc[i].시도 + '교육청'

# 개방시작, 개방종료 시간 양식 통일화
# ex1) 0:00 -> 00:00
# ex2) 미개방 -> nan
for cols in school.keys():
    if '개방' in cols:
        num = 0
        for i in school[cols]:
            if type(i) == float:
                if np.isnan(i):
                    continue
            if len(i) == 4:
                school[cols][num] = '0' + i
            num += 1

# 개방시작시간, 개방종료시간 combine
# 14일 00:00, 24:00 -> 14,00:00~24:00
# day_flag(개방시작시간) == 0
# day_flag(개방종료시간) == 1
day_flag = 0
for cols in school.keys():
    # 개방시작시간 읽으면서 종료시간까지 읽고 combine하여 새로운 column 생성
    if '개방' in cols and day_flag == 0:
        day_flag = 1
        days, tmp = cols.split(', ')
        year, month, day_week = days.split('.')
        new_cols = month+'.'+day_week
        day, week = day_week.split('(')
        
        school[new_cols] = day + ',' + school[cols] + '~' + school[days+', 개방종료시간']
        school.rename(columns={cols:days}, inplace=True)
        
    elif day_flag == 1:
        day_flag = 0

# 기존의 날짜 column 삭제
for cols in school.keys():
    if "'18" in cols or 'Unnamed' in cols:
        del school[cols]

# 위도가 비어있는 부분을 찾아 print하여 확인하는 작업
# print를 이제 dict에서 x, y에 저장해야 하지만 데이터를 못찾는 부분이 존재함
for i in school.index:
    # park의 위도, 경도가 nan이 아닌 경우
    if type(school['위도'][i]) == str:
        continue
    # park의 위도, 경도가 nan인 경우
    if np.isnan(school['위도'][i]):
        # 구글 api를 활용하여 검색
        # 건물명으로도 확인이 가능하여 더 섬세한 검색 가능
        # 예외처리가 실질적으로 필요하지 않은 구문이지만 Index가 잘못됐다는 에러가 나옴
        # 분명 for i in school.index로 존재하는 index만 반복해야하는게 맞지만 메모리 처리상에서 충돌하는듯
        # 예외처리를 해두면 문제는 발생하지 않음! 한칸 넘어가서 데이터를 처리하는 것과 같은 문제 X
        # 나중에 다시 확인하여 확실하게 할것! 일단 데이터는 확실하게 잘 들어감.
        try :
            address_combine = school.loc[i].시도 + ' ' + school.loc[i].주소
            addr_ll = gmaps.geocode(address_combine, language='ko')[0]['geometry']['location']
            addr_x = str(addr_ll['lat'])
            addr_y = str(addr_ll['lng'])
        except :
            1
        finally:
            school.loc[i].위도 = addr_x
            school.loc[i].경도 = addr_y

# 날짜 columns 을 월과 일 구분자 .에서 _로 바꾸는 과정
# school.loc[index]를 하면 object로 나오는데 이 과정에서 .를 사용해야 하기 때문.
for cols in school.keys():
    if '.' in cols:
        month, day = cols.split('.')
        name = month+'_'+day
        school.rename(columns={cols:name}, inplace=True)

# park 데이터와 school 데이터 combine
combined = pd.merge(park, school, how='outer')

# final.csv를 저장
combined.to_csv('/data/final_data.csv', encoding='utf-8-sig')