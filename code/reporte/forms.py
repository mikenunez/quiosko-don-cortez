from django import forms
from django.utils.timezone import datetime

from facturacion.models import  DocumentoCabecera

class FormReporteDiario(forms.Form):
	fecha = forms.DateField(initial=datetime.today())
	