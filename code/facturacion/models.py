from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.encoding import python_2_unicode_compatible # only if you need to support Python 2
# Create your models here.

@python_2_unicode_compatible  # only if you need to support Python 2
class Cliente(models.Model):
	ruc 		= models.CharField(max_length=15, null=False, blank=False, unique=True)
	email 		= models.EmailField(max_length=200, null=False, blank=False)
	firstname 	= models.CharField(max_length= 100, null=False, blank=False)
	lastname 	= models.CharField(max_length= 100, null=True, blank=True)
	phone		= models.CharField(max_length= 20, null=True, blank=True)
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.ruc)

	def __str__(self):
		return str(self.ruc)


@python_2_unicode_compatible  # only if you need to support Python 2
class TablaCatalogo(models.Model):
	code 		= models.CharField(max_length= 6, null=False, blank=False, unique=True)
	description	= models.CharField(max_length= 50, null=False, blank=False,)
	value		= models.IntegerField(null=True, blank=True)
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.value)

	def __str__(self):
		return str(self.value)


@python_2_unicode_compatible  # only if you need to support Python 2
class Producto(models.Model):
	name 		= models.CharField(max_length=200, null=False, blank=False)
	price 		= models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)])
	sale_price 	= models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)])
	tablacatalogo = models.ForeignKey(TablaCatalogo)
	stock		= models.PositiveSmallIntegerField(null=True, blank=True)
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.name)

	def __str__(self):
		return str(self.name)


@python_2_unicode_compatible  # only if you need to support Python 2
class DocumentoCabecera(models.Model):
	seller		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	cliente		= models.ForeignKey(Cliente)
	ruc 		= models.CharField(max_length=15, default='0999999999001', null=False, blank=False)
	docid 		= models.CharField(max_length= 17, null=False, blank=False, unique=True)
	doctype		= models.CharField(max_length=3,choices=(('-','-'),('Fac','Factura'),('Ret','Retencion'),('NC','Nota Credito'),),default='Fac',)
	payment		= models.CharField(max_length=3,choices=(('-','-'),('Efe','Efectivo'),('Che','Cheque'),('Deb','Debito'),('Tar','Tarjeta'),),default='Efe',)
	iva			= models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)])
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.docid)

	def __str__(self):
		return str(self.docid)


@python_2_unicode_compatible  # only if you need to support Python 2
class DocumentoDetalle(models.Model):
	documento	= models.ForeignKey(DocumentoCabecera)
	producto	= models.ForeignKey(Producto)
	tablacatalogo = models.ForeignKey(TablaCatalogo)
	cantidad	= models.PositiveSmallIntegerField(null=False, blank=False)
	descuento	= models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)], default='0.00')
	subtotal	= models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(0)], default='0.00')
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.id)

	def __str__(self):
		return str(self.id)
