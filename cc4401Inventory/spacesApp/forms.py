from django.forms import ModelForm
from spacesApp.models import Space

class SpaceForm(ModelForm):
    class Meta:
        model = Space
        fields = ['name', 'description', 'image', 'state']