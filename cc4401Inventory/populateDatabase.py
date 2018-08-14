'''
Comando Para correr el Script: python manage.py shell < populateDatabase.py
'''

# users
## admin
# TODO agregar usuarios admin
from django.contrib.auth import get_user_model
admin = get_user_model().objects.create_user(email="miniadmin@cei.cl", password="administrador")
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
# TODO agregar imagenes a los articulos (no se cómo hacerlo)
from articlesApp.models import Article
Article.objects.all().delete()

silla = Article(name = 'Silla CEC', description = 'La silla que nos pelamos del CEC', state = 'D')
silla.save()
metal = Article(name = 'Silla sala', description = 'La silla que no nos pelamos del CEC', state = 'R')
metal.save()
madera = Article(name = 'Mesa', description = 'Una mesa, pero no de plástico', state = 'L')
madera.save()
mesa = Article(name = 'Mesa plástico', description = 'Una mesa, pero de plástico', state = 'P')
mesa.save()

# spaces
# TODO agregar imagenes a los espacios (no se cómo hacerlo)
from spacesApp.models import Space
Space.objects.all().delete()

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