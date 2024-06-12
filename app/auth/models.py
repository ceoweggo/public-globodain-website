from config.db.connection import db_app
from datetime import datetime

class Models():

    class Requests:
 
        def business_demo(items):
            return db_app.requests.insert_one({
                'type': 'demo',
                'subtype': '-',
                'details': items,
                'status': 'pending',
                'updated': None,
                'created': datetime.now()
            })