from django.shortcuts import render
from django.views import View
# Create your views here.
class ReporteFacturaPage(View):

	def get(self, request, *args, **kwargs):
		context = {
			'title': '',
			'description': ''
		}
		return render(request,"reporte-facturas.html", context)