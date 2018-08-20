from mainApp.models import Action, User
from articlesApp.models import Article
from django.db import models


class Loan(Action):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, related_name="admin_art_prestador", on_delete=models.CASCADE, default=None,
                              null=True)