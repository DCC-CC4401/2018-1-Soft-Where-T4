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
from reservationsApp.models import Reservation
from datetime import datetime, timezone, timedelta, date, time
Reservation.objects.all().delete()

tz = timezone(-timedelta(hours=-4))
d1=date(2018,5,10)
d2=date(2018,5,15)
d3=date(2018,6,1)
d4=date(2018,6,2)
d5=date(2018,6,3)
d6=date(2018,6,4)
h1=time(11,00,tzinfo=tz)
h2=time(12,00,tzinfo=tz)
h3=time(13,00,tzinfo=tz)
h4=time(14,30,tzinfo=tz)
t1=datetime.combine(d1,h1)
t12=datetime.combine(d1,h2)
t13=datetime.combine(d1,h3)
t14=datetime.combine(d1,h4)
t2=datetime.combine(d2,h1)
t22=datetime.combine(d2,h2)
t23=datetime.combine(d2,h3)
t24=datetime.combine(d2,h4)
t3=datetime.combine(d3,h1)
t32=datetime.combine(d3,h2)
t33=datetime.combine(d3,h3)
t34=datetime.combine(d3,h4)
t4=datetime.combine(d4,h1)
t42=datetime.combine(d4,h2)
t43=datetime.combine(d4,h3)
t44=datetime.combine(d4,h4)
t5=datetime.combine(d5,h1)
t52=datetime.combine(d5,h2)
t53=datetime.combine(d5,h3)
t54=datetime.combine(d5, h4)
t6=datetime.combine(d6, h1)
t62=datetime.combine(d6, h2)
t63=datetime.combine(d6, h3)
t64=datetime.combine(d6, h4)

r1 = Reservation(starting_date_time=t1,ending_date_time=t2,state='P',user=user, prestado=False, admin=admin, space=b01)
r1.save()
r2 = Reservation(starting_date_time=t3,ending_date_time=t4,state='P',user=user, prestado=False, admin=admin, space=b02)
r2.save()
