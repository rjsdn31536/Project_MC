
# coding: utf-8

# In[13]:


import os
import sys
import urllib.request
import json

def insertXY(addr):
    client_id = "tUqrLwYE5RBZ93YVPsdb"
    client_secret = "f3pO2qEAzi"
    encText = urllib.parse.quote(addr)
    url = "https://openapi.naver.com/v1/map/geocode?query=" + encText # json 결과
    # url = "https://openapi.naver.com/v1/map/geocode.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        dict_addr = json.loads(response_body.decode('utf-8'))
        return dict_addr['result']['items'][0]['point']
    else:
        return('error')

