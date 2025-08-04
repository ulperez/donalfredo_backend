from django.urls import path
from . import views
from .views import index

urlpatterns =[
    path('',index, name='inicio'),
    path('productos/', views.ProductoAPIView.as_view(), name='producto-lista'),
    path('productos/<int:id_producto>/', views.ProductoDetalleAPIView.as_view(), name='producto-detalle'),
    path('clientes/', views.ClienteAPIView.as_view(),name='cliente-lista'),
    path('clientes/<int:id_cliente>/', views.ClienteDetalleAPIView.as_view(), name='cliente-detalle'),
    path('empleados/', views.EmpleadoAPIView.as_view(), name='empleado-lista'),
    path('empleados/<int:id_empleado>/', views.EmpleadoDetalleAPIView.as_view(), name='empleado-detalle'),
    path('turnos/', views.TurnoAPIView.as_view(), name='turno-lista'),
    path('turnos/<int:id_turno>/', views.TurnoDetalleAPIView.as_view(), name='turno-detalle'),
    path('servicios/', views.ServicioAPIView.as_view(), name='servicio-lista'),
    path('servicios/<int:id_servicio>/', views.ServicioDetalleAPIView.as_view(), name='servicio-detalle'),
]