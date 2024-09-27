# Proyecto Urban Routes

## Descripción del Proyecto
Este proyecto contiene pruebas automatizadas para verificar la funcionalidad de la plataforma **Urban Routes**. Las pruebas cubren acciones como seleccionar el origen y destino, elegir la tarifa Comfort, agregar un método de pago, y realizar pedidos adicionales como pedir una manta y pañuelos.

## Tecnologías y Técnicas Utilizadas
- **Lenguaje**: Python
- **Herramientas de automatización**: Selenium WebDriver
- **Gestión del navegador**: ChromeDriver
- **Técnicas**: 
  - Pruebas de interfaz de usuario
  - Esperas explícitas con Selenium

## Estructura del proyecto
- `data.py`: Contiene los datos necesarios, como la URL de Urban Routes, direcciones, número de teléfono y tarjeta.
- `main.py`: Implementa las pruebas automatizadas usando Selenium WebDriver.

## Instrucciones para ejecutar las pruebas
1. Asegurarnos de tener todas las dependencias instaladas (Selenium, pytest, etc.) en el entorno de Python.
2. Abrir PyCharm y asegurarnos de que el proyecto está cargado
   - Ve a File → Settings → Project: [nombre_del_proyecto] → Python Interpreter. 
   - Asegúrate de que tienes seleccionado el intérprete con Python 3.12.4 y que los paquetes necesarios están instalados.
3. Navega hasta el archivo de pruebas, en este caso main.py, en el explorador de archivos de la izquierda.
Haz clic derecho en el archivo de prueba.
Selecciona Run 'nombre_del_archivo'. Esto ejecutará todas las pruebas en el archivo.
Alternativamente, si estás usando pytest, también puedes hacer clic derecho en cualquier directorio o archivo que contenga tus pruebas y seleccionar Run 'pytest in nombre_del_directorio'.
4. Despues de ejecutarlo, PyCharm mostrara los resultados de las pruebas en la ventana de resultados.