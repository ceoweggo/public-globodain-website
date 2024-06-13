from flask import request,redirect,session,url_for,render_template
from . import public_

from app import app

@public_.before_request
def language():
    if not 'lang' in session:
<<<<<<< HEAD
        session['lang'] = 'es'
=======
        session['lang'] = 'en'
>>>>>>> 353c311599c35e239451c55a2f3251d1f6eb64f8
    session['lang_code'] = session['lang']

@public_.route("/", methods=['GET', 'POST'])
def index():
    return redirect(url_for("global.index"))

@public_.route("/prevent", methods=['GET'])
@public_.route("/prevent/", methods=['GET'])
def prevent():
    # Redirijo al idioma deseado
    return render_template("errors/prevent.html")

@public_.route("/en-us/services", methods=['GET'])
@public_.route("/en-us", methods=['GET'])
@public_.route("/en-us/", methods=['GET'])
def en_redirect():
    session.clear()
    session['lang'] = 'en'
    # Redirijo al idioma deseado
    return redirect(url_for('global.index'))

@public_.route("/es-es/services", methods=['GET'])
@public_.route("/es-es", methods=['GET'])
@public_.route("/es-es/", methods=['GET'])
def es_redirect():
    session.clear()
    session['lang'] = 'es'
    # Redirijo al idioma deseado
    return redirect(url_for('global.index'))    

@public_.route('/change-language/<language>', methods=['GET'])
def change_language(language):
    session['lang_code'] = language
    
    last_url = request.referrer
    last_url_splitted = last_url.split('/')
    
    # Encuentra la posición del código de idioma en la URL
    for i, path in enumerate(last_url_splitted):
        if len(path) == 2:  # Asume que el código del idioma tiene 2 letras
            last_url_splitted[i] = language
            break
    
    # Reconstruye la URL
    url_to_redirect = '/'.join(last_url_splitted)
    
    return redirect(url_to_redirect)


@public_.route("/sitemap/")
@public_.route("/sitemap.xml")
def xml_sitemap():
    """
        Route to dynamically generate a sitemap of your website/application.
        lastmod and priority tags omitted on static pages.
        lastmod included on dynamic content such as blog posts.
    """
    from flask import make_response, request, render_template
    from urllib.parse import urlparse

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # Static routes with static content
    static_urls = list()
    for rule in app.url_map.iter_rules():
        exclude_dirs = ["/auth", "/sitemap", "/<lang_code>", "/static", "/admin", "/change-language"]
        if any(str(rule).startswith(dir) for dir in exclude_dirs):
            pass
        else:
            import datetime
            url = {
                "loc": f"{host_base}{str(rule)}",
                "lastmod": (datetime.datetime.now()-datetime.timedelta(7)).strftime('%Y-%m-%d'),
                "changefreq": "weekly",
                "priority": 1.0,
            }
            static_urls.append(url)

    # Dynamic routes with dynamic content
    dynamic_urls = list()

    xml_sitemap = render_template("/sitemap.xml", static_urls=static_urls, dynamic_urls=dynamic_urls, host_base=host_base) # dynamic_urls=dynamic_urls
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response



class Errors:

    @public_.app_errorhandler(400)
    def page_refresh(e):
        return render_template('errors/400.html'), 400

    @public_.app_errorhandler(401)
    def page_need_arguments(e):
        return render_template('errors/401.html', title="Se ha producido un error al cargar la función. Vuelva a intentarlo"), 401

    @public_.app_errorhandler(403)
    def page_not_access(e):
        return render_template('errors/403.html', title="¡No tienes autorización para acceder!"), 403
    
    @public_.app_errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html', 
                               title="Página no encontrada"), 404
    
    @public_.app_errorhandler(406)
    def page_only_users_except_autor(e):
        return render_template('errors/406.html'), 406
