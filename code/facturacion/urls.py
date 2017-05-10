from django.conf.urls import url, include
from facturacion import views

urlpatterns = [
    url(r'^', views.FacturacionPage.as_view(), name='facturacion'),
]