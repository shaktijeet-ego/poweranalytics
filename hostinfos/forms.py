from django import forms
from .models import Host

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['host_name', 'outlet', 'province', 'host_type', 'date_of_live']