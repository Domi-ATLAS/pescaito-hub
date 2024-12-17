# <strong>pescaito-hub</strong>

Grupo 1

Curso escolar: 2024/2025

Asignatura: Evolución y gestión de la configuración

## Miembros del equipo: escala de 1 al 10 con el esfuerzo hecho en el proyecto (10 mayor implicación, 1 menor implicación)


Miembro	| Implicación:

| Apellidos, Nombre | [1-10] |
|-------------------|--------|
| Pizarro López, Eduardo | [8] |
| Garate Fuentes, Yesica | [6] |
| Portillo Sánchez, Alonso | [10] |
| Sevillano Barea, Alejandro | [10] |
| Espinosa Naranjo, Pablo | [10] |
| Harana Mancilla, Rafael | [5] |


## Enlaces de interés:
repositorio de código: https://github.com/pescaito-team/pescaito-hub
sistema desplegado: https://uvlhub-pescaito-hub.onrender.com

| Miembro del equipo | Horas | Commits | LoC  | Test | Issues | Work Item          |
|--------------------|-------|---------|------|------|--------|--------------------|
| Pizarro López, Eduardo | 80    | 24      | 13993   | 19   | 09     | Permitir al usuario recibir una contraseña si tiene la configuración necesaria y restablecer su contraseña y cambiar su contraseña una vez iniciada la sesion. Se intento implementar el WI search querys el cual se avanzo hasta el punto de poder buscar por cadenas exactas en el buscador de datasets  |
| Garate Fuentes, Yesica | 55    | 44      | 1019   | 8   | 10     |  Permitir al usuario recibir una contraseña si tiene la configuración necesaria y restablecer su contraseña. Se intento implementar el WI search querys el cual se avanzo hasta el punto de poder buscar por cadenas exactas en el buscador de datasets  |
| Portillo Sánchez, Alonso | 85    | 17      | 1210   | 11   | 18     | Realizacion de FakeNodo, además de incluir la vista del perfil de usuario y el filtro avanzado en la bsuqueda de datasets |
| Sevillano Barea, Alejandro | 100    | 61      | 2769   | 9   | 16     | Construir un dataset seleccionando feature models y añadiendolos como si fuera un carrito y que se te descarguen automáticamente. Luego ese dataset se muestra en la lista de datasets. Realizacion de un dashboard para usuarios y para personas que no están registradas. |
| Espinosa Naranjo, Pablo  | 90    | 31      | 1187   | 7   | 11     | Realizacion de FakeNodo, ha incluido una serie de botones que permiten que cada dataset pueda ser valorado entre 1 a 5 estrellas modificando la base de datos para su incorporación  |
| Harana Mancilla, Rafael  | 30    | 22      | 908   | 6   | 4     | Realización de search queries: consiste en adaptar el motor de búsqueda para permitir cierto nivel de búsqueda programática de datasets  |
| **TOTAL**          | 440   | 199     | 21086  | 60  | 68    | Se han realizado 6 WI mas el FakeNodo, ademas de intentarse e implimentarse parte de otros 2  |


## Integración con otros equipos
N/P
## Resumen ejecutivo 

## Descripción del sistema
En este proyecto, se nos solicita hacer, por medio de un fork, una serie de implementaciones en el proyecto llamado "Uvlhub", desarrollado previamente por el departamento encargado de esta asignatura. Además, se nos solicitó implementar una serie de automatizaciones que agilizaran el proceso, así como implementar una Integración Continua y Despliegue Continuo.

Para esto, nuestro equipo "Pescaito-Team" realizó una elección de que work items ibamos a desarrollar, de un listado que nos era proporcionado. Escogimos los mencionados arriba; por un lado "Fakenodo", el cual era obligatorio, y proseguimos por la elección del resto de Work Items, los cuales fueron escogidos como se nos indico, un work item por miembro de equipo (6 miembros, por lo tanto 6 work items), y dos de cada dificultad, siendo estas low, medium y hard. Así, los escogidos inicialmente serían: 

### Fakenodo (High)

Este WI trata de sustituir las funcionalidades dadas por la API de Zenodo, por un Mock llamado "Fakenodo", el cual realizaria en local todos los procesos realizados por la API.

Esto implico:

- Estudio y conocimiento previo de las funciones de Zenodo en el proyecto inicial
- Desarrollo de servicio y rutas adicionales, con sus funcionalidades y restricciones logicas
- Correccion de llamadas a la API de zenodo, sustituidas por llamadas a los servicios y rutas de Fakenodo implementadas.
- Adición de botones que sirvan para llamar a las funciones creadas/actualizadas

