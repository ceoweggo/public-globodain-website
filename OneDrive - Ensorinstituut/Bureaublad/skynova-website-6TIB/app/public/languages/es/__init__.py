from flask import Blueprint
public_language = Blueprint('public_es', __name__, template_folder='templates')
from . import routes
