from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.forms import formset_factory

from .models import Cliente, Producto, DocumentoCabecera
from .forms import FormDocCabecera, FormDocDetalle, FormCliente


# Create your views here.
class FacturacionPage(View):
	DocDetFormSet 	= formset_factory(FormDocDetalle, extra=1)
	DocNumber		= DocumentoCabecera.objects.last()
	if (DocNumber):
		DocLast = split('-', DocNumber.doc_id)
		DocLast = int(DocLast[2] + 1)
		DocLast = str(DocLast).zfill(9)
	else:
		DocLast	= '1'.zfill(9)
	DocLast			= "001-001-" + DocLast
	def get(self, request, *args, **kwargs):
		formCliente	= FormCliente()
		formDocCab 	= FormDocCabecera(initial={ 'doc_id': self.DocLast })
		formDocDet 	= self.DocDetFormSet
		context = {
			'title': '',
			'description': '',
			'formCliente': formCliente,
			'formDocCab': formDocCab,
			'formDocDet': formDocDet
		}
		return render(request,"index.html",context)

	def post(self, request, *args, **kwargs):
		formCliente 	= FormCliente(request.POST)
		formDocCab 		= FormDocCabecera(request.POST)
		formDocDet 		= self.DocDetFormSet(request.POST)
		if (request.POST.get('cli_val')):
			qs_cliente = Cliente.objects.filter(ruc=request.POST.get('cli_val')).first()
			client = {
				'ruc': qs_cliente.ruc,
				'nombre': qs_cliente.firstname,
				'apellido': qs_cliente.lastname,
				'email': qs_cliente.email,
				'phone': qs_cliente.phone
			}
			return JsonResponse(client)
		else:
			cliente_id = ""
			if formCliente.is_valid():
				obj, create = Cliente.objects.update_or_create(
					ruc = formCliente.cleaned_data.get('ruc'),
					defaults={
						'firstname': formCliente.cleaned_data.get('firstname'),
						'lastname': formCliente.cleaned_data.get('lastname'),
						'phone': formCliente.cleaned_data.get('phone'),
						'email': formCliente.cleaned_data.get('email'),
						}
					)
				if create:
					print ("nuevo-- ", create)
				else:
					print ("updated-- ", obj)

				# existe = 'Cliente.objects.filter(ruc=instance.ruc).exists()'
				# if (existe):
				# 	print("client exist: ")
				# else:
				# 	print("new client: " )
				# 	# instance.save()

			context = {
				'title': '',
				'description': '',
				'formCliente': formCliente,
				'formDocCab': formDocCab,
				'formDocDet': formDocDet
			}
			return render(request,"index.html", context)