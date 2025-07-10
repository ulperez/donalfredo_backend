from django.urls import path
from . import views
from .views import index

urlpatterns =[
    path('',index, name='inicio'),
    path('productos/', views.ProductoAPIView.as_view()),
    path('clientes/', views.ClienteAPIView.as_view()),
    path('empleados/', views.EmpleadoAPIView.as_view()),
    path('turnos/', views.TurnoAPIView.as_view()),
    path('servicios/', views.ServicioAPIView.as_view()),
    path('clientes/<int:id_cliente>/', views.ClienteDetalleAPIView.as_view()),
    path('empleados/<int:id_empleado>/', views.EmpleadoDetalleAPIView.as_view()),
]