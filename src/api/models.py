from django.db import models

# Create your models here.

class Servicio(models.Model):
    nombre= models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.nombre}'

class Producto(models.Model):
    servicio = models.ForeignKey(Servicio,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    precio = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return f"{self.servicio.nombre} {self.nombre}"

    
class Cliente(models.Model):
    nombre = models.CharField(max_length=36)
    apellido = models.CharField(max_length=36)
    usuario = models.CharField(max_length=18, unique=True)
    edad = models.IntegerField()
    email = models.EmailField(max_length=45, unique=True)
    celular = models.CharField(max_length=25, unique=True)
    nro_socio = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Empleado(models.Model):
    nombre = models.CharField(max_length=36)
    apellido = models.CharField(max_length=36)
    usuario = models.CharField(max_length=18, unique=True)
    email = models.EmailField(max_length=45, unique=True)
    legajo = models.IntegerField(unique=True, )
    sueldo= models.DecimalField(max_digits=8,decimal_places=2)
    servicio= models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='Servicio')

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.servicio.nombre}"

    
class Turno(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cliente_turno')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='empleado_turno')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='producto_turno')
    hora = models.TimeField()
    fecha = models.DateField()

    def __str__(self):
        return f'{self.hora}/{self.fecha}/{self.producto}/{self.empleado.nombre} {self.empleado.apellido}'