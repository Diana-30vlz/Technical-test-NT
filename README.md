Manual de Usuario: Aplicación de Reportes de Cargos y API de Números Faltantes 🚀
Este manual proporciona instrucciones detalladas para configurar y ejecutar la aplicación de reportes de cargos y la API de números faltantes utilizando Docker y Docker Compose. ¡Prepárate para ponerlo en marcha! ✨

1. Introducción 🌟
Esta aplicación Django se compone de dos funcionalidades principales:

Reporte de Cargos por Día y Compañía: Una interfaz web que muestra el monto total de transacciones agrupadas por día y por compañía, con la capacidad de filtrar por fecha. 📊

API de Número Faltante: Un endpoint de API RESTful que recibe una lista de 99 números (asumiendo que son los primeros 100 números naturales con uno faltante) y devuelve el número que falta. 🔢

2. Prerrequisitos ✅
Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

Docker Desktop: Incluye Docker Engine y Docker Compose. 🐳

Descarga e instalación: https://www.docker.com/products/docker-desktop/

3. Configuración del Proyecto 🛠️
Sigue estos pasos para preparar el proyecto:

Clonar o Descargar el Proyecto: 📂
Asegúrate de tener la carpeta principal de tu proyecto (Prueba_Tecnica) en tu máquina local. Esta carpeta debe contener docker-compose.yml, Dockerfile, y las carpetas coreApp y webPersonal (la del proyecto Django).

Navegar al Directorio del Proyecto: ➡️
Abre tu terminal (PowerShell en Windows, o tu terminal preferida en Linux/macOS) y navega a la carpeta raíz de tu proyecto Prueba_Tecnica. Esta es la carpeta que contiene el archivo docker-compose.yml. Reemplaza [/ruta/a/tu/proyecto/Prueba_Tecnica] con la ubicación real en tu sistema.

cd [/ruta/a/tu/proyecto/Prueba_Tecnica]

¡Importante! Todos los comandos docker compose (como up, down, exec, ps, logs) deben ejecutarse desde esta carpeta. 💡

4. Configuración de la Base de Datos e Importación de Datos 💾
Antes de ejecutar la aplicación, necesitas configurar la base de datos y cargar los datos de ejemplo del archivo data_prueba.csv.

Construir y Levantar Contenedores (Primera Vez): 🏗️⬆️
Este comando construirá las imágenes de Docker y levantará los servicios web y db. Ejecútalo desde la carpeta raíz de tu proyecto (Prueba_Tecnica).

docker compose up --build -d

--build: Fuerza la reconstrucción de la imagen web (útil si hay cambios en el código o dependencias).

-d: Ejecuta los contenedores en segundo plano.

Realizar Migraciones de la Base de Datos: 🔄
Estos comandos ejecutan manage.py dentro del contenedor web para crear las tablas necesarias en tu base de datos PostgreSQL, basadas en tus modelos de Django (Company, Charges).

docker compose exec web python manage.py makemigrations coreApp
docker compose exec web python manage.py migrate

Crear un Superusuario (Opcional, para acceder al Admin de Django): 👤🔑
Si deseas acceder al panel de administración de Django, crea un superusuario. Se te pedirá un nombre de usuario, correo electrónico (opcional) y contraseña.

docker compose exec web python manage.py createsuperuser

Importar Datos del CSV: 📥
Este comando ejecutará tu comando de gestión personalizado para importar los datos de data_prueba.csv a la base de datos.

docker compose exec web python manage.py import_data data_prueba.csv

Asegúrate de que data_prueba.csv esté en la misma carpeta que tu docker-compose.yml.

5. Ejecutar la Aplicación ▶️
Una vez que la base de datos esté configurada y los datos importados, puedes iniciar o reiniciar la aplicación:

Para iniciar los contenedores (si no están corriendo):

docker compose up -d

Para reiniciar los contenedores (si ya están corriendo y has hecho cambios en el código):

docker compose down

docker compose up --build -d

6. Acceder a la Aplicación Web (Reporte de Cargos) 🌐
Una vez que los contenedores estén corriendo, puedes acceder al reporte de cargos a través de tu navegador web:

URL del Reporte de Cargos:
http://localhost:8000/

Aquí podrás ver el reporte y usar el filtro de fecha para ver los totales por día y compañía. 📈

7. Acceder a la API (Número Faltante) 💻
La API del número faltante espera peticiones POST con un cuerpo JSON. ¡No puedes acceder a ella directamente desde el navegador!

URL de la API:
http://localhost:8000/api/find-missing-number/

Cómo Probar la API (usando PowerShell): 🧪
Abre tu terminal (PowerShell) y ejecuta el siguiente comando. Este ejemplo envía una lista de números donde falta el 50.

Invoke-WebRequest -Uri http://localhost:8000/api/find-missing-number/ -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]}'

Si la API funciona correctamente, la terminal te devolverá una respuesta JSON similar a:

{"success": true, "missing_number": 50, "message": "El número faltante es: 50"}

8. Solución de Problemas Comunes ⚠️
Page not found (404):

Causa: La URL que estás intentando acceder no coincide con las rutas definidas en tus archivos urls.py.

Solución: Revisa tu webPersonal/urls.py y coreApp/urls.py para asegurarte de que las rutas estén definidas correctamente. Asegúrate de usar la URL completa http://localhost:8000/... si la ruta está en la raíz o http://localhost:8000/coreapp/... si está bajo coreApp/.

ERR_EMPTY_RESPONSE o "La conexión ha terminado de forma inesperada":

Causa: El servidor Django dentro del contenedor Docker se está cayendo o reiniciando debido a un error de Python.

Solución: Revisa los logs del contenedor web para ver el error exacto: docker compose logs web. Busca un "Traceback" de Python que te indicará la línea de código con el problema. Las causas comunes son:

ModuleNotFoundError: No module named 'coreApp.urls': Asegúrate de que 'coreApp' esté en INSTALLED_APPS en webPersonal/settings.py y que el archivo coreApp/urls.py exista y esté correctamente nombrado dentro de la carpeta coreApp.

Errores de sintaxis en views.py o utils.py.

Método no permitido. Esta API solo acepta peticiones POST.:

Causa: Estás intentando acceder a la API de número faltante directamente desde el navegador (que envía una petición GET) en lugar de usar una herramienta que envíe una petición POST.

Solución: Usa el comando Invoke-WebRequest en PowerShell (como se describe en la Sección 7) para enviar una petición POST con los datos JSON requeridos.

Problemas de Base de Datos (ej. "relation 'company' does not exist"):

Causa: Las migraciones no se han aplicado correctamente o la base de datos no está sincronizada con tus modelos.

Solución: Asegúrate de ejecutar docker compose exec web python manage.py makemigrations coreApp y docker compose exec web python manage.py migrate después de cualquier cambio en tus modelos (models.py).

