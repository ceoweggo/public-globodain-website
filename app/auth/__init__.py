from flask import Blueprint
auth_ = Blueprint('auth', __name__, template_folder='templates')
from . import routes
