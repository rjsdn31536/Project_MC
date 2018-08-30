from flask import Blueprint, render_template, request, session, redirect
import googlemaps
import pymysql
import numpy as np
import pandas as pd

datalab = Blueprint('datalab', __name__, template_folder='dataLab')


@datalab.route('/')
def dataLab():
    return render_template('dataLab/datalab.html')