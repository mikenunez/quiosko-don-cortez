from django.db import models
from django.utils.encoding import python_2_unicode_compatible # only if you need to support Python 2
# Create your models here.

@python_2_unicode_compatible  # only if you need to support Python 2
class Cliente(models.Model):
	ruc 		= models.IntegerField(null=False, blank=False)
	email 		= models.EmailField(max_length=200, null=False, blank=False)
	firstname 	= models.CharField(max_length= 100, null=False, blank=False)
	lastname 	= models.CharField(max_length= 100, null=True, blank=True)
	phone		= models.CharField(max_length= 20, null=True, blank=True)
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.email)

	def __str__(self):
		return str(self.email)


@python_2_unicode_compatible  # only if you need to support Python 2
class Producto(models.Model):
	name 		= models.CharField(max_length=200, null=False, blank=False)
	price 		= models.DecimalField(decimal_places=2, max_digits=20)
	sale_price 	= models.DecimalField(decimal_places=2, max_digits=20)
	stock		= models.IntegerField(null=True, blank=True)
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.name)

	def __str__(self):
		return str(self.name)


@python_2_unicode_compatible  # only if you need to support Python 2
class TablaCatalogo(models.Model):
	code 		= models.CharField(max_length= 6, null=False, blank=False, unique=True)
	description	= models.CharField(max_length= 50, null=False, blank=False,)
	value		= models.IntegerField(null=True, blank=True)
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.description)

	def __str__(self):
		return str(self.description)


@python_2_unicode_compatible  # only if you need to support Python 2
class DocumentoCabecera(models.Model):
	ruc 		= models.IntegerField(default='0999999999001', null=False, blank=False)
	doc_id 		= models.CharField(max_length= 15, null=False, blank=False, unique=True)
	doc_type	= models.CharField(max_length=3,choices=(('-','-'),('Fac','Factura'),('Ret','Retencion'),('NC','Nota Credito'),),default='Fac',)
	cliente		= models.ForeignKey(Cliente)
	payment		= models.CharField(max_length=3,choices=(('-','-'),('Efe','Efectivo'),('Che','Cheque'),('Deb','Debito'),('Tar','Tarjeta'),),default='Efe',)
	subtotal	= models.DecimalField(decimal_places=2, max_digits=20)
	tablacatalogo = models.ForeignKey(TablaCatalogo)
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.doc_id)

	def __str__(self):
		return str(self.doc_id)


@python_2_unicode_compatible  # only if you need to support Python 2
class DocumentoDetalle(models.Model):
	documento 	= models.ForeignKey(DocumentoCabecera)
	produto		= models.ForeignKey(Producto)
	cantidad	= models.IntegerField(null=True, blank=True)
	created		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True, auto_now_add=False)
	
	def __unicode__(self):
		return str(self.id)

	def __str__(self):
		return str(self.id)
