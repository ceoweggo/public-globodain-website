
from flask import Flask,render_template
import os

app = Flask(__name__, instance_relative_config=True)
app_root = os.path.dirname(os.path.abspath(__file__))
app.config['static_url'] = os.path.join(app_root, 'static') # Ruta definida para wkhtmltopdf

from flask_dropzone import Dropzone
dropzone = Dropzone()

from flask_mail import Mail
mail = Mail()

from flask_breadcrumbs import Breadcrumbs
Breadcrumbs(app=app)

from flask_recaptcha import ReCaptcha
recaptcha = ReCaptcha()

languages = {}
app_language = os.environ.get("DEFAULT_LANG")

def gd_app(instance):
    # Load the environment parameters configuration
    from config.settings import Config
    Config(instance).update_app_config(app)

    # Force to close session
    from datetime import timedelta
    app.permanent_session_lifetime = timedelta(minutes=10080)

    app.config.update({
        'RECAPTCHA_ENABLED': True,
        'RECAPTCHA_SITE_KEY': '6LdPkEEpAAAAAEZtlgG4TJh6v5Rc9yxcfH6mL4ws',
        'RECAPTCHA_SECRET_KEY': '6LdPkEEpAAAAAIikUXKNTSJXfkDnk7wslcHPc_T6',
    })
    
    dropzone.init_app(app)
    mail.init_app(app)
    recaptcha.init_app(app)

    # Creamos url estáticas por cada lenguage para mejorar el SEO y guardar páginas individuales

    # Main Blueprint
    from .public import public_
    app.register_blueprint(public_)
    from .auth import auth_
    app.register_blueprint(auth_)
    ## Global
    from .public.languages import public_global
    app.register_blueprint(public_global)

    ### ES
    from .public.languages.es import public_language
    app.register_blueprint(public_language, url_prefix="/es/")
    ### EN
    from .public.languages.en import public_language
    app.register_blueprint(public_language, url_prefix="/en/")

    from .libraries import libraries_gtc
    app.register_blueprint(libraries_gtc)

    app.register_error_handler(400, errors.page_refresh)
    app.register_error_handler(404, errors.page_not_found)
    app.register_error_handler(403, errors.page_not_access)
    app.register_error_handler(401, errors.page_only_col)
    app.register_error_handler(406, errors.page_only_users_except_autor)

    return app

class errors:
    def page_refresh(e):
        return render_template('errors/404.html'), 400
    """
    def page_not_found(e):
        response = jsonify({
            'message': 'Resource not found\n' + request.url,
            'status': 404
        })
        response.status_code = 404
        return render_template('errors/404.html'), response
    """
    def page_not_found(e):
        return render_template('errors/404.html'), 404
        
    def page_not_access(e):
        return render_template('errors/403.html'), 403

    def page_only_col(e):
        return render_template('errors/401.html'), 401

    def page_only_users_except_autor(e):
        return render_template('errors/406.html'), 406
