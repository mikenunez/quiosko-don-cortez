from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View


from .forms import PickyAuthenticationForm


# Create your views here.
class LoginPage(View):

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			form = PickyAuthenticationForm()
			context = {
				'title': '',
				'description': '',
				'user': request.user,
				'form': form
			}
			return render(request,"login.html", context)
		else:
			return HttpResponseRedirect("/facturacion")

	def post(self, request, *args, **kwargs):
		form = PickyAuthenticationForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# Redirect to a success page.
			return HttpResponseRedirect("/facturacion")
		else:
			# Return an 'invalid login' error message.
			context = {
				'title': '',
				'description': '',
				'user': request.user,
				'form': form
			}
			return render(request,"login.html", context)


class LogoutPage(View):

	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect("/login")
