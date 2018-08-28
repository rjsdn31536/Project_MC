from flask import Blueprint, render_template, request
import googlemaps
import numpy as np
import pandas as pd

form_dict = {'e_mail' : ['rjsdn315@gmail.com'], 
             'phone_number' : ['010-5653-5259'],
             'address' : ['서울시 관악구 남부순환로 161길 45'],
             'age' : [24],
             'sex' : ['M'],
             'family' : [4]}

member = pd.DataFrame(form_dict)

gmaps = googlemaps.Client(key='AIzaSyCoLfrAJNvN7zqZpqNGby1xYuZTOzkOGf0')

search = Blueprint('search', __name__, template_folder='search')



# http://localhost:5000/search/
@search.route("/")
def searchpage():
    return render_template('search/index.html')

@search.route("/result/", methods=['POST'])
def searchResult():
    address = request.form['address']
    addr_ll = gmaps.geocode(address, language='ko')[0]['geometry']['location']
    addr_x = str(addr_ll['lat'])
    addr_y = str(addr_ll['lng'])

    # return render_template('search_result/search_result.html')
    return render_template('search_result/search_result.html', address=str(address), addr_x=float(addr_x), addr_y=float(addr_y), member=dict(form_dict))