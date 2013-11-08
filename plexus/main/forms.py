from django.forms import ModelForm
from .models import Alias, Contact


class AliasForm(ModelForm):
    class Meta:
        model = Alias
        exclude = ['ip_address', ]


class ContactForm(ModelForm):
    class Meta:
        model = Contact
