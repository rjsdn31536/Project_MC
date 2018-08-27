from flask import Blueprint, render_template, request
import googlemaps

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
    return render_template('search_result/search_result.html', address=str(address), addr_x=float(addr_x), addr_y=float(addr_y))