Como funcionalidades añadidas, entonces, tendriamos:

- Upload de un dataset por via local, con el guardado del deposition los datos de los dataset y sus metadatos en local.
- Generación de DOI para su sincronización
- Opción de sincronizado y desincronizado de los dataset, siendo publicados cuando están sincronizados, y por tanto, visibles para el resto de usuarios

Adicionalmente:

- Un dataset ahora puede ser eliminado si este esta desincronizado (no publicado) por su usuario.

### RateDataset (Medium)

Este WI trata de añadir una funcionalidad que permita a los usuarios ratear los distintos Dataset. 

Esto implico:

- Planteamiento inicial de como seria implementado, como se registraria y calcularia la valoracion
- Adición de 3 atributos para el calculo de la valoración al modelo de Dataset, conllevando una actualización de la base de datos
- Creación de modelo rate en dataset, vinculado con un usuario y un dataset, conllevanto una actualización de la base de datos
- Desarrollo de funciones en repositorio, servicios y rutas para un correcto funcionamiento
- Adición de botones que sirvan para llamar a las funciones creadas
- Adición de la valoración media en distintas pantallas

Como funcionalidades añadidas, entonces, tendriamos:

- Valoraciones individuales de cada usuario para distintos datasets, unica para cada usuario en cada dataset
- Valoracion media de un dataset, visible para todos los usuarios que observen el listado de dataset publicados o los detalles de un dataset 

### View User Profile (Low)

Este WI trata de que cuando un usuario accede a un dataset y ve el autor de dicho dataset, el usuario puede clickear en el nombre del autor y acceder a la información del perfil del otro usuario.

Esto implico:

- Estudio y conocimiento previo de las funciones de Dataset y Profile en el proyecto inicial
- Desarrollo de rutas adicionales, templates y servicios con sus funcionalidades y restricciones logicas
- Adición de un hipervínculo en el nombre sel autor que sirvan para llamar a las funciones creadas/actualizadas

Como funcionalidades añadidas, entonces, tendriamos:

- Visualización del perfil de otros usuarios mediante un clickeo en un dataset

### Advanced Filtering (High)

Este WI trata de que cuando un usuario accede a la pestaña de explore, puede buscar diferentes datasets sincronizados mediante un filtrado avanzado de las diferentes características del dataset. 

Esto implico:
- Estudio y conocimiento previo de las funciones de Explore y Dataset en el proyecto inicial
- Desarrollo de scripts para que la funcionalidad se ejecutase en el frontend, con sus funcionalidades y restricciones lógicas
- Adición de bloques de enumerados que sirvan para aplicar el filtrado por la diferentes características

Como funcionalidades añadidas, entonces, tendriamos:

- Visualización de datasets por tipo de publicación, autor, archivos, tags, tamaño y título.
- Se pueden aplicar más de un filtro a la vez
- Botón de limpieza de filtro es capaz de poner en valor predeterminado todos los valores para que se vuelvana  mostrar todos los datasets

### Build my dataset (Medium)

Este WI consiste en la implementación de una funcionalidad para crear datasets seleccionando feature models específicos, añadiéndolos a un carrito y, posteriormente, generando el dataset final, el cual descargará automáticamente los feature models seleccionados.

Esto implicó:

- Comprensión de las relaciones entre módulos: Estudio de cómo se vinculan los módulos de dataset, feature model, auth y hubfile dentro del proyecto.
- Modificaciones en rutas y servicios: Desarrollo y actualización de las rutas y servicios necesarios para soportar la lógica de selección, adición al carrito, y creación del dataset.
- Interfaz de usuario:
        - Botón para seleccionar modelos de características (feature models) disponibles.
        - Botón para añadir modelos seleccionados al carrito.
        - Botón para generar el dataset a partir de los elementos del carrito.
- Sincronización y desincronización: Comprender el estado de los datasets (sincronizados y desincronizados) y cómo esto afecta las operaciones de creación y publicación.

### Dashboard (Medium)

Este WI trata sobre la creación de un dashboard que sirva como punto central de información y estadísticas tanto para usuarios registrados como para visitantes no registrados.

Esto implicó:

- Diseño y desarrollo del dashboard:
  - Generación de vistas diferentes para usuarios registrados y no registrados.
  - Incorporación de estadísticas relevantes como todas las que estan relacionadas con dataset, con featuremodel,autores y equipos.
- Interactividad:
  - Botones para la generación de gráficas relacionadas con las estadísticas mostradas.
  Exportación:
    -Botón para que el usuario pueda exportar su dashboard personalizado en formato PDF.

