from django import forms
from .models import Cliente, Producto, TablaCatalogo, DocumentoCabecera


class FormCliente(forms.Form):
	ruc 		= forms.CharField(max_length=15, label='Cédula / RUC')
	firstname 	= forms.CharField(max_length=50, label='Nombre')
	lastname 	= forms.CharField(max_length=50, label='Apellido')
	phone 		= forms.CharField(max_length=20, label='Teléfono')
	email 		= forms.EmailField(max_length=100,)


class FormDocCabecera(forms.ModelForm):
	class Meta:
		model = DocumentoCabecera
		fields = ['docid', 'doctype', 'payment', 'iva',]
		widgets = {
			'iva': forms.TextInput(attrs={'readonly':'readonly'}),
		}


class FormDocDetalle(forms.Form):
	cantidad 	= forms.IntegerField(required=True, widget=forms.TextInput())
	producto 	= forms.ModelChoiceField(queryset=Producto.objects.all(),)
	precio_uni 	= forms.DecimalField(decimal_places=2, max_digits=6, label='Precio Unit.', widget=forms.TextInput(), disabled=False)
	iva			= forms.ModelChoiceField(queryset=TablaCatalogo.objects.all(), to_field_name="code", label='IVA %', required=True, initial='010100')
	descuento 	= forms.DecimalField(initial=0.00, decimal_places=2, max_digits=6, widget=forms.TextInput())
	subtotal	= forms.DecimalField(decimal_places=2, max_digits=6, disabled=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))