from django.shortcuts import render
from django.db.models.deletion import RestrictedError

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Response as OpenAPIResponse, Parameter, IN_PATH, TYPE_INTEGER

from .serializers import ProductoSerializer, ClienteSerializer, EmpleadoSerializer, TurnoSerializer, ServicioSerializer
from .models import Cliente, Empleado, Producto, Turno, Servicio

# Create your views here.
def index(request):
    return render(request,'api/index.html')

class ProductoAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description='Obtiene la lista de productos',
        responses={200: ProductoSerializer(many=True)}
    )
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='API para crear nuevo producto',
        request_body=ProductoSerializer,
        responses={
            201: ProductoSerializer,
            400: OpenAPIResponse(
                description='Errores al crear productos',
                examples={
                    'application/json': {
                        'nombre': ['Este campo no puede estar en blanco'],
                        'precio': ['Debe ser un entero positivo']
                    }
                }
            ),
            403: 'No tiene permisos para acceder al recurso'
        }
    )
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Producto creado exitosamente', 'datos': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description='Obtiene un producto por id',
        responses={200: ProductoSerializer()}
    )
    def get(self, request, id_producto):
        try:
            producto = Producto.objects.get(pk=id_producto)
        except Producto.DoesNotExist:
            return Response({'message': 'El producto no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    def delete(self, request, id_producto):
        try:
            producto = Producto.objects.get(pk=id_producto)
            producto.delete()
            return Response({'mensaje': 'Producto eliminado exitosamente'}, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({'message': 'El producto no existe'}, status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({'error': 'No se puede eliminar el producto porque tiene elementos relacionados'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id_producto):
        try:
            producto = Producto.objects.get(pk=id_producto)
        except Producto.DoesNotExist:
            return Response({'message': 'El producto no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Producto actualizado exitosamente', 'datos': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClienteAPIView(APIView):
    model = Cliente
    permission_classes= [IsAuthenticated]
    @swagger_auto_schema(
            operation_description='Obtiene la lista de clientes',
            responses={200:ClienteSerializer(many=True)}
    )
    def get (self, request):
        cliente = Cliente.objects.all()
        serializer = ClienteSerializer(cliente, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(
            operation_description='API para crear nuevo cliente',
            request_body=ClienteSerializer,
            responses={
                201:ClienteSerializer,
                400: OpenAPIResponse(
                    description='Errores al crear clientes',
                    examples={
                        'application/json':{
                            'nombre':['Este campo no puede estar en blanco'],
                            'apellido':['Este campo no puede estar en blanco'],
                            'usuario':['Este campo no puede estar en blanco'],
                            'edad':['Debe ser un entero positivo'],
                            'email':['Este campo no puede estar en blanco'],
                            'celular':['Este campo no puede estar en blanco'], 
                            'nro_socio':['Debe ser un numero positivo'], 
                        }
                    }
                ),
                403:'No tiene permisos para acceder al recurso'
                }

    )
    def post(self, request):
        datos_peticion = request.data
        serializer = ClienteSerializer(data=datos_peticion)
        if serializer.is_valid():
            serializer.save()
            respuesta = {'mensaje': 'Cliente creado exitosamente', 'datos': serializer.data}
            return Response(respuesta, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClienteDetalleAPIView(APIView):
    model = Cliente
    permission_classes= [IsAuthenticated]
    @swagger_auto_schema(
            operation_description='Obtiene la lista de los turnos de cada cliente',
            responses={200:ClienteSerializer(many=True)}
    )
    def get(self, request, id_cliente):
        try:
            cliente = Cliente.objects.get(pk=id_cliente)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no existente'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    def put(self, request, id_cliente):
        try:
            cliente = Cliente.objects.get(pk=id_cliente)
        except Cliente.DoesNotExist:
            return Response({'message':'El cliente no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            respuesta = {'mensaje':'Cliente actualizado exitosamente', 'datos': serializer.data}
            return Response(respuesta, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id_cliente):
        try:
            cliente = Cliente.objects.get(pk=id_cliente)
            cliente.delete()
            return Response({'mensaje':'Cliente elminado exitosamente'}, status=status.HTTP_200_OK)
        except Cliente.DoesNotExist:
            return Response({'message':'El cliente no existe'}, status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({'error':'No se puede eliminar el cliente porque tiene elementos relacionados'},status=status.HTTP_400_BAD_REQUEST)
        

class EmpleadoAPIView(APIView):
    model = Empleado
    permission_classes= [IsAuthenticated]
    @swagger_auto_schema(
            operation_description='Obtiene la lista de empleados',
            responses={200:EmpleadoSerializer(many=True)}
    )
    def get (self, request):
        empleado = Empleado.objects.all()
        serializer = EmpleadoSerializer(empleado, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(
            operation_description='API para crear nuevo empleado',
            request_body=EmpleadoSerializer,
            responses={
                201:EmpleadoSerializer,
                400: OpenAPIResponse(
                    description='Errores al crear empleados',
                    examples={
                        'application/json':{
                            'nombre':['Este campo no puede estar en blanco'],
                            'apellido':['Este campo no puede estar en blanco'],
                            'usuario':['Este campo no puede estar en blanco'],
                            'legajo':['Debe ser un entero positivo'],
                            'email':['Este campo no puede estar en blanco'],
                            'servicio':['Este campo no puede estar en blanco'], 
                            'sueldo':['Debe ser un numero positivo'], 
                        }
                    }
                ),
                403:'No tiene permisos para acceder al recurso'
                }
    )
    def post(self, request):
        datos_peticion = request.data
        serializer = EmpleadoSerializer(data=datos_peticion)
        if serializer.is_valid():
            serializer.save()
            respuesta ={'mensaje':'Empleado creado exitosamente','datos':serializer.data}
            return Response(respuesta, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmpleadoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Obtiene los datos de un empleado por ID',
        responses={200: EmpleadoSerializer()}
    )
    def get(self, request, id_empleado):
        try:
            empleado = Empleado.objects.get(pk=id_empleado)
        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no existente'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data)

    def put(self, request, id_empleado):
        try:
            empleado = Empleado.objects.get(pk=id_empleado)
        except Empleado.DoesNotExist:
            return Response({'message': 'El empleado no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmpleadoSerializer(empleado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Empleado actualizado exitosamente', 'datos': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_empleado):
        try:
            empleado = Empleado.objects.get(pk=id_empleado)
            empleado.delete()
            return Response({'mensaje': 'Empleado eliminado exitosamente'}, status=status.HTTP_200_OK)
        except Empleado.DoesNotExist:
            return Response({'message': 'El empleado no existe'}, status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({'error': 'No se puede eliminar el empleado porque tiene elementos relacionados'}, status=status.HTTP_400_BAD_REQUEST)

class TurnoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Obtiene la lista de turnos',
        responses={200: TurnoSerializer(many=True)}
    )
    def get(self, request):
        turnos = Turno.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(turnos, request)
        serializer = TurnoSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description='API para crear nuevo turno',
        request_body=TurnoSerializer,
        responses={
            201: TurnoSerializer,
            400: OpenAPIResponse(
                description='Errores al crear turnos',
                examples={
                    'application/json': {
                        'cliente': ['Este campo no puede estar en blanco'],
                        'empleado': ['Este campo no puede estar en blanco'],
                        'producto': ['Este campo no puede estar en blanco'],
                        'hora': ['Este campo no puede estar en blanco'],
                        'fecha': ['Este campo no puede estar en blanco'],
                    }
                }
            ),
            403: 'No tiene permisos para acceder al recurso'
        }
    )
    def post(self, request):
        serializer = TurnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Turno creado exitosamente', 'datos': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TurnoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Obtiene los datos de un turno por ID',
        responses={200: TurnoSerializer()}
    )
    def get(self, request, id_turno):
        try:
            turno = Turno.objects.get(pk=id_turno)
        except Turno.DoesNotExist:
            return Response({'error': 'El turno no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TurnoSerializer(turno)
        return Response(serializer.data)

    def put(self, request, id_turno):
        try:
            turno = Turno.objects.get(pk=id_turno)
        except Turno.DoesNotExist:
            return Response({'message': 'El turno no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TurnoSerializer(turno, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Turno actualizado exitosamente', 'datos': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_turno):
        try:
            turno = Turno.objects.get(pk=id_turno)
            turno.delete()
            return Response({'mensaje': 'Turno eliminado exitosamente'}, status=status.HTTP_200_OK)
        except Turno.DoesNotExist:
            return Response({'message': 'El turno no existe'}, status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({'error': 'No se puede eliminar el turno porque tiene elementos relacionados'}, status=status.HTTP_400_BAD_REQUEST)

class ServicioAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description='Obtiene la lista de servicios',
        responses={200: ServicioSerializer(many=True)}
    )
    def get(self, request):
        servicios = Servicio.objects.all()
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='API para crear nuevo servicio',
        request_body=ServicioSerializer,
        responses={
            201: ServicioSerializer,
            400: OpenAPIResponse(
                description='Errores al crear servicios',
                examples={
                    'application/json': {
                        'nombre': ['Este campo no puede estar en blanco']
                    }
                }
            ),
            403: 'No tiene permisos para acceder al recurso'
        }
    )
    def post(self, request):
        serializer = ServicioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Servicio creado exitosamente', 'datos': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ServicioDetalleAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description='Obtiene los datos de un servicio por ID',
        responses={200: ServicioSerializer()}
    )
    def get(self, request, id_servicio):
        try:
            servicio = Servicio.objects.get(pk=id_servicio)
        except Servicio.DoesNotExist:
            return Response({'error': 'El servicio no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServicioSerializer(servicio)
        return Response(serializer.data)

    def put(self, request, id_servicio):
        try:
            servicio = Servicio.objects.get(pk=id_servicio)
        except Servicio.DoesNotExist:
            return Response({'message': 'El servicio no existe'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServicioSerializer(servicio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Servicio actualizado exitosamente', 'datos': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_servicio):
        try:
            servicio = Servicio.objects.get(pk=id_servicio)
            servicio.delete()
            return Response({'mensaje': 'Servicio eliminado exitosamente'}, status=status.HTTP_200_OK)
        except Servicio.DoesNotExist:
            return Response({'message': 'El servicio no existe'}, status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({'error': 'No se puede eliminar el servicio porque tiene elementos relacionados'}, status=status.HTTP_400_BAD_REQUEST)