from pathlib import Path
from dotenv import load_dotenv
import os

class Config(object):
    def __init__(self, environment):
        self.environment = environment
        self.load_env_variables()
        self.set_environment()

    def load_env_variables(self):
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)
        self.SECRET_KEY = os.getenv('SECRET_KEY')

        self.CSRF_ENABLED = False  # O el valor que desees por defecto
        self.WTF_CSRF_ENABLED = False  # O el valor que desees por defecto

        # Database
        self.MONGO_URI_APP = os.getenv("DATABASE_TESTING_URL")

    def set_environment(self):
        if self.environment == 'deployment':
            self.set_deployment_env()
        elif self.environment == 'testing':
            self.set_testing_env()
        else:
            self.set_default_env()

    def set_deployment_env(self):
        # Configuración para el entorno de despliegue
        self.ENV = "deployment"
        self.DEBUG = False
        self.CSRF_ENABLED = True
        self.WTF_CSRF_ENABLED = True

        self.MONGO_URI_APP = os.getenv("DATABASE_REMOTE_URL")

        self.SESSION_COOKIE_SECURE = True
        self.SESSION_COOKIE_HTTPONLY = True
        self.SESSION_COOKIE_SAMESITE = 'GTC'

    def set_testing_env(self):
        # Configuración para el entorno de pruebas
        self.ENV = "testing"
        self.DEBUG = True

        self.MONGO_URI_APP = os.getenv("DATABASE_TESTING_URL")

    def set_default_env(self):
        # Configuración por defecto
        self.ENV = "development"
        self.DEBUG = True
        self.OAUTHLIB_INSECURE_TRANSPORT = True

        self.MONGO_URI_APP = os.getenv("DATABASE_LOCAL_URL")
        
    def update_app_config(self, app):
        app.config.update(
            DEBUG=self.DEBUG,
            FLASK_ENV=self.ENV,
            FLASK_APP=os.getenv('FLASK_APP'),
            SECRET_KEY=self.SECRET_KEY,
            MONGO_URI_APP=self.MONGO_URI_APP,
            CSRF_ENABLED=self.CSRF_ENABLED,
            WTF_CSRF_ENABLED=self.WTF_CSRF_ENABLED,
        )