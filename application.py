"""
<!-- -| 
  * Globodain is a registered trademark of Globodain Technology Corporation, S.L
  * Any disclosure of this code violates intellectual property laws.
  * Developed by Ruben Ayuso. 
|- -->
""" 

from config.db.connection import instance

from app import gd_app
application = gd_app(instance)

deployment_mode = False

if __name__ == "__main__":
  if not deployment_mode:
    application.run(port=4000, debug=True)
  else:
    # DEPLOYMENT SERVER (SIMILAR TO WSGI)
    from waitress import serve
    serve(application, host="0.0.0.0", port=8080)