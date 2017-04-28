from flask import Blueprint
wifi_views = Blueprint('wifi_views', __name__)

from . import views
