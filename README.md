<div align="center">

  <a href="">[![Pytest Testing Suite](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/tests.yml)</a>
  <a href="">[![Commits Syntax Checker](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml/badge.svg?branch=main)](https://github.com/diverso-lab/uvlhub/actions/workflows/commits.yml)</a>
  
</div>

<div style="text-align: center;">
  <img src="https://www.uvlhub.io/static/img/logos/logo-light.svg" alt="Logo">
</div>

# Pescaito-HUB

Forked from a repository of feature models in UVL format integrated with Zenodo and flamapy following Open Science principles - Developed by DiversoLab and developed by Pescaito-hub team, formed by 4th grade software engineers in the subject "EGC".

## Official documentation

You can consult the official documentation of the project at the folder */docs*. There you can see all the different politics, the team diary, the project document and the founding document, with all the information than may interest you

## Guia ante posibles inconvenientes

### Acerca de la base de datos

Para la configuración e instalación de la base de datos, se deben utilizar los comandos vistos en la asignatura en la práctica 1.

En caso de ocurrir algun error inesperado en el proceso de la misma que dificulte o inhabilite el despliegue del mismo, se deben ejecutar los siguientes comandos:

sudo rm -rf /var/lib/mysql
sudo rm -rf /etc/mysql
sudo apt-get purge mariadb-server mariadb-client mariadb-common
sudo apt-get autoremove
sudo apt-get autoclean

Tras esto, se deberían repetir los comandos mencionados anteriormente correspondiente a la primera practica.


### Acerca de recuperar contraseña por gmail

Para que funcione la implementacion de remember password es necesario tener una cuenta de google, registrarse en local y  generar un archivo .env o en el existente colocar:

MAIL_USERNAME= TU CORREO DE GMAIL

MAIL_PASSWORD= CONTRASEÑA DE APLICACION NECESARIA PARA ELLO

La contraseña de apliacion se optiene desde el apartado de seguridad de google gmail

## Development Team

Here are the developers involved in Pescaito-Hub project:

<table>
    <tr>
        <td align="center">
            <a href="https://github.com/Domi-ATLAS">
                <img src="https://avatars.githubusercontent.com/u/87647202?v=4 width="100px;" alt="Eduardo Pizarro Lopez"/>
                <br />
                <sub><b>Eduardo Pizarro Lopez</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/alesevbar">
                <img src="https://avatars.githubusercontent.com/u/73104510?v=4 width="100px;" alt="Alejandro Sevillano Barea"/>
                <br />
                <sub><b>Alejandro Sevillano Barea</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/yesgarfue">
                <img src="https://avatars.githubusercontent.com/u/62544177?v=4 width="100px;" alt="Yesica Garate Fuentes"/>
                <br />
                <sub><b>Yesica Garate Fuentes</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/pabespnar">
                <img src="https://avatars.githubusercontent.com/u/92688817?v=4 alt="Alonso Portillo Sanchez"/>
                <br />
                <sub><b>Alonso Portillo Sanchez</b></sub>
            </a>
        </td>
              <td align="center">
            <a href="https://github.com/rharana">
                <img src="https://avatars.githubusercontent.com/u/91393864?v=4 width="100px;" alt="Rafael Harana Mancilla"/>
                <br />
                <sub><b>Rafael Harana Mancilla</b></sub>
            </a>
        </td>
        <td align="center">
            <a href="https://github.com/pabespnar">
                <img src="https://avatars.githubusercontent.com/u/73230195?s=400&v=4 width="100px;" alt="Pablo Espinosa Naranjo"/>
                <br />
                <sub><b>Pablo Espinosa Naranjo</b></sub>
            </a>
        </td>
    </tr>
</table>
