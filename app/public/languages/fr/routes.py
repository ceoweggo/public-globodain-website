from . import public_language
from flask_breadcrumbs import register_breadcrumb
from flask import render_template,session,request,flash,redirect,url_for,g
from werkzeug.urls import url_parse
from datetime import datetime

from app.libraries.mailing.models import emails

from config.db.connection import db_app as gd
from app import app

import json, random

@public_language.before_request
def language():
    # Reseteamos el lenguaje al visitar la url
    session['lang'] = 'fr'
    session['lang_code'] = session['lang']

    global lang
    lang = session['lang'] 

    # Cargar el archivo JSON correspondiente al idioma seleccionado
    with open(f'app/lang/{lang}.json', 'r', encoding='utf8') as file:
        g.lang_data = json.loads(file.read())

def find_data(function):
    data = {}
    for i in g.lang_data:
    
        if i['page'] == function:
            data['page'] = i

        if i['page'] == 'data_lang_common':
            data['common'] = i

    return data

# Breadcrumbs load
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
default_breadcrumb_root(public_language, '.')


@public_language.route('/', methods=['GET'])
@register_breadcrumb(public_language, '.fr_index', 'Globodain')
def index():
    #from app.libraries.announcements.functions import home_announcement
    #data_announcement = home_announcement(1,lang)
    return render_template('es-landing.html', 
                           lang_data=find_data('index'),
                           #"""announcement=data_announcement[0], url=data_announcement[1],"""
                           header_dark_mode=False)

# Newsletter function
@public_language.route("/newsletter", methods=['GET', 'POST'])
def add_user_to_newsletter():
    form = request.form.get
    email = form('email')

    if gd.db.users_newsletter.find_one({'email': email}) is not None:
        flash(f"L'email {email} est déjà enregistré dans notre newsletter.", 'danger')
    else:
        from datetime import datetime
        gd.db.users_newsletter.insert_one({
            'userid': None,
            'email': email,
            'is_anonymous': True,
            'is_newsletter': True,
            'updated': None,
            'created': datetime.now()
        })
        flash(f"L'email {email} a été inclus dans notre newsletter. Vérifiez votre boîte de réception, nous vous avons envoyé un courriel de confirmation.", 'success')
    return redirect('/')


class navbar:

    @public_language.route("/education")
    @register_breadcrumb(public_language, '.fr_education', "L'éducation", 3)
    def education():
        return render_template("pages/es-education.html",
                               lang_data=find_data('education'))


class gtc_explore_navbar:

    """    
    @public_language.route("/modules")
    @register_breadcrumb(public_language, '.modules', 'Modules')
    def gtc_modules():
        return render_template("pages/es-us-modules.html")
    
    @public_language.route("/programs")
    @register_breadcrumb(public_language, '.programs', 'Programs')
    def gtc_programs():
        return render_template("pages/es-us-programs.html")

    @public_language.route("/projects")
    @register_breadcrumb(public_language, '.projects', 'Projects')
    def gtc_projects():
        return render_template("pages/es-us-projects.html",
        title="Projects Globodain is working on",
        footer_page_modified=True)

    @public_language.route("/technologies")
    @register_breadcrumb(public_language, '.technologies', 'Technologies')
    def gtc_technologies():
        return render_template("pages/es-us-technologies.html")
    
    """

    @public_language.route("/applications")
    @register_breadcrumb(public_language, '.fr_applications', 'Applications')
    def applications():
        return render_template("pages/es-applications.html",
                               lang_data=find_data('applications'),
                                header_dark_mode=True)

# ! -- S E C T I O N S -- ! #

