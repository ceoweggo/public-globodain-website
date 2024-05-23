from flask import Blueprint
public_ = Blueprint('public', __name__, template_folder='templates')
from . import routes
