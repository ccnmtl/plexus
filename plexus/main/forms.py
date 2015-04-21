from django.forms import ModelForm
from .models import Alias, Contact, Server, Application


class AliasForm(ModelForm):
    class Meta:
        model = Alias
        exclude = ['ip_address', ]


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class ServerForm(ModelForm):
    class Meta:
        model = Server
        fields = '__all__'


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = '__all__'
