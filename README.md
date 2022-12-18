### Proyecto tweeter FastAPI

Este es un proyecto creado para el curso de [FastAPI](https://platzi.com/cursos/fastapi-errores/) de platzi, en el cual se crea una API que simula el comportamiento de la API de Tweeter; se puede registrar, actualizar, borrar y mostrar usuarios y tweets creados.

Para ejecutar el proyecto es necesario crear un entorno virtual e instalar las librerías descriptas en el archivo `requirements.txt`

Posteriormente, se debe ejecutar el servidor uvicorn con el siguiente comando:
~~~
python -m uvicorn main:app --reload
~~~
Una vez se ha activado el servidor, copiar la siguiente URL en el navegador web:
~~~
http://127.0.0.1:8000/docs
