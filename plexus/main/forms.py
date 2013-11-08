from django.forms import ModelForm
from .models import Alias


class AliasForm(ModelForm):
    class Meta:
        model = Alias
        exclude = ['ip_address', ]
