from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'facturas$', views.ReporteFacturaPage.as_view(), name='reporte_factura'),
]