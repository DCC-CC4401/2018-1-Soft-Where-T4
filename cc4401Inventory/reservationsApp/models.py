from mainApp.models import Action, User
from spacesApp.models import Space
from django.db import models


class Reservation(Action):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, related_name="admin_spa_prestador", on_delete=models.CASCADE, default=None)