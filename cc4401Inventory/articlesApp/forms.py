from django.forms import ModelForm
from articlesApp.models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'description', 'image', 'state']