'''
Comando Para correr el Script: python manage.py shell < populateDatabase.py
'''

# users
## admin
# TODO agregar usuarios admin

## natural users
# TODO agregar usuarios naturales

# articles
# TODO agregar imagenes a los articulos (no se cómo hacerlo)
from articlesApp.models import Article
Article.objects.all().delete()

silla = Article(name = 'Silla CEC', description = 'La silla que nos pelamos del CEC', state = 'D')
silla.save()
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

# reservations
# TODO agregar reservas