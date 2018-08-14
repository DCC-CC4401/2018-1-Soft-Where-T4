from mainApp.models import Action
from spacesApp.models import Space
from django.db import models


class Reservation(Action):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)

"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Reservation(Action):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
"""