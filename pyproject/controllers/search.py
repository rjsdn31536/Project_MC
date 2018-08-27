from flask import Blueprint, render_template, request


search = Blueprint('search', __name__, template_folder='search')

# http://localhost:5000/search/
@search.route("/")
def searchpage():

    return render_template('search/index.html')

@search.route("/result")
def searchResult():

    return render_template('search_result/search_result.html')

