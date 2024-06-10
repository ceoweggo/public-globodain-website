from config.settings import Config

instance = 'development' # Development, Testing, Deployment
config = Config(instance)

# Configuración de MongoDB
MONGO_URI_APP = config.MONGO_URI_APP

from pymongo import MongoClient
client_app = MongoClient(MONGO_URI_APP)
db_app = client_app.get_default_database()