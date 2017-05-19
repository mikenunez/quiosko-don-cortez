from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.forms import formset_factory

from .models import Cliente, Producto, DocumentoCabecera, DocumentoDetalle
from .forms import FormDocCabecera, FormDocDetalle, FormCliente


# Create your views here.
class FacturacionPage(LoginRequiredMixin, View):
	login_url = '/login'
	DocDetFormSet 	= formset_factory(FormDocDetalle, extra=10)
	try:
		DocNumber	= DocumentoCabecera.objects.last()
		DocLast 	= DocNumber.docid.split('-')
		DocLast 	= int(DocLast[2]) + 1
		DocLast 	= str(DocLast).zfill(9)
		DocLast		= "001-001-" + DocLast
		
	except:
		DocLast	= '1'.zfill(9)
		DocLast	= "001-001-" + DocLast


	def clientePopulate(self, *args, **kwargs):
		qs_cliente = Cliente.objects.filter(ruc=kwargs['cliente']).first()
		if qs_cliente:
			cliente = {
				'ruc': qs_cliente.ruc,
				'nombre': qs_cliente.firstname,
				'apellido': qs_cliente.lastname,
				'email': qs_cliente.email,
				'phone': qs_cliente.phone
			}
		else:
			cliente= {}
		return cliente

	def precioPopulate(self, *args, **kwargs):
		qs_precio = Producto.objects.filter(pk=kwargs['producto']).first()
		precio = {
			'precio': qs_precio.sale_price,
		}
		return precio

	def clienteNuevo(self, *args, **kwargs):
		# print (kwargs['formCliente'].cleaned_data.get('ruc'))
		obj, create = Cliente.objects.update_or_create(
			ruc = kwargs['formCliente'].cleaned_data.get('ruc'),
			defaults={
				'firstname': kwargs['formCliente'].cleaned_data.get('firstname'),
				'lastname': kwargs['formCliente'].cleaned_data.get('lastname'),
				'phone': kwargs['formCliente'].cleaned_data.get('phone'),
				'email': kwargs['formCliente'].cleaned_data.get('email'),
				}
			)
		if create:
			print ("nuevo-- ", create)
		else:
			print ("updated-- ", obj)
		return obj

		
	def saveDetalles(self, *args, **kwargs):
		detalle = DocumentoDetalle(
			documento=kwargs['documento'],
			producto=kwargs['formDet'].cleaned_data.get('producto'),
			cantidad=kwargs['formDet'].cleaned_data.get('cantidad'),
			tablacatalogo=kwargs['formDet'].cleaned_data.get('iva'),
			descuento=kwargs['formDet'].cleaned_data.get('descuento'),
			subtotal=kwargs['formDet'].cleaned_data.get('subtotal'),
			)
		return detalle


	def get(self, request, *args, **kwargs):
		formCliente	= FormCliente()
		formDocCab 	= FormDocCabecera(initial={ 'docid': self.DocLast })
		formSetDocDet 	= self.DocDetFormSet
		context = {
			'title': '',
			'description': '',
			'formCliente': formCliente,
			'formDocCab': formDocCab,
			'formSetDocDet': formSetDocDet
		}
		return render(request,"facturacion.html",context)


	def post(self, request, *args, **kwargs):
		formCliente 	= FormCliente(request.POST)
		formDocCab 		= FormDocCabecera(request.POST)
		formSetDocDet 	= self.DocDetFormSet(request.POST)
		if (request.POST.get('cli_val')):
			cliente = self.clientePopulate(cliente=request.POST.get('cli_val'))
			return JsonResponse(cliente)
		elif (request.POST.get('prod_pk')):
			precio = self.precioPopulate(producto=request.POST.get('prod_pk'))
			return JsonResponse(precio)
		else:
			if formCliente.is_valid():
				cliente = self.clienteNuevo(formCliente=formCliente)
			if formDocCab.is_valid():
				doc_instance = formDocCab.save(commit=False)
				doc_instance.cliente = cliente
				doc_instance.seller = request.user
				doc_instance.save()
				det = 0
				for formDocDet in formSetDocDet:
					if formDocDet.is_valid():
						if (formDocDet.cleaned_data.get('cantidad') or formDocDet.cleaned_data.get('subtotal')):
							detalle = self.saveDetalles(documento=doc_instance, formDet=formDocDet)
							detalle.save()
							det = det + 1
				if (det == 0):
					doc_instance.delete()

			context = {
				'title': '',
				'description': '',
				'formCliente': formCliente,
				'formDocCab': formDocCab,
				'formSetDocDet': formSetDocDet
			}
			return render(request,"facturacion.html", context)

	