# Poner en producción el proyecto "social"

## 1.- Como usuario `root` Crear usuario `cuahutli` y directorio `www` que contendrá la web
- Creamos un nuevo usuario en linux llamado `websamao` 
    ```sh
    adduser cuahutli
    ```

- después de esto nos hará una serie de preguntas este es un ejemplo del output, en donde nos pide la contraseña escribirla y anotarla ya que será la contraseña del usuario que usaremos
    ```sh
    Adding user `cuahutli' ...
    Adding new group `cuahutli' (1001) ...
    Adding new user `cuahutli' (1001) with group `cuahutli' ...
    Creating home directory `/home/cuahutli' ...
    Copying files from `/etc/skel' ...
    Enter new UNIX password:
    Retype new UNIX password:
    passwd: password updated successfully
    Changing the user information for urban
    Enter the new value, or press ENTER for the default
    Full Name []:
    Room Number []:
    Work Phone []:
    Home Phone []:
    Other []:
    Is the information correct? [Y/n]
    ```

- Agregar el usuario a la lista de sudoers
    ```sh
    gpasswd -a cuahutli sudo
    ```
    
- Cambiar al nuevo usuario creado `cuahutli`
    ```sh
    su - cuahutli
    ```

- Cambiar al `home` de `cuahutli`
    ```sh
    cd ~
    ```

- Crear un nuevo directorio para las webs
    ```sh
    mkdir www
    ```
    
## 2.- Instalar virtualenv

- Instalar el paquete `pip` en nuestro sistema.
 
    ```sh
    sudo apt-get install python-pip
    ```
   
- Instalar `virtualenv` en nuestro python
   ```sh
    sudo pip install virtualenv
    ```   
    
## 3.- Clonar nuestra web y echarla a andar

- Acceder a nuestro usuario `cuahutli` si aún no estamos en él o salimos por alguna razón
   ```sh
    su cuahutli
    ```
    
- Ir al directorio de `www` en el usuario `cuahutli`
   
   ```sh
    cd ~/www
    ```

- Clonar nuestro repositorio
   ```sh
    git clone https://github.com/Cuahutli/cuahutweet.git
    ```

- Acceder al directorio `cuahutweet` creado al hacer el clone dentro de `www`
   ```sh
    cd cuahutweet
    ```
    
- Creamos un entorno virtual con `virtualenv`
   ```sh
    virtualenv -p python3 venv
    ```
 
- Activamos nuestro entorno virtual.
   ```sh
    source venv/bin/activate
    ```
    
- Instalamos los paquetes necesarios para nuestro programa en nuestro entorno virtual
   ```sh
    pip install -r requirements.txt
    ```

- Recolectamos los archivos estáticos de nuestra `app django`
    ```sh
    cd src && python manage.py collectstatic
    ```
    
-  Con el comando anterior se debio haber creado un directorio `static-cdn` dentro del directorio `cuahutweet` , accedemos a él y creamos un directorio llamado `media`
   ```sh
    cd ~/www/cuahutweet/static-cdn && mkdir media
    ```
    

## 4.- Instalar y configurar apache

- Instalar `apache`

    ```sh
    sudo apt-get install apache2
    ```

- Instalar `lib-wsgi` para usar los proyectos de django
    ```sh
    # si usas python 3
    sudo apt-get install libapache2-mod-wsgi-py3
    
    # si usas python 2
    sudo apt-get install libapache2-mod-wsgi
    ```    
    
## 5.- Habilitar nuestro sitio en apache

- Creamos un enlace simbólico del archivo contenido en la carpeta `conf` del proyecto a `/etc/apache2/sites-available`
    ```sh
    sudo ln -s /home/cuahutli/www/cuahutweet/conf/apache-social.conf /etc/apache2/sites-available/
    ```
    
- Habilitamos nuestro sitio en apache
    ```sh
    sudo a2ensite apache-social.conf
    ```
- Recargamos el servidor apache
    ```sh
    sudo service apache2 reload
    ```    

## 6.- Ajustar permisos en las carpetas para que todo funcione correctamente

- Agregar al usuario `cuahutli` al grupo `www-data` de apache
    ```sh
    sudo adduser cuahutli www-data
    ```

- Modificar los permisos en la carpeta `www`
    ```sh
    sudo chown -R cuahutli:www-data /home/cuahutli/www
    ```

## 7.- Actualizar el proyecto con los cambios realizados.
    
Una vez implementado el proyecto para actualizarlo con los cambios que se hayan realizado y que todo funcione correctamente se deben realizar los siguientes pasos.

- Ingresar a la ruta del proyecto
    ```sh
    cd ~/www/cuahutweet
    ```
    
- Bajar las actualizaciones del proyecto del repositorio git.
    ```sh
    git pull
    ```

- Activar el entorno virtual
   ```sh
    source venv/bin/activate
    ```
    
- Actualizar las librerias del entorno virtual por si se incluyó alguna nueva.
    ```sh
    pip install -r requirements.txt
    ```
    
- Actualizar la Base de Datos por si se realizaron cambios:
    ```sh
    cd src &&  python manage.py makemigrations && python manage.py  migrate
    ```

- Recolectar estáticos
    ```sh
    python manage.py collectstatic
    ```

- Volver a establecer los permisos correctos en Linux
    ```sh
    sudo chown -R cuahutli:www-data /home/cuahutli/www
    ```

- Recargar apache
    ```sh
    sudo service apache2 reload
    ```

- Validar que apache arrancó correctamente
   ```sh
    sudo service apache2 status
    ```
    
     
### XX.- Solución de problemas

----   

- Si hay un problema al correr la app en apache y dentro de los logs de error aparece un error similar a :
    ```sh
    [error] mod_wsgi (pid=31000): Call to 'site.addsitedir()' failed for '(null)', stopping.
    ```

    entonces habría que cambiar en el archivo de configuración la linea:
    
    ```sh
    WSGIDaemonProcess insamao python-path=/home/cuahutli/www/cuahutweet/src/:/home/cuahutli/www/cuahutweet/venv/lib/python3.5/site-packages
    ```
    
    por la siguiente:

    ```sh
    WSGIDaemonProcess uscitme python-path=/home/cuahutli/www/cuahutweet/src/ python-home=/home/cuahutli/www/cuahutweet/venv/lib/python3.5/site-packages
    ```