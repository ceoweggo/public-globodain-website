from flask import redirect,url_for,request,flash
from app.auth.functions import Functions

from . import auth_

class Requests:

    @auth_.route('/requests/demo', methods=['GET', 'POST'])
    def request_business_demo():

        form = request.form.get

        items = {
            'fullname': form('demoName')+' '+form('demoLastname'),
            'email': form('demoEmail'),
            'business': {
                'company': form('demoBusinessName'),
                'cif': form('demoCIF'),
                'position': form('demoPosition'),
                'phone': form('demoPhone')
            }
        }

        Functions.Requests.request_business_demo(items)

        flash('¡Gracias por solicitar nuestra demo! el equipo de soporte contactará contigo en las próximas horas.','success')
        return redirect(url_for('public_es.hospitality_demo'))
