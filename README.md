# 💈 API REST para Peluquería "Don Alfredo" 💈

Este repositorio contiene el backend de una API RESTful desarrollada con **Django y Python** para la gestión de la peluquería "Don Alfredo". Proporciona los servicios necesarios para la administración de turnos, clientes, servicios, empleados y más.

---

## 🚀 Características Principales

* **Gestión de Citas/Turnos:** Permite agendar, modificar y cancelar turnos.
* **Gestión de Clientes:** CRUD para la base de datos de clientes, historial de servicios.
* **Gestión de Servicios:** Catálogo de servicios ofrecidos por la peluquería.
* **Gestión de Empleados:** Registro y roles del personal.
* **Autenticación de Usuarios:** Sistema de usuarios y permisos (ej. administradores, empleados).
* **API RESTful:** Interfaz bien definida para interactuar con el frontend o aplicaciones de terceros.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**
* **Django 5.x** (o la versión que estés usando)
* **Django REST Framework** (DRF)
* **Base de Datos:** SQLite (por defecto en desarrollo, se puede configurar otra en producción)
* **Pipenv / Virtualenv** para gestión de dependencias (segun tu `venv` en la captura)

---

## 📦 Configuración y Ejecución Local

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

### 1. Clonar el Repositorio

```bash
git clone [https://github.com/ulperez/api_donalfredo]
````

### 2\. Crear y Activar el Entorno Virtual

Es **altamente recomendable** usar un entorno virtual para gestionar las dependencias del proyecto.

```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
# O en Windows: venv\Scripts\activate
```

### 3\. Instalar Dependencias

Instala todas las librerías necesarias utilizando `pip`:

```bash
pip install -r requirements.txt
```

### 4\. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (al mismo nivel que `manage.py`) con tus variables de entorno. Puedes usar `.env.example` como plantilla.

```ini
# .env
SECRET_KEY=
#CREDENCIALES BASE DE DATOS
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```


### 5\. Aplicar Migraciones

```bash
python manage.py migrate
```

### 6\. Crear Superusuario (Opcional, para acceder al admin de Django)

```bash
python manage.py createsuperuser
```

*(Sigue las indicaciones para crear el usuario y contraseña.)*

### 7\. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Una vez que el servidor esté en ejecución, podrás acceder a la API en `http://127.0.0.1:8000/` (o el puerto que te indique Django).

-----

## 🤝 Contribución
¡Las contribuciones son bienvenidas! Si deseas contribuir a este proyecto, por favor:

Haz un "fork" del repositorio.

Crea una nueva rama para tus cambios (git checkout -b feature/nombre-de-tu-feature).

Realiza tus cambios y haz commits descriptivos.

Haz "push" a tu rama (git push origin feature/nombre-de-tu-feature).

Abre un "Pull Request" (PR) describiendo tus cambios.