class sections:

    # ! - APPLICATIONS - ! #

    @public_language.route("/applications/finances")
    @register_breadcrumb(public_language, '.fr_applications.fr_finances', 'Finances')
    def applications_finances():
        return render_template("pages/applications/es-finances.html",
                               lang_data=find_data('applications_finances'))

    @public_language.route("/applications/accounting")
    @register_breadcrumb(public_language, '.fr_applications.fr_accounting', 'Comptabilité')
    def applications_accounting():
        return render_template("pages/applications/es-accounting.html",
                                lang_data=find_data('applications_accounting'))

    @public_language.route("/applications/business")
    @register_breadcrumb(public_language, '.fr_applications.fr_business', 'Business Intelligence')
    def applications_business():
        return render_template("pages/applications/es-business-intelligence.html",
                                lang_data=find_data('applications_business'))

    @public_language.route("/applications/e-city")
    @register_breadcrumb(public_language, '.fr_applications.fr_city30', 'City 3.0')
    def applications_city30():
        return render_template("pages/applications/es-city30.html",
                                lang_data=find_data('applications_ecity'))

    """ # Next implementations

    @public_language.route("/applications/farming")
    @register_breadcrumb(public_language, '.applications.farming', 'Farming')
    def applications_farming():
        return render_template("pages/applications/es-us-farming.html",
        title="Boost the productivity in your crop activity with our analyzing system with algorithms")

    @public_language.route("/applications/metallurgy")
    @register_breadcrumb(public_language, '.applications.metallurgy', 'Metallurgy')
    def applications_metallurgy():
        return render_template("pages/applications/es-us-metallurgy.html")

    @public_language.route("/applications/aeronautical")
    @register_breadcrumb(public_language, '.applications.aeronautical', 'Aeronautical')
    def applications_aeronautical():
        return render_template("pages/applications/es-us-aeronautical.html")

    @public_language.route("/applications/automotive")
    @register_breadcrumb(public_language, '.applications.automotive', 'Automotive')
    def applications_automotive():
        return render_template("pages/applications/es-us-automotive.html")

    @public_language.route("/applications/hardware")
    @register_breadcrumb(public_language, '.applications.hardware', 'Hardware')
    def applications_hardware():
        return render_template("pages/applications/es-us-hardware.html")
        
    """

    # ! - SERVICES - ! #

    @public_language.route("/services")
    @register_breadcrumb(public_language, '.fr_services', 'Services')
    def services():
        return render_template("sections/services/es-services.html",
                               lang_data=find_data('services'))
    
    # ! - EDUCATION - ! #

    # EDUCATION - STUDENTS

    @public_language.route("/education/for-students", methods=["GET", "POST"])
    @register_breadcrumb(public_language, '.fr_education.fr_students', 'Pour les étudiants')
    def education_students():
        function_to_list_images = None
        gallery = random.sample(function_to_list_images, 10)

        if request.method == 'POST':
            form = request.form.get
            
            items = {
                "type": "contact",
                "email": form("email"),
                "requested": "student",
                "created": datetime.now()
            }

            if not gd.db.requests.find_one({"type": "contact", "email": items['email']}):
                # Guardamos en la base de datos
                gd.db.requests.insert_one(items)

                # Enviamos un email a team@globodain.com
                emails.send_no_reply_email(items['email'], "Un étudiant a envoyé une pétition", 
                                        "<p>Chère école :</p>Nous vous contactons de <strong>Globodain</strong>, une entreprise technologique d’Espagne, conformément à la demande de l’un de vos étudiants dans le but de <strong>discuter de la possible collaboration dans les programmes éducatifs</strong> que nous offrons pour les étudiants et les enseignants.<br>Nos programmes éducatifs, en collaboration avec des institutions gouvernementales européennes, sont entièrement financés par les plans de développement régional et de coopération économique de l’Union européenne.<br>Si cela vous intéressait, je serais ravi de pouvoir envoyer plus d’informations sur nos programmes.<br><p style='color: #004AAD;'>** Vous pouvez nous écrire si cela vous intéresse à ana.perez@globodain.com ou ruben.ayuso@globodain.com<p><br>Cordialement, <br>Rubén Ayuso<br>Directeur des programmes de <a href='https://globodain.com'>Globodain Education</a><br><b><small>Ceci est un courrier automatique envoyé par le système interne de la plateforme. Ne pas répondre à ce courrier</small>")
                
                flash('Nous prendrons contact avec votre école afin de vous proposer nos programmes éducatifs.', 'success')
            else:
                flash("Vous avez déjà soumis une demande. Restez à l'écoute", 'danger')

        return render_template("sections/education/es-students.html",
                                lang_data=find_data('for-students'),
                                gallery=gallery)

    # EDUCATION - SCHOOLS

    @public_language.route("/education/for-schools", methods=["GET", "POST"])
    @register_breadcrumb(public_language, '.fr_education.fr_schools', 'Pour les écoles')
    def education_schools():
        
        if request.method == 'POST':
            form = request.form.get
            
            items = {
                "type": "contact",
                "email": form("email"),
                "requested": "school",
                "created": datetime.now()
            }

            if not gd.db.requests.find_one({"type": "contact", "email": items['email']}):
                # Guardamos en la base de datos
                gd.db.requests.insert_one(items)

                # Enviamos un email a team@globodain.com
                emails.send_no_reply_email("admin@globodain.com", "Una escuela ha enviado una petición", 
                                        "<p>Una escuela ha enviado una petición de contacto interesándose por los programas educativos ofrecidos en la página web: <br><br>Email de contacto: <strong>{}<strong><br><br><small>Este es un correo automático enviado por el sistema interno de la plataforma. No responder a este correo</small></p>".format(items['email']))
                
                flash("Un membre de l'équipe vous contactera pour un premier entretien.", 'success')
            else:
                flash("Vous avez déjà soumis une demande. Restez à l'écoute", 'danger')

        return render_template("sections/education/es-schools.html",
                               lang_data=find_data('for-schools'))

    # EDUCATION - PROGRAMS

    @public_language.route("/education/programs")
    @register_breadcrumb(public_language, '.fr_education.fr_programs', 'Programmes éducatifs')
    def education_programs():
        return render_template("sections/education/es-programs.html",
                               lang_data=find_data('education_programs'))
    
    ## EDUCATION - PROGRAMS - MOBILITY 

    @public_language.route("/education/programs/mobility")
    @register_breadcrumb(public_language, '.fr_education.fr_programs.fr_mobility', 'Mobilité internationale')
    def education_programs_mobility():
        function_to_list_images = None
        images = random.sample(function_to_list_images, 2)
        return render_template("sections/education/programs/es-mobility.html",
                               lang_data=find_data('education_programs_mobility'),
                               images=images)
    
    @public_language.route("/education/programs/mobility/erasmus")
    @register_breadcrumb(public_language, '.fr_education.fr_programs.fr_mobility.fr_erasmus', 'Erasmus+')
    def education_programs_mobility_erasmus():
        return render_template("sections/education/programs/mobility/es-erasmus.html",
                               lang_data=find_data('education_programs_mobility_erasmus'))

    ### EDUCATION - PROGRAMS - MOBILITY - SERVICES
    """
    @public_language.route("/education/programs/mobility/services")
    @register_breadcrumb(public_language, '.fr_education.fr_programs.fr_mobility.fr_services', 'Servicios')
    def education_programs_mobility_services():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")

    @public_language.route("/education/programs/mobility/services/host-organization")
    @register_breadcrumb(public_language, '.fr_education.fr_programs.fr_mobility.fr_services.fr_host', 'Prácticas')
    def education_programs_mobility_services_host():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")

    @public_language.route("/education/programs/mobility/services/accommodation")
    @register_breadcrumb(public_language, '.fr_education.fr_programs.fr_mobility.fr_services.fr_accommodation', 'Alojamiento')
    def education_programs_mobility_services_accommodation():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")
    
    @public_language.route("/education/programs/mobility/services/trips")
    @register_breadcrumb(public_language, '.fr_education.fr_programs.fr_mobility.fr_services.fr_trips', 'Viajes')
    def education_programs_mobility_services_trips():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")
    
    @public_language.route("/education/programs/mobility/services/experiences")
    @register_breadcrumb(public_language, '.fr_education.fr_programs.fr_mobility.fr_services.fr_experiences', 'Experiencias')
    def education_programs_mobility_services_experiences():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")

    
    ### EDUCATION - AREAS OF EDUCATION

    @public_language.route("/education/areas-of-education")
    @register_breadcrumb(public_language, '.fr_education.fr_areas', 'Áreas de enseñanza')
    def education_areas():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")

    @public_language.route("/education/areas-of-education/programming")
    @register_breadcrumb(public_language, '.fr_education.fr_areas.fr_programming', 'Programación')
    def education_areas_programming():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")

    @public_language.route("/education/areas-of-education/marketing")
    @register_breadcrumb(public_language, '.fr_education.fr_areas.fr_marketing', 'Marketing')
    def education_areas_marketing():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")

    @public_language.route("/education/areas-of-education/ui-ux")
    @register_breadcrumb(public_language, '.fr_education.fr_areas.fr_uiux', 'Interfaz de usuarios')
    def education_areas_uiux():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('index'),
                               title="Educational Partnership")
    """

    # EDUCATION - PARTNERSHIP

    @public_language.route("/education/partnership")
    @register_breadcrumb(public_language, '.fr_education.fr_partnership', 'Je veux être partenaire')
    def education_partnership():
        return render_template("sections/education/es-partnership.html", 
                               lang_data=find_data('education_partnership'))

    @public_language.route("/education/partnership/request-prices", methods=['GET', 'POST'])
    @register_breadcrumb(public_language, '.fr_education.fr_partnership.fr_request_prices', 'Demande de prix')
    def education_partnership_request_prices():
        if request.method == 'POST':
            form = request.form.get
            
            items = {
                "type": "prices",
                "fullname": form('fullname'),
                "email": form("email"),
                "business_name": form("business_name"),
                "business_title": form("business_title"),
                "created": datetime.now()
            }

            if not gd.db.requests.find_one({"type": "prices", "email": items['email']}):
                # Guardamos en la base de datos
                gd.db.requests.insert_one(items)

                # Enviamos un email a team@globodain.com
                emails.send_no_reply_email("admin@globodain.com", "Un usuario ha solicitado precios", 
                                        "<p>Nombre completo: <strong>{}</strong><br>Email: <strong>{}</strong><br>Empresa: <strong>{}</strong><br>Cargo: <strong>{}</strong></p>".format(items['fullname'], items['email'], items['business_name'], items['business_title']))
                
                flash("Une demande a été envoyée à l'équipe", 'success')
            else:
                flash("Vous avez déjà demandé des prix auparavant. Restez à l'écoute", 'danger')

            return redirect(request.referrer)

        return render_template("sections/education/es-partnership-prices.html", 
                               lang_data=find_data('education_partnership_prices'))

