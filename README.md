# Registro de pacientes automatizado

Script que toma los datos de un archivo csv, el cual contiene información de 1000 pacientes generados aleatorimente, y registra estos datos (de 3 pacientes escogidos al azar) de manera automatizada (utilizando Selenium) a la **demo B** de [Open EMR](https://demo.openemr.io/b/openemr/interface/login/login.php?site=default).

## Integrantes del equipo

* Maldonado Aguilar Angel Julian.
* Montejo Lopez Axel Alexis.

## Enlace a video de script en funcionamiento

https://drive.google.com/file/d/1-mY9pvHzL9_EF-zDDRKWT_Qfvkh5L8BH/view?usp=sharing

## Variables de configuración

* `path_to_chromedriver`

Se usa `chromedriver` para abrir el navegador Chrome. Si el `chromedriver` está en un directorio que se encuentra registrado en el `$PATH`,
establecer la variable `path_to_chromedriver = ''`, lo cual es el valor por defecto. Si el `chromedriver` no está en el path, colocar
la ruta al binario.

* `patients_to_register`

Cantiad de pacientes a registrar. Hay disponibles hasta 1000.

* `user`

El nombre de usuario con el que se iniciará sesión en el OpenEMR. El valor por defeto es `physician`. Se sugiere no cambiarse pues las opciones
de cada usuario varían de posición, y al no haber `id`s para todos los elementos en el flujo a seguir, el script puede romperse.

* `password_user`

Contraseña del usuario.

* `url`

URL del sitio donde está hosteado OpenEMR. Se usa la demo b, y se sugiere no cambiar, para evitar que algunos XPATH no se encuentren en caso de que en la demo original el admin configure apartados del sistema.
