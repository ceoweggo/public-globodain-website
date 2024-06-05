"""
<!-- -| 
  
  * GLOBODAIN is a registered trademark in Spain as Globodain Technology Corporation, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->

--------------------------- FUNCIONAMIENTO DEL SISTEMA --------------------------

1. Creamos una tabla en DB que al crear un post en el panel de administración, guarde:
    - El texto que aparecerá en el anuncio
    - La URL de la página de salida
    - La localización del anuncio.
    - El idioma del anuncio

2. Los datos son guardados en la base de datos con una ID la cual se llamará posteriormente por 
    las sentencias de las funciones, asignando el código correspondiente la anuncio

3. El código pasa cómo variable a la sentencia que a su vez pasará a otra variable dentro de ésta para 
    hacer una consulta al documento correspondiente, buscando el lenguaje y el código indicado. 
    Si el código no aparece, automáticamente el anuncio no aparece (se determina cómo None)

4. La consulta encuentra el anuncio, así que retorna los valores de 'announcement_text' y 'url',
    asignándoles un valor a las variables definidas

Esquema:

Admin --> DB --> Sentencia --> DB --> Devuelve valores
"""

from flask import url_for

# AUN NO AUTOMATIZADO
def home_announcement(code,lang):
    """ from config.db import weggo
        if not weggo.db.announcements.find():
            #Create the announcements document
            weggo.db.announcements.insert(
                
            )"""

    if code == 0 or None:
        # Deactivate announcement in home
        announcement_text = None
        url = None

    if code == 1:
        if lang == 'es-es':
            announcement_text = "Comienza a explorar los servicios de GTC Finances con la cuenta gratuita de Estudiante. Créala ahora!"
            url = url_for("public_es_es.education_landing_pages", lang=lang,section='education', page='students')
        elif lang == 'en-us':
            announcement_text = "Start to explore the GTC finances services to students creating a free account."
            url = url_for("public_en_us.education_landing_pages", lang=lang, section='education', page='students')
            
    return announcement_text, url
