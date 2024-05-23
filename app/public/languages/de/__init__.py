from flask import Blueprint
public_language = Blueprint('public_de', __name__, template_folder='templates')
from . import routes
