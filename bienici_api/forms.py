from django import forms
from django.core.validators import RegexValidator

class QueryForm(forms.Form):
    city = forms.CharField(max_length=100, required=False)
    dept_code = forms.CharField(max_length=2, required=False)
    zip_code = forms.CharField(max_length=5, required=False)

class AddUrlDataForm(forms.Form):
    url = forms.CharField(validators=[RegexValidator(regex='^https://www.bienici.com/annonce/vente/', message='Enter a valid URL in the form of: https://www.bienici.com/annonce/vente/xxx')]) 