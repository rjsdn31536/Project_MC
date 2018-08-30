
# coding: utf-8

# In[1]:


import random
import numpy as np
import pandas as pd


# In[19]:


# member DataFrame에 data를 집어넣는 함수
# ex) data_insert(1, 'rjsdn315@gmail.com', '010-5653-5259', '서울시 관악구 남부순환로 161길 45', 24, 'M', 4)
def data_insert(index, e_mail, phone_number, address, age, sex, family):
    global member
    member.loc[index] = {'e_mail' : e_mail, 
             'phone_number' : phone_number,
             'address' : address,
             'age' : age,
             'sex' : sex,
             'family' : family}


# In[52]:


def random_alpha_num():
    alpha_num = alpha_list + number_list
    return random.choice(alpha_num)


# In[94]:


def get_email():
    # email ID를 4글자에서 12글자로 Random 생성
    email = ''
    email_length = random.randint(4,13)
    for i in range(email_length):
        email += random_alpha_num()
    
    # email domain을 Random 생성
    email_domain = ['naver.com', 'google.com', 'daum.net']
    email = email + '@' + random.choice(email_domain)
        
    return email


# In[114]:


def get_phone_number():
    phone_num = '010-'
    phone_num = phone_num + str(random.randint(1000, 9999)) + '-' + str(random.randint(1000, 9999))
    return phone_num


# In[156]:


def get_address():
    park = pd.read_csv('./data/2018_parking_free.csv')
    rand = random.choice(park.index)
    
    return park.loc[rand].주소


# In[169]:


def get_age():
    return random.randint(20,101)


# In[170]:


def get_sex():
    return random.choice(['M', 'W'])


# In[171]:


def get_family():
    return random.randint(1,12)


# In[46]:


# alpha_list 는 알파벳 List(소문자)
alpha_list = []
for i in range(ord('a'), ord('z')+1):
    alpha_list.append(chr(i))


# In[49]:


# number_list 는 숫자 List
number_list = []
for i in range(0,10):
    number_list.append(str(i))


# In[6]:


member.loc[0].e_mail


# In[2]:


# 회원 DataFrame 틀 작성
# member 라는 dataframe 생성했고, 이 member에 data를 row단위로 insert할 예정
form_dict = {'e_mail' : ['rjsdn315@gmail.com'], 
             'phone_number' : ['010-5653-5259'],
             'address' : ['서울시 관악구 남부순환로 161길 45'],
             'age' : [24],
             'sex' : ['M'],
             'family' : [4]}

member = pd.DataFrame(form_dict)


# In[176]:


for i in range(1,501):
    data_insert(i, get_email(), get_phone_number(), get_address(), get_age(), get_sex(), get_family())


# In[179]:


# 멤버 데이터를 member.csv에 저장
member.to_csv('./data/member.csv', encoding='utf-8-sig')

