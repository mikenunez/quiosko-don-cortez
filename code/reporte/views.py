from django.db.models import FloatField, Sum, F
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from facturacion.models import DocumentoCabecera, DocumentoDetalle

# Create your views here.
class ReporteFacturaPage(ListView):
	model = DocumentoCabecera
	template_name = "facturas.html"
	queryset = DocumentoCabecera.objects.annotate(Sum(F('documentodetalle__subtotal')))