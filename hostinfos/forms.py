from django import forms
from .models import Host,PowerInfo

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['host_name', 'outlet', 'province', 'host_type', 'date_of_live']




class PowerInfoForm(forms.ModelForm):
    class Meta:
        model = PowerInfo
        fields = '__all__'  # or list fields explicitly