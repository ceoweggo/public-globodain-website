from flask import Blueprint
public_language = Blueprint('public_fr', __name__, template_folder='templates')
from . import routes