# ! -- E N D   S E C T I O N S -- ! #

class pages:
    @public_language.route("/privacy")
    @register_breadcrumb(public_language, '.fr_privacy', 'Vie privée')
    def privacy():
        return render_template("policies/es-policy-privacy.html",
                               lang_data=find_data('privacy'))

    @public_language.route("/terms")
    @register_breadcrumb(public_language, '.fr_terms', "Conditions générales d'utilisation")
    def terms():
        return render_template("policies/es-policy-terms.html",
                               lang_data=find_data('terms'))

    @public_language.route("/cookies")
    @register_breadcrumb(public_language, '.fr_cookies', 'Cookies')
    def cookies():
        return render_template("policies/es-policy-cookies.html",
                               lang_data=find_data('cookies'))

    @public_language.route("/request", methods=['GET', 'POST'])
    @register_breadcrumb(public_language, '.fr_request', 'Demande de services')
    def request_services():
        if request.method == 'POST':
            form = request.form.get

            # Generate unique id for peticion
            import uuid
            request_id = "{}".format(str(uuid.uuid4().hex))[0:16]

            # Get form information
            fullname=form("form_contact_fullname")
            email=form("form_contact_email")
            phone=form("form_contact_phone")
            company=form("form_contact_company")
            position=form("form_contact_position")
            message=form("form_contact_message")

            if gd.db.contact_blacklist.find_one({"fullname": fullname}) or gd.db.contact_blacklist.find_one({"email": email}):
                return redirect(url_for("public.prevent"))
            else:
                if gd.db.users_contact_request.find_one({"email": email}):
                    flash(f"Vous avez déjà fait une demande. Restez à l'écoute", 'danger')
                else:
                    from datetime import datetime   
                    gd.db.users_contact_request.insert_one({
                        "request_id": request_id,
                        "fullname": fullname,
                        "email": email,
                        "phone": phone,
                        "company": company,
                        "position": position,
                        "message": message,
                        "privacy_accept": True,
                        "created": datetime.now()
                    })

                    gtc_email="admin@globodain.com"
                    subject="GLOBODAIN: Un nuevo usuario ha enviado una petición de contacto"
                    html=render_template('emails/admin-notification-user-contact-request.html',
                    fullname=fullname,email=email,phone=phone,position=position,message=message)
                    emails.send_no_reply_email(gtc_email,subject,html)
                    
                    next_page = request.args.get('next', None)
                    if not next_page or url_parse(next_page).netloc != '':
                        flash(f"Votre demande a bien été enregistrée, un membre de l'équipe vous contactera prochainement.", 'success')
                        next_page = url_for('public_es.request_services')
                    return redirect(next_page) # Si todo correcto, redirigimos al index de colaborador

        return render_template("pages/es-request-services.html",
                               lang_data=find_data('request-services'))

    @public_language.route("/sitemap")
    @public_language.route("/sitemap/")
    @register_breadcrumb(public_language, '.fr_sitemap', 'Sitemap')
    def sitemap():

        # Generar la estructura del sitemap
        sitemap_structure = {}

        for rule in app.url_map.iter_rules():
            if str(rule).startswith("/"+session['lang']):
                exclude_dirs = ["/upload","/{}/sitemap".format(session['lang']),"/{}/newsletter".format(session['lang'])]
                if any(str(rule).startswith(dir) for dir in exclude_dirs):
                    pass
                else:
                    if "GET" in rule.methods and len(rule.arguments) == 0:
                        # Extraer la información del breadcrumb de la ruta
                        breadcrumb = list(filter(None, rule.endpoint.split('.')))
                        if len(breadcrumb) > 1:
                            area = breadcrumb[-1]
                            label = breadcrumb[-1]

                            if len(breadcrumb[-1].split('_')) > 1:
                                split = breadcrumb[-1].split('_')
                                area = split[0]
                                label = breadcrumb[-1].replace('_','-')
                                

                            if area not in sitemap_structure:
                                sitemap_structure[area] = []
                            
                            sitemap_structure[area].append({
                                "name": label,
                                "route": str(rule)
                            })
                                
        return render_template("sitemap.html", sitemap_structure=sitemap_structure,
                                lang_data=find_data('index'))