Estas funcionalidades agregaron valor al proyecto al proporcionar a los usuarios una visión consolidada y funcional de sus datos y estadísticas, mientras mantenían la diferenciación entre usuarios registrados y visitantes.

### Search Queries(High)

Este WI tiene como objetivo modificar la funcionalidad de búsqueda para que permita el paso a través de la barra de búsqueda de limitaciones por título, descripción o autor

Esto implicó:


- Lectura de formato de query desde la barra de búsqueda (argumento:"valor")
- Lectura de valores lógicos (&&, ||. And y Or lógico respectivamente)
- Procesamiento de la orden de búsqueda (Transformación del resultado en un arreglo de condiciones en una queries
- Se crearon las queries para que pudiesen unirse dentro de una misma
- Testing a través de selenium con casos que sirven como ejemplos de uso

### Remember password (Low)

Este WI tiene como objetivo implementar una funcionalidad que permita a los usuarios recuperar su contraseña de forma segura a través del correo electrónico.

Esto implico:

- Conocimiento sobre recuperar contraseña mediante un correo electrónico enviado desde una cuenta específica de Gmail.
- Conocimiento de configuración para la integración entre Gmail y la aplicación Flask

Como funcionalidades añadidas, entonces, tendriamos:
- Recuperación de contraseña con Gmail.
- Verificación para comprobar y validar el correcto funcionamiento del sistema de recuperación de contraseñas
- Función de editar la contraseña.



 --------------------------------------------------------------

 Una vez todo el equipo desarrolló sus Work Item, cada miembro pasó a realizar los test sobre los que fue responsable. Estos test se dividieron en:

- Test Unitarios: pruebas automatizadas que verifican el comportamiento individual de las unidades más pequeñas de un programa, como funciones o métodos. Su objetivo es asegurar que cada parte del código funcione de manera correcta y aislada

- Test de Interfaz: (Selenium): validan que la interfaz de usuario (UI) de una aplicación funcione correctamente y cumpla con las expectativas de usabilidad y comportamiento. Para ellos se utilizó Selenium, una herramienta popular que permite automatizar la interacción con aplicaciones web, simulando acciones del usuario como clics, ingreso de texto y navegación.

- Test de carga (Locust): evalúan el comportamiento de un sistema cuando se somete a una carga alta de usuarios o solicitudes simultáneas. Para ellos se utilizó Locust, herramienta de pruebas de carga basada en Python que permite simular múltiples usuarios concurrentes para medir el rendimiento y la capacidad del sistema.


Cada miembro del equipo se encargó de la decisión del tipo de pruebas a utilizar en los WI de los que era responsable, con una lógica detrás del porque esta toma de decisión. Una vez se realizó, se encargó de la implementacion dde las mismas

## Visión global del proceso de desarrollo

El proceso de desarrollo sigue una estructura clara y organizada, para garantizar una colaboración eficiente, un historial de cambios limpio y un código estable.

### Principales Aspectos del Proceso
 - **Gestión de Commits:**

    - Se aplican los **estándares Conventional Commits**, asegurando que cada cambio sea atómico, claro y rastreable.
    - Los commits siguen la estructura **tipo(<área>): descripción breve**, donde los principales tipos incluyen feat, fix, docs, entre otros.
    - Se prohíben los mensajes genéricos o commits con código incompleto.
      
- **Gestión de Issues:**

    - Las tareas y problemas se gestionan mediante issues clasificados por **etiquetas** estándar (feature, bug, docs, etc.) y **priorizados** en high, medium o low.
    - Cada issue debe contar con una **descripción clara**, **responsable asignado** y un **flujo de trabajo** definido para su resolución.
    - Las tareas activas se organizan en el Project "Pescaito HUB" según su **estado**: Todo, In Progress, Staged, Done o Stopped.
      
- **Gestión de Ramas:**

    - La rama **main** refleja siempre el código estable y listo para producción, mientras que la rama develop se utiliza para integración de funcionalidades.
    - Las nuevas funcionalidades se desarrollan en ramas **feature/** específicas, y las versiones estables se gestionan mediante ramas **release/** siguiendo un esquema semántico (X.Y.Z).
    - Las ramas principales tienen **reglas de protección**, como la aprobación obligatoria de pull requests y la integración continua (CI) para validar cambios.
      
### Aplicación de las Políticas

Las políticas establecidas se han venido aplicando de manera progresiva en el proyecto, garantizando que todo el equipo siga un proceso estructurado y eficiente. Desde la gestión de commits atómicos, pasando por la correcta clasificación de issues, hasta la organización y protección de las ramas, todas las acciones se han alineado con las políticas definidas. Este enfoque ha permitido mejorar la calidad del código, la colaboración en equipo y el seguimiento de tareas, asegurando que cada parte del flujo de trabajo esté bien documentada y bajo control.

 ### Más Información
 
Para detalles completos sobre las políticas de gestión de commits, issues y ramas, consulta los documentos específicos alojados en la misma carpeta. 

## Entorno de desarrollo

El desarrollo del proyecto se llevó a cabo en un entorno configurado de manera robusta y eficiente, con el objetivo de asegurar la reproducibilidad, estabilidad y facilidad de colaboración entre los miembros del equipo. A continuación, se describen los componentes esenciales del entorno y las herramientas utilizadas:

### Sistema Operativo y Configuración General
- **Sistema Operativo:** **Ubuntu 22.04 LTS**, utilizado de forma uniforme por todo el equipo para garantizar la compatibilidad.
- **Lenguaje de Programación:** **Python 3.10 o superior**, aprovechando las características modernas del lenguaje.
- **Framework Principal:** **Flask** como base para el desarrollo del backend.
- **Base de Datos:** **MariaDB** para el entorno de producción y pruebas, con las bases de datos uvlhubdb y uvlhubdb_test.
- **Gestión de Dependencias:** Todas las dependencias se manejaron mediante el archivo **requirements.txt** para asegurar consistencia entre los diferentes entornos.

### Configuración de la Base de Datos
La base de datos MariaDB fue configurada siguiendo los pasos estándar de instalación y asegurando las credenciales necesarias:

**1. Instalación del servidor:**

```bash
sudo apt update
sudo apt install mariadb-server -y
sudo systemctl start mariadb
```

**2. Configuración inicial:**

Ejecutar la configuración segura:

```bash
sudo mysql_secure_installation
```

Valores predeterminados para una correcta instalación:

```bash
- Enter current password for root (enter for none): (enter)
- Switch to unix_socket authentication [Y/n]: `y`
- Change the root password? [Y/n]: `y`
    - New password: `uvlhubdb_root_password`
    - Re-enter new password: `uvlhubdb_root_password`
- Remove anonymous users? [Y/n]: `y`
- Disallow root login remotely? [Y/n]: `y` 
- Remove test database and access to it? [Y/n]: `y`
- Reload privilege tables now? [Y/n] : `y`
```

Crear las bases de datos necesarias:

```MariaDB
CREATE DATABASE uvlhubdb;
CREATE DATABASE uvlhubdb_test;
CREATE USER 'uvlhubdb_user'@'localhost' IDENTIFIED BY 'uvlhubdb_password';
GRANT ALL PRIVILEGES ON uvlhubdb.* TO 'uvlhubdb_user'@'localhost';
GRANT ALL PRIVILEGES ON uvlhubdb_test.* TO 'uvlhubdb_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Configuración del Proyecto
Sigue estos pasos para preparar el entorno de desarrollo:

**1. Clonar el repositorio**
```bash
git clone git@github.com:<USUARIO_GITHUB>/pescaito-hub.git
cd pescaito-hub
```

**2. Configurar entorno virtual**

Este paso es opcional si se prefiere usar un entorno virtual para la instalación de las dependencias:
```bash
sudo apt install python3.12-venv
python3.12 -m venv venv
source venv/bin/activate
```

**3. Instalar dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Configurar variables de entorno**
```bash
cp .env.local.example .env
```

**5. Aplicar migraciones y poblar la base de datos**
```bash
flask db upgrade
rosemary db:seed
```

**6. Iniciar servidor de desarrollo**
```bash
flask run --host=0.0.0.0 --reload --debug
```
#### ¡Cuidado!

En caso de ocurrir algun error inesperado en el proceso de la misma que dificulte o inhabilite el despliegue del mismo, se deben ejecutar los siguientes comandos para **desinstalar MariaDB y empezar de 0 la instalación**:
```bash
sudo rm -rf /var/lib/mysql 
sudo rm -rf /etc/mysql 
sudo apt-get purge mariadb-server mariadb-client mariadb-common 
sudo apt-get autoremove 
sudo apt-get autoclean
```

Tras esto, se deberían repetir los comandos mencionados anteriormente correspondiente a la primera practica.

### Herramientas y Librerías Utilizadas


- **Frameworks Más Importantes:**

  - **Flask:** Es el framework principal en este proyecto. Flask es un framework web ligero y flexible para desarrollar aplicaciones web en Python. Las extensiones mencionadas como Flask-SQLAlchemy, Flask-RESTful, Flask-Login, Flask-Mail, y Flask-Migrate sugieren que se están utilizando funcionalidades como autenticación, gestión de bases de datos, servicios RESTful, migraciones de bases de datos y manejo de correos electrónicos.

  - **SQLAlchemy:** Este es un ORM (Object Relational Mapper) utilizado para interactuar con bases de datos de forma eficiente. Es esencial para manejar las conexiones y consultas a bases de datos en aplicaciones basadas en Flask.

  - **BeautifulSoup y lxml:** Son bibliotecas muy útiles para el procesamiento de datos HTML y XML. BeautifulSoup se utiliza comúnmente para scraping web, es decir, para extraer contenido de páginas web, y lxml es otro parser eficiente para trabajar con XML y HTML.

  - **pyOpenSSL y cryptography:** Son fundamentales si tu aplicación maneja conexiones seguras mediante HTTPS, encriptación de datos o autenticación, ya que proporcionan herramientas de seguridad y cifrado.

  - **Flamapy:** Este es un conjunto de librerías relacionadas con Modelos de Aprendizaje Automático, FM (Feature Model), SAT (Satisfiability), etc. Las distintas versiones de Flamapy (como flamapy-fm o flamapy-sat) sugieren que se está trabajando en tareas relacionadas con la gestión de configuraciones, satisfacibilidad, y posiblemente la integración de modelos de características o estructuras complejas.

- **Pruebas Más Importantes:**

    - **Pruebas Unitarias con pytest:** pytest es uno de los frameworks de prueba más utilizados. Se utiliza para escribir pruebas unitarias e integradas de forma sencilla. Con el plugin pytest-cov, puedes obtener información de cobertura del código, lo que permite identificar partes del código que no se están probando adecuadamente.pytest-html también es utilizado para generar informes HTML de las pruebas, lo que facilita la visualización de resultados.

    - **Pruebas de UI con Selenium:** Selenium permite realizar pruebas de interfaz de usuario simulando la interacción del usuario con la web. Usando Selenium-wire, se pueden realizar pruebas también sobre las solicitudes HTTP/HTTPS y analizar la red.

    - **Pruebas de Carga con Locust:** Locust permite simular una carga pesada en el sistema para verificar su rendimiento y escalabilidad bajo condiciones de estrés. A través de scripts en Python, se puede definir cómo se comportan los usuarios virtuales durante la prueba de carga.


## Ejercicio de propuesta de cambio

Se solicitará actualizar una funcionalidad, en este caso rate-dataset, haciendo que ahora se pueda valorar del 1 al 6

Se realizará todo el proceso de trabajo seguido a lo largo de trabajo, con sus correspondientes aperturas de código, issues…

Tras las correspondientes ediciones, se hará la pull request a la rama principal, siguiendo los procedimientos seguidos hasta ahora.




## Conclusiones y trabajo futuro

Como conclusiones, nos hemos visto envueltos en todos los procesos de evolución y gestión de la configuración vistos en la asignatura. Hemos podido observar lo util que es automatizar partes del proyecto para agilizar todos los procesos, así como distintas opciones de despliegue. También añadir como, a pesar de tener experiencia previamente en implementación de WI, no ha sido hasta ahora que lo hemos realizado siguiendo unas políticas estrictas en función a lo recomendado por la asignatura, las cuales hemos tenido que seguir a rajatabla, para una mayor profesionalidad, y claridad tanto para los usuarios implicados en el desarrollo como para cualquier persona externa que quiera observar commits, issues o ramas concretas en busca de información precisa.

En resumen, hemos podido observar casos reales de las distintas metodologías, procedimientos y tecnicas que nos han sido enseñadas. Así, nos hemos visto en el proceso de aprendizaje, entendiendo que hacía cada recurso implementado, enfrentandonos a su implementación y observando su utilidad una vez estaban en pleno funcionamento.

Para futuro, nos quedamos con todos los puntos positivos de aprendizaje mencionados anteriormente, pero también destacamos puntos a mejorar, como seguir unas políticas no demasiado enrrevesadas desde el inicio para agilizar el proceso, o adecuarse todos los miembros a los tiempos marcados para cada milestone, para evitar retrasos posteriores



https://github.com/EGCETSII/Entregables/wiki/Documento-del-proyecto
https://github.com/EGCETSII/Entregables/wiki/Modelo-de-portada
