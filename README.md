# Proyecto. Conexión entre patio y recibo
En este repositorio se encuentran los archivos necesarios acerca del proyecto para mejorar la logistica en los patios de los centros de distribución para Grupo Bimbo.
Este trabajo fue realizado por:
* Pablo Ceballos Gutiérrez
* Santiago Martínez Vallejo
* Damián Suárez Bernal
* Adrián Aguilar Sánchez
* Daniel Olivares Ángeles
* Gael Pérez Gómez

## Pasos para correr el frontend
Una vez dentro de la carpeta raiz se debra ejecutar los siguientes comandos:
```
npm install
npm run dev
```
Esto correra el forntend de la aplicación en localhost:5173

## Pasos para correr el backend
Para que la aplicación corra apropiadamente, debe existir una base de datos de nombre 'bimbo'. Dentro de la consola de mySQL se debe correr el siguiente comando:
```
create database bimbo;
```
Esto creara la base de datos necesaria para que el backend funcione apropiadamente. De ser necesario, se deben cambiar las credenciales de ingreso a mySQL en el archivo 'settings.py' dentro de la carpeta 'bimbo':
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "bimbo",
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```
Una vez creada y configurada la base de datos, se deberan crear las migraciones de las tablas necesarias con el siguiente comando:
```
python manage.py makemigrations bimboC
```
Una vez creadas las migraciones, se migraran a la base de datos con el siguiente comando:
```
python manage.py migrate
```
Esto creara la tablas necesarias en la base de datos 'bimbo'.
Adicionalmente si se cuenta con el archivo de Excel con datos en el formato correcto, se podran migrar estos datos al ejecutar el archivo 'ExcelToBb.py'.
Para montar el backend en localhost, se debe ejecutar el siguiente comando:
```
python manage.py runserver
```
Esto correra el backend en localhost:8000.
