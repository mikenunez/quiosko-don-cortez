from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import FloatField, Sum, F
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import datetime
from django.views import View

from quiosko.utils import render_to_pdf
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
		

class ReporteDiario2PDF(View):
	fecha 		= datetime.today()

	def get(self, request, *args, **kwargs):
		if request.GET.get('fecha'):
			self.fecha = request.GET.get('fecha')
		qs = DocumentoCabecera.objects.filter(created__date=self.fecha).annotate(Sum(F('documentodetalle__subtotal')))
		context = {
			'title': '',
			'description': '',
			'fecha': self.fecha,
			'user': request.user,
			'facturas': qs
		}
		pdf = render_to_pdf('reportediario2pdf.html', context)
		# return render(request,"reportediario2pdf.html",context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Reporte_%s.pdf" %(self.fecha)
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not found")