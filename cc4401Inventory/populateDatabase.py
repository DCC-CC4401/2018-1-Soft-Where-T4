'''
Comando Para correr el Script: python manage.py shell < populateDatabase.py
'''

# users
## admin
# TODO agregar usuarios admin
from django.contrib.auth import get_user_model
get_user_model().objects.all().delete()
admin = get_user_model().objects.create_superuser(email="admin@cei.cl", password="administrador")
admin.is_staff = True
admin.first_name = "Administrador"
admin.last_name = "McAdmin"
admin.rut = "12.345.678-9"
admin.save()

## natural users
# TODO agregar usuarios naturales
user = get_user_model().objects.create_user(email="usuario@cei.cl", password="usuario")
user.first_name = "Usuario"
user.last_name = "McUser"
user.rut = "01.234.567-8"
user.save()

# articles
from articlesApp.models import Article
Article.objects.all().delete()

silla = Article(name='Silla CEC', description='La silla que nos pelamos del CEC', state='D',
                image='static/img/items/silla_cec.jpg')
silla.save()
metal = Article(name='Silla sala', description='La silla que no nos pelamos del CEC', state='R',
                image='static/img/items/silla_sala.jpg')
metal.save()
madera = Article(name='Mesa', description='Una mesa, pero no de plástico', state='L', image='static/img/items/mesa.jpg')
madera.save()
mesa = Article(name='Mesa plástico', description='Una mesa, pero de plástico', state='P',
               image='static/img/items/mesa_plastico.jpg')
mesa.save()

# spaces
# TODO agregar imagenes a los espacios (no se cómo hacerlo)
from spacesApp.models import Space
Space.objects.all().delete()

quincho = Space(name = 'quincho', description = 'Best Quincho', state = 'P', image='static/img/items/quincho.jpg')
quincho.save()
b01 = Space(name = 'B01', description = 'De las mejores salas para mechones que hay', state='P')
b01.save()
b02 = Space(name = 'B02', description = 'De las mejores salas para mechones que hay', state='P')
b02.save()
b03 = Space(name = 'B03', description = 'De las mejores salas para mechones que hay', state='R')
b03.save()
b04 = Space(name = 'B04', description = 'De las mejores salas para mechones que hay', state='D')
b04.save()
# reservations
# TODO agregar reservas