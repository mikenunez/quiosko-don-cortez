from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

# Create your views here.
class FacturacionPage(View):
	def get(self, request, *args, **kwargs):
		context = {
			'title': '',
			'description': '',
			'form': ''
		}
		return render(request,"index.html",context)