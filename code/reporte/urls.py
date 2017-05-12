from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'diario$', views.ReporteDiarioPage.as_view(), name='reporte_diario'),
]
