from flask import Blueprint, render_template, request


details = Blueprint('details', __name__, template_folder='details')


@details.route("/")
def detailpage():
    return render_template('details/index.html')


