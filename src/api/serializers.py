from rest_framework import serializers
import re
from .models import Servicio, Producto, Cliente, Empleado, Turno
import datetime


class ServicioSerializer(serializers.ModelSerializer):
   class Meta:
      model = Servicio
      fields='__all__'
   
class ProductoSerializer(serializers.ModelSerializer):
 servicio = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
 class Meta:
   model = Producto
   fields='__all__'
   def validate_precio(self, value):
       if value < 0:
         raise serializers.ValidationError('El precio no puede ser negativo')
       return value

class ClienteSerializer(serializers.ModelSerializer):
    turnos = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = '__all__'

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError({"nombre":'El nombre no puede estar vacío.'})
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$', value):
            raise serializers.ValidationError({"nombre":"El nombre solo puede contener letras y no puede tener espacios u otros caracteres."})
        
        if len(value) < 2:
            raise serializers.ValidationError({'nombre':'El nombre debe tener al menos 2 caracteres.'})
        if len(value) > 36:
            raise serializers.ValidationError({"nombre":"El nombre no puede exceder los 36 caracteres."})
            
        return value

    def validate_apellido(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError({"apellido":"El apellido no puede estar vacío."})
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$', value):
            raise serializers.ValidationError({'apellido':"El apellido solo puede contener letras y no puede tener espacios u otros caracteres."})
        if len(value) < 2:
            raise serializers.ValidationError({'apellido':'El apellido debe tener al menos 2 caracteres.'})
        if len(value) > 36:
            raise serializers.ValidationError({'apellido':'El apellido no puede exceder los 36 caracteres.'})
            
        return value
    
    def validate_password(self, value):
        pass_length=len(str(value))
        if pass_length < 8:
            raise serializers.ValidationError({'password':'La contraseña tiene que ser mayor a 8 caracteres'})
        if pass_length>50:
            raise serializers.ValidationError({'password':'La contraseña debe ser menor a 50 caracteres'})
    
    def validate_edad(self, value):
        if value < 13:
            raise serializers.ValidationError('La edad del cliente no puede ser menor a 13 años.')
        return value
    
    def validate_usuario(self, value): 
     user_length = len(str(value))

     if user_length < 3:
        raise serializers.ValidationError({'usuario': 'El usuario no puede ser menor a 3 caracteres'})
     elif user_length >18:
        raise serializers.ValidationError({'usuario':'El usuario no puede ser mayor a 18 caracteres'})
     return value 
    
    def validate_nro_socio(self, value):
        if value < 0:
            raise serializers.ValidationError({'nro_socio': 'El numero de socio no puede ser negativo'})

    def validate_celular(self, value):
         celular_str = str(value)
         celular_length = len(celular_str)

         if celular_length < 10:
            raise serializers.ValidationError({'celular': 'El celular no puede ser menor a 10 dígitos.'})
         elif celular_length > 25:
            raise serializers.ValidationError({'celular': 'El celular no puede ser mayor a 25 dígitos.'})
         
         if not celular_str.isdigit():
             raise serializers.ValidationError({'celular': 'El celular solo puede contener dígitos numéricos.'})
         return value

    def get_turnos(self, obj):
        turnos_cliente = obj.cliente_turno.all().order_by('fecha', 'hora')
        return TurnoSerializer(turnos_cliente, many=True).data

class EmpleadoSerializer(serializers.ModelSerializer):
    turnos = serializers.SerializerMethodField()

    class Meta:
        model = Empleado
        fields = '__all__'

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError({"nombre":'El nombre no puede estar vacío.'})
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$', value):
            raise serializers.ValidationError({"nombre":"El nombre solo puede contener letras y no puede tener espacios u otros caracteres."})
        
        if len(value) < 2:
            raise serializers.ValidationError({'nombre':'El nombre debe tener al menos 2 caracteres.'})
        if len(value) > 36:
            raise serializers.ValidationError({"nombre":"El nombre no puede exceder los 36 caracteres."})
            
        return value

    def validate_apellido(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError({"apellido":"El apellido no puede estar vacío."})
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$', value):
            raise serializers.ValidationError({'apellido':"El apellido solo puede contener letras y no puede tener espacios u otros caracteres."})
        if len(value) < 2:
            raise serializers.ValidationError({'apellido':'El apellido debe tener al menos 2 caracteres.'})
        if len(value) > 36:
            raise serializers.ValidationError({'apellido':'El apellido no puede exceder los 36 caracteres.'})
            
        return value
    
    def validate_password(self, value):
        pass_length=len(str(value))
        if pass_length < 8:
            raise serializers.ValidationError({'password':'La contraseña tiene que ser mayor a 8 caracteres'})
        if pass_length>50:
            raise serializers.ValidationError({'password':'La contraseña debe ser menor a 50 caracteres'})

    def validate_usuario(self, value): 
       user_length = len(str(value))
       if user_length < 3:
        raise serializers.ValidationError({'usuario': 'El usuario no puede ser menor a 3 caracteres'})
       elif user_length >18:
        raise serializers.ValidationError({'usuario':'El usuario no puede ser mayor a 18 caracteres'})
       return value 
    
    def validate_legajo(self,value):
        if value < 0:
            raise serializers.ValidationError({'legajo': 'El legajo no puede ser negativo'})

    def validate_sueldo(self, value):
        if value < 0:
            raise serializers.ValidationError('El sueldo no puede ser negativo')
        return value

    def get_turnos(self, obj):
        turnos_empleado = obj.empleado_turno.all().order_by('fecha', 'hora')
        return TurnoSerializer(turnos_empleado, many=True).data

class TurnoSerializer(serializers.ModelSerializer):
   class Meta:
      model= Turno
      fields='__all__'
   def validate_hora(self, value):
        if not (datetime.time(11, 0) <= value <= datetime.time(20, 0)):
            raise serializers.ValidationError('La hora del turno debe ser entre las 11:00 y las 20:00.')
        if value.minute not in [0, 30]:
            raise serializers.ValidationError('Los minutos del turno deben ser en punto (00) o y media (30).')
        return value
   