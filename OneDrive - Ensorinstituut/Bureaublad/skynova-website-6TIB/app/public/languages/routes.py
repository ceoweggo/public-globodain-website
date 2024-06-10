from flask import session,g,render_template,request,redirect,url_for
from . import public_global
from app import app

@public_global.url_defaults
def add_language_code(endpoint, values):
    values['lang_code'] = str(session['lang'] if 'lang' in session else 'en')[0:2]
    if 'lang_code' in values or not g.lang_code:
        return
    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
        values['lang_code'] = g.lang_code

@public_global.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code', None)

from flask_breadcrumbs import default_breadcrumb_root,register_breadcrumb
default_breadcrumb_root(public_global, '.')

@public_global.route("/", methods=['GET'])
@register_breadcrumb(public_global, '.', 'Globodain')
def index():
    # Redirijo a global de idiomas
    return redirect(url_for('global.index'))

@public_global.route("/error", methods=['GET'])
@public_global.route("/error/", methods=['GET'])
@register_breadcrumb(public_global, '.error', 'Error')
def error():
    # Redirijo al idioma deseado
    return render_template("errors/404.html")

@public_global.route("/softcamp", methods=['GET'], strict_slashes=False)
@register_breadcrumb(public_global, '.softcamp', 'SoftCamp')
def softcamp():
    lang = request.args.get('lang')
    if lang not in ["es", "en", "it", "de", "fr"]:
        lang = "en"
    url = "https://softcamp.eu/{}/".format(lang)
    return redirect(url)

@app.route("/<lang_code>/sitemap")
@app.route("/<lang_code>/sitemap.xml")
def xml_sitemap(lang_code):
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
            if lang_code in str(rule):
                if "GET" in rule.methods and len(rule.arguments) == 0:
                    url = {
                        "loc": f"{host_base}{str(rule)}"
                    }
                    static_urls.append(url)

    """# Dynamic routes with dynamic content
    dynamic_urls = list()
    blog_posts = Post.objects(published=True)
    for post in blog_posts:
        url = {
            "loc": f"{host_base}/blog/{post.category.name}/{post.url}",
            "lastmod": post.date_published.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        dynamic_urls.append(url)"""

    xml_sitemap = render_template("/sitemap.xml", static_urls=static_urls, host_base=host_base) # dynamic_urls=dynamic_urls
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response