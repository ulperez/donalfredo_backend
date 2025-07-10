from django.contrib import admin
from .models import Cliente, Empleado, Servicio, Producto, Turno
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Servicio)
admin.site.register(Producto)
admin.site.register(Turno)
