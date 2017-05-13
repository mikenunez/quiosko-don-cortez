import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import FloatField, Sum, F
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.utils.timezone import datetime
from django.views import View

from facturacion.models import DocumentoCabecera, DocumentoDetalle
from .forms import FormReporteDiario

from xhtml2pdf import pisa

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
		qs = DocumentoCabecera.objects.filter(created__date=self.fecha).annotate(
			total1=Sum(F('documentodetalle__subtotal'))
			).annotate(
			total2=F('iva')+Sum(F('documentodetalle__subtotal'))
			)
		context = {
			'title': '',
			'description': '',
			'form': form,
			'facturas': qs
		}
		return render(request,"reporte_diario.html",context)
		

class ReporteDiario2PDF(LoginRequiredMixin, View):
	login_url 	= '/login'
	fecha 		= datetime.today()

	def get(self, request, *args, **kwargs):
	# Prepare context
		if request.GET.get('fecha'):
			self.fecha = request.GET.get('fecha')
		qs = DocumentoCabecera.objects.filter(created__date=self.fecha).annotate(
			total1=Sum(F('documentodetalle__subtotal'))
			).annotate(
			total2=F('iva')+Sum(F('documentodetalle__subtotal'))
			)
		context = {
			'title': '',
			'description': '',
			'fecha': self.fecha,
			'user': request.user,
			'facturas': qs
		}
		# Render html content through html template with context
		template = get_template('reportediario2pdf.html')
		html = template.render(context)

		# Write PDF to file
		if not os.path.exists(settings.MEDIA_ROOT):
			os.makedirs(settings.MEDIA_ROOT)
		with open(os.path.join(settings.MEDIA_ROOT, 'reporte.pdf'), "w+b") as f:
		# f = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
			pisaStatus = pisa.CreatePDF(html, dest=f)

			# Return PDF document through a Django HTTP response
			f.seek(0) #Set pointer at the beginning to read "goto() canvas()"
			pdf = f.read()
			f.close()            # Don't forget to close the file handle
		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Reporte_%s.pdf" %(self.fecha)
		content = "inline; filename='%s'" %(filename)
		download = request.GET.get("download")
		if download:
			content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response
