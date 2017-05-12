from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import FloatField, Sum, F
from django.shortcuts import render
from django.utils.timezone import datetime
from django.views import View

from facturacion.models import DocumentoCabecera, DocumentoDetalle
from .forms import FormReporteDiario

# Create your views here.
class ReporteDiarioPage(LoginRequiredMixin, View):
	login_url 	= '/login'
	fecha 		= datetime.today()

	def get(self, request, *args, **kwargs):
		form	= FormReporteDiario()
		qs = DocumentoCabecera.objects.filter(created__date=self.fecha).annotate(Sum(F('documentodetalle__subtotal')))
		context = {
			'title': '',
			'description': '',
			'form': form,
			'facturas': qs
		}
		return render(request,"reporte_diario.html",context)

	def post(self, request, *args, **kwargs):
		form	= FormReporteDiario(request.POST)
		if form.is_valid():
			self.fecha = form.cleaned_data.get('fecha')
		qs = DocumentoCabecera.objects.filter(created__date=self.fecha).annotate(Sum(F('documentodetalle__subtotal')))
		context = {
			'title': '',
			'description': '',
			'form': form,
			'facturas': qs
		}
		return render(request,"reporte_diario.html",context)
		