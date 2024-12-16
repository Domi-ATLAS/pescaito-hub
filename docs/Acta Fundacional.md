# ACTA FUNDACIONAL

---

## Introducción

El presente documento establece los compromisos, responsabilidades y normas que rigen el funcionamiento del equipo de trabajo en el proyecto.  
Todos los miembros se comprometen a cumplir con las disposiciones aquí descritas para asegurar un ambiente colaborativo, profesional y orientado al éxito del proyecto.

---

## Objetivos del Proyecto

Realizar todas las tareas garantizando:  
- Trabajo en equipo.  
- Colaboración y aprendizaje.  
- Un entorno de trabajo positivo donde podamos superar la asignatura juntos.

---

## Roles y Responsabilidades

Cada integrante del equipo tendrá asignado un rol específico, el cual podrá ser modificado según las necesidades del proyecto y el consenso del grupo.  

### Roles Generales:
1. **Coordinador del Proyecto:**  
   - Supervisar el progreso general del equipo.  
   - Convocar reuniones.  
   - Mediar en conflictos.  
   - Asegurar que se cumplan los plazos.  

2. **Desarrollador/Implementador:**  
   - Programar, implementar y desarrollar funcionalidades clave del proyecto.  

3. **Documentador:**  
   - Mantener actualizada la documentación técnica y de usuario.  

4. **Tester:**  
   - Realizar pruebas de funcionalidad y calidad del proyecto.  

Los roles específicos se asignarán según las habilidades e intereses de cada integrante.

---

## Compromisos de los Miembros

Todos los integrantes del equipo se comprometen a:  
- Asistir puntualmente a las reuniones acordadas.  
- Participar activamente en las tareas asignadas y cumplir con los plazos establecidos.  
- Comunicarse con el equipo de manera oportuna y respetuosa.  
- Mantener una actitud colaborativa y profesional.  
- Respetar las políticas internas del proyecto (commits, ramas, issues, etc.).  

---

## Resolución de Conflictos y Penalizaciones

### **Conflicto 1: Falta de Participación Activa**

**Situación:**  
Un miembro no asiste a reuniones, no responde a mensajes, no participa en tareas asignadas o no demuestra interés en el proyecto.

**Acciones:**  
1. Se emitirán dos avisos formales documentados en acta.  
2. El miembro tendrá un plazo máximo de una semana para justificar su falta de participación y retomar sus responsabilidades.  
3. Si no hay mejoras, se discutirá su sanción o continuidad en el equipo, previa notificación formal y firma del acta.  
4. El equipo ajustará los horarios del miembro para facilitar su implicación.  
5. Si el comportamiento persiste, se evaluará su continuidad en el proyecto.  

---

### **Conflicto 2: Diferencias de Puntos de Vista sobre el Trabajo**

**Situación:**  
Existen enfoques o puntos de vista opuestos respecto a la dirección del trabajo.

**Acciones:**  
1. Fomentar el diálogo interno para resolver las diferencias de manera respetuosa y profesional.  
2. Si no se llega a un acuerdo, el coordinador o un tercero mediará en el conflicto.  
3. Las decisiones finales se tomarán por consenso o, si no es posible, mediante votación del equipo.  

---

### **Conflicto 3: Diferencias en los Niveles de Habilidad o Compromiso**

**Situación:**  
Los miembros tienen diferentes niveles de habilidad o interés, lo que puede afectar la calidad y eficiencia del trabajo.

**Acciones:**  
1. Los miembros más experimentados acompañarán y motivarán a aquellos con menor habilidad o experiencia.  
2. Se organizarán sesiones de capacitación o tutorías internas para reducir brechas y fomentar el aprendizaje.  
3. Si el miembro no mejora tras un aviso formal, se le asignarán tareas menos críticas o se redistribuirán sus responsabilidades.  
4. La dinámica del grupo funcionará en parejas para trabajar primero en una tarea y luego en otra. Si el equipo enfrenta dificultades, todo el grupo colaborará para resolverlas.  

---

### **Conflicto 4: Caso Excepcional**

**Situación:**  
Se da un escenario no contemplado en los conflictos anteriores.

**Acción:**  
Reunión urgente del equipo para discutir y decidir las medidas oportunas.

---

## Penalizaciones

Se aplicarán las siguientes penalizaciones para aquellos miembros que incumplan con sus responsabilidades o compromisos:

### **1. Amonestaciones Formales**
- Cualquier falta de compromiso o conducta inapropiada se notificará mediante una amonestación formal, documentada en acta.  

### **2. Aumento de Responsabilidades**
- Después de dos amonestaciones, el equipo puede decidir aumentar las responsabilidades del miembro en cuestión y reasignar tareas menos críticas a otros compañeros.  

### **3. Expulsión del Equipo**
- Si tras agotar las medidas anteriores el miembro no cumple con sus responsabilidades, se procederá a su expulsión definitiva.  
- La decisión será tomada por consenso o votación del equipo y documentada en acta.  
- En caso de expulsión, las tareas y responsabilidades del miembro serán redistribuidas para no comprometer los plazos ni la calidad del proyecto.

---

## Documentación

La documentación a entregar por el equipo será:

**Acta fundacional:** Este mismo documento, en el que se recoge la información más importante del proyecto, el equipo de trabajo y los procedimientos a seguir

**Diario de equipo:** Se recoge el trabajo semanal de los miembros individualmente y la valoración del mismo

**Politicas:** Distintos documentos que describen los procedimientos y directrices de trabajo a acatar por todos los miembros

**Documento del proyecto** 

---

## Gestión de ramas

Aquí se describen, a modo de resumen, los apartados mas importantes de la gestión de ramas del proyecto.
Las ramas utilizadas son:

**Main:** Rama principal en la cual solo se encuentra código estable y funcional

Formato: main


**Develop:** Unica rama que debe entrar converger con main, usada a modo de cortafuegos. El resto de ramas convergen en ella

Formato: develop


**Feature:** Rama destinada a funcionalidades o caracteristicas concretas. Estas branches nacen en develop, y una vez se finaliza la implementación de la funcionalidad necesaria mergean en la misma.

Formato: feature/<nombre-descriptivo>
Ejemplo: feature/autenticación-usuario

Para profundizar más en la gestión de ramas, se debe leer el documento correspondiente

---

## Gestión de issues

Aquí se describen, a modo de resumen, los apartados mas importantes de la gestión de issues del proyecto. Las etiquetas usadas para identificar su propósito y prioridad son:

**Feature:** Implementación o mejora de funcionalidad

**Bug:** Reporte de errores que causa fallos o comportamientos inesperados

**Enhacement:** Sugerencia de mejora de una funcionalidad

**Docs:** Creación o actualización de documentos

**Chore:** Enfocado a actualización de dependencias, configuración o mantenimiento.

**Research:** Investigación o consulta a modo de analisis para implementar una funcionalidad o correguir un error


Para la creación de una issue:

- El *titulo* debe ser claro y conciso
  
- La *descripción* debe resumir su cometido, con los pasos a seguir para obtener la solución, el comportamiento o
solución esperado, y el contenido adicional y versionado si procede.

- Cada issue debe tener tantas *etiquetas* como sea necesario para describir sus funciones y prioridades

Acerca de las *prioridades*, estas son:

- **High:** Problemas críticos de máxima urgencia

- **Media:** Funcionalidades importantes o errores no bloqueantes que deben solucionarse sin máxima prioridad

- **Low:** Tareas a resolver eventualmente

En cuanto a las *responsabilidades*, toda issue debe ser asignada a un único individuo, ya sea en su creación o posteriormente

El *flujo de trabajo* de los issues es:

**Creación ->**
**Etiquetado y clasificado ->**
**Asignación ->**
**Revisión ->**
**Resolución ->**
**Cierre**

Como *reglas adicionales*, destacamos:

-Evitar duplicidad de issues

-Las issues deben ser punto central de discusión del equipo

-Una issue podrá ser reabierta si fue cerrada prematuramente


*Para profundizar más en la gestión de issues, se debe leer el documento correspondiente*

---

## Gestión de commits

Aquí se describen, a modo de resumen, los apartados mas importantes de la gestión de commits del proyecto.

La estrictura a seguir para un commit será el de *Convencional Commit*:

<tipo>(<area>): <descripción breve>

[opcional]: Cuerpo de mensaje

Los *tipos de commits* son:

- feat: Inclusión de funcionalidades
- fix: Corrección de errores
- docs: Cambios en documentación
- style: Cambios en estilo de código
- refactor: Cambios en estructura del codigo a mejor
- test: En relación a pruebas
- chore: En relación a adición de herramientas, bibliotecas o versionados actualizados
- perf: Cambios para mejorar el rendimiento
- build: Cambios que afectan al sistema de construcción o dependencias externas
- ci: Cambios en los archivos de configuración CI y scripts

Un commit debe ser atómico, conteniendo **un único** cambio significativo, sin combinar múltiples cambios en el mismo, funcionando de manera independiente

En cuanto a su estructura, su cuerpo es *obligatorio*, sirviendo para explicar su mótivo o su funcionalidad. El pie de mensaje es *opcional*, usandose para cerrar issues, referencias documentos o proporcionar detalles especificos

En cuanto a sus buenas prácticas:

- Uso de modo imperativo
- Descripción breve, clara y concisa (-50 caracteres)
- Cuerpo breve (-72 caracteres)

Para su *validación, revisión y aprobación*, cada commit sera revisado antes de su integración en otra rama, verificandose lo mencionado anteriormente

El *flujo de trabajo de commits y pull request* es:

**Trabajo en nueva rama ->**
**Commit atómico ->**
**Sincronización regular ->**
**Pull request ->**
**Revisión ->**
**Fusión y eliminación de la rama**

Como *reglas adicionales*, destacamos:

- Se deben evitar commits con código incompleto o roto
  
- Se deben pasar todas las pruebas locales implementadas antes de subir el commit

- Se evitan mensajes genéricos

- Si el cambio no es trivial, se proporcionará descripción

- Uso de ramas correctas, de la mano con el tipo del commit (feature - feat, fix - fix)

- En la rama main no podrán realizarse commits si no son de tipo docs



*Para profundizar más en la gestión de commits, se debe leer el documento correspondiente*


