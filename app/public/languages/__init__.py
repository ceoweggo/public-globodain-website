from flask import Blueprint
public_global = Blueprint('global', __name__, url_prefix='/<lang_code>', template_folder='templates')
from . import routes