from django.shortcuts import render
from django.views import View
from facturacion.models import DocumentoCabecera, DocumentoDetalle

# Create your views here.
class ReporteFacturaPage(View):

	def get(self, request, *args, **kwargs):
		facturas = DocumentoCabecera.objects.all()
		context = {
			'title': '',
			'description': '',
			'facturas': facturas
		}
		return render(request,"facturas.html", context)