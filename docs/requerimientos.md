# Análisis y definición del requerimiento

## 1. Supuestos y acuerdos

Como el requerimiento original tiene aspectos no definidos, se establecen los siguientes acuerdos para llegar al comportamiento esperado del sistema.

| ID   | Ambigüedad                                                                  | Acuerdo                                                                                                                                     |
| ---- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| A-01 | No se indican los datos obligatorios de una persona autorizada.             | Cada usuario tendrá ID, nombre, correo, contraseña y rol.                                                                                   |
| A-02 | No se indican los datos obligatorios de un equipo.                          | Cada equipo tendrá ID, nombre, categoría, estado y descripción.                                                                             |
| A-03 | No se define la cantidad máxima de equipos por persona.                     | Un solicitante podrá mantener como máximo 3 equipos asociados a préstamos activos.                                                          |
| A-04 | No se define la duración máxima de un préstamo.                             | Un préstamo podrá durar como máximo 2 días hábiles.                                                                                         |
| A-05 | No se define con cuánta anticipación se puede reservar.                     | Una reserva podrá realizarse con hasta 30 días de anticipación.                                                                             |
| A-06 | No se define qué ocurre con solicitudes superpuestas.                       | Un mismo equipo no podrá estar asignado a préstamos cuyas fechas se superpongan.                                                            |
| A-07 | No se define si usuarios atrasados pueden solicitar nuevos equipos.         | Un usuario con al menos un préstamo atrasado no podrá crear nuevas solicitudes.                                                             |
| A-08 | No se definen los estados de una solicitud/préstamo.                        | Se utilizarán los estados: SOLICITADA, APROBADA, RECHAZADA, ENTREGADA, DEVUELTA y CANCELADA.                                                |
| A-09 | No se define cuándo se puede cancelar una solicitud.                        | El solicitante podrá cancelar mientras la solicitud esté en estado SOLICITADA o APROBADA, siempre que el equipo aún no haya sido entregado. |
| A-10 | No se define cómo tratar equipos dañados o en mantenimiento.                | Los equipos podrán estar DISPONIBLE, PRESTADO o MANTENIMIENTO. Solo los equipos disponibles podrán incorporarse a nuevas solicitudes.       |
| A-11 | No se define cuándo un préstamo está atrasado.                              | Se considera atrasado cuando la fecha actual supera la fecha de devolución comprometida y el préstamo continúa en estado ENTREGADA.         |
| A-12 | No se define si una solicitud puede contener períodos distintos por equipo. | Todos los equipos de una misma solicitud compartirán la misma fecha de inicio y devolución.                                                 |

---

## 2. Requerimiento mejorado

El sistema deberá permitir gestionar préstamos de equipos tecnológicos de un Fablab universitario mediante una aplicación de línea de comandos.

El sistema deberá permitir registrar y autenticar usuarios, diferenciando al menos los roles Solicitante y Encargado.

Los solicitantes podrán consultar los equipos registrados, revisar su disponibilidad, crear solicitudes de préstamo, consultar sus solicitudes y cancelar aquellas que aún no hayan sido entregadas.

Los encargados podrán administrar usuarios y equipos, revisar solicitudes, aprobarlas o rechazarlas y registrar la entrega y devolución de los equipos.

El sistema tiene que impedir operaciones que violen las reglas de negocio definidas, tales como préstamos superpuestos, solicitudes de usuarios con atrasos, exceso de equipos activos, equipos en mantenimiento y períodos superiores al máximo permitido.

Toda la información deberá mantenerse entre ejecuciones mediante persistencia local y se deben generar registros de eventos relevantes mediante logs.

---

## 3. Reglas de negocio

### RN-01 — Límite de equipos activos

Un solicitante podrá mantener como máximo 3 equipos asociados a préstamos activos simultáneamente.

### RN-02 — Duración máxima

La duración de un préstamo no podrá superar 2 días hábiles.

### RN-03 — Anticipación máxima

Una reserva podrá solicitarse como máximo con 30 días de anticipación.

### RN-04 — Solapamiento

Un equipo no podrá estar asignado a más de un préstamo cuando sus períodos se superpongan.

### RN-05 — Usuario con atraso

Un usuario con al menos un préstamo atrasado no podrá crear nuevas solicitudes.

### RN-06 — Disponibilidad del equipo

Solo podrán solicitarse equipos cuyo estado permita su préstamo y que se encuentren libres durante todo el período solicitado.

### RN-07 — Aprobación

Solo un usuario con rol Encargado podrá aprobar o rechazar solicitudes.

### RN-08 — Entrega

Solo podrán registrarse entregas correspondientes a solicitudes previamente aprobadas.

### RN-09 — Devolución

Solo podrán devolverse préstamos que se encuentren en estado ENTREGADA.

### RN-10 — Cancelación

Una solicitud podrá cancelarse únicamente mientras se encuentre SOLICITADA o APROBADA y antes de registrar su entrega.

### RN-11 — Fechas válidas

La fecha de devolución deberá ser posterior a la fecha de inicio.

### RN-12 — Estado atrasado

Un préstamo se considerará atrasado cuando la fecha comprometida de devolución haya vencido y aún no exista una devolución registrada.

---

## 4. Alcance

El sistema incluirá:

- autenticación básica
- gestión de usuarios
- gestión de equipos
- consulta de disponibilidad
- creación de solicitudes
- aprobación y rechazo de solicitudes
- cancelación de solicitudes
- entrega de equipos
- devolución de equipos
- consulta de préstamos vigentes, futuros y atrasados
- persistencia local
- validación de reglas de negocio
- manejo de errores
- logs
- integración con Sentry
- datos de demostración.

---

## 5. Exclusiones

Quedan fuera del alcance:

- interfaz web o gráfica
- pagos o multas
- notificaciones por correo
- integración con sistemas institucionales
- base de datos remota
- recuperación de contraseña
- distintos niveles de prioridad entre usuarios
- gestión detallada de daños o reparaciones
- autenticación mediante cuentas institucionales
- reservas recurrentes.

---

## 6. Criterios de aceptación iniciales

### CA-01 — Inicio de sesión

Dado un usuario registrado con credenciales válidas, cuando ingresa su correo y contraseña, entonces el sistema debe autenticarlo y mostrar las opciones correspondientes a su rol.

### CA-02 — Credenciales inválidas

Dado un intento de inicio de sesión con credenciales incorrectas, el sistema debe rechazar el acceso.

### CA-03 — Solicitud válida

Dado un solicitante habilitado y un equipo disponible, cuando solicita un período válido, entonces la solicitud debe registrarse correctamente.

### CA-04 — Máximo de equipos

Dado un usuario que ya posee 3 equipos asociados a préstamos activos, cuando intenta solicitar otro equipo, entonces el sistema debe rechazar la solicitud.

### CA-05 — Usuario atrasado

Dado un usuario con un préstamo atrasado, cuando intenta crear una nueva solicitud, entonces el sistema debe impedir la operación.

### CA-06 — Solapamiento

Dado un equipo reservado para un determinado período, cuando se intenta aprobar otra solicitud cuyo período se superpone, entonces el sistema debe rechazar la aprobación.

### CA-07 — Duración

Dada una solicitud cuya duración supera 2 días, el sistema debe rechazarla.

### CA-08 — Equipo en mantenimiento

Dado un equipo marcado como MANTENIMIENTO, cuando un solicitante intenta reservarlo, entonces el sistema no debe permitir la solicitud.

### CA-09 — Entrega

Dada una solicitud APROBADA, cuando el encargado registra la entrega, entonces la solicitud debe cambiar a ENTREGADA.

### CA-10 — Devolución

Dado un préstamo ENTREGADO, cuando el encargado registra la devolución, entonces debe cambiar a DEVUELTA y el equipo debe quedar nuevamente disponible si no existen reservas incompatibles.

### CA-11 — Cancelación

Dada una solicitud SOLICITADA o APROBADA, cuando el solicitante la cancela antes de la entrega, entonces debe pasar a CANCELADA.

### CA-12 — Persistencia

Dado que se registraron usuarios, equipos y préstamos, cuando se cierra y vuelve a ejecutar la aplicación, entonces los datos deben mantenerse.

# 7. Estados y transiciones del préstamo

## 7.1 Estados

Cada solicitud de préstamo tendrá uno de los siguientes estados:

| Estado     | Descripción                                                                                                      |
| ---------- | ---------------------------------------------------------------------------------------------------------------- |
| SOLICITADA | La solicitud fue creada por un solicitante y se encuentra pendiente de revisión.                                 |
| APROBADA   | La solicitud fue revisada y aceptada por un encargado. Los equipos quedan reservados para el período solicitado. |
| RECHAZADA  | La solicitud fue revisada y rechazada por un encargado.                                                          |
| ENTREGADA  | Los equipos asociados a una solicitud aprobada fueron entregados al solicitante.                                 |
| DEVUELTA   | Todos los equipos asociados al préstamo fueron devueltos al laboratorio.                                         |
| CANCELADA  | La solicitud fue cancelada antes de que se registrara la entrega.                                                |

El atraso no se considerará un estado independiente. Un préstamo estará atrasado cuando permanezca en estado `ENTREGADA` después de superar su fecha comprometida de devolución.

---

## 7.2 Transiciones permitidas

| Estado actual | Estado siguiente | Responsable | Condiciones                                                                            |
| ------------- | ---------------- | ----------- | -------------------------------------------------------------------------------------- |
| SOLICITADA    | APROBADA         | Encargado   | Usuario habilitado, equipos disponibles y cumplimiento de todas las reglas de negocio. |
| SOLICITADA    | RECHAZADA        | Encargado   | El encargado decide rechazar la solicitud.                                             |
| SOLICITADA    | CANCELADA        | Solicitante | La solicitud todavía no ha sido entregada.                                             |
| APROBADA      | ENTREGADA        | Encargado   | Los equipos son entregados físicamente al solicitante.                                 |
| APROBADA      | CANCELADA        | Solicitante | La entrega todavía no ha sido registrada.                                              |
| ENTREGADA     | DEVUELTA         | Encargado   | Todos los equipos asociados al préstamo fueron recibidos de vuelta.                    |

Los estados `RECHAZADA`, `CANCELADA` y `DEVUELTA` son estados finales y no permiten nuevas transiciones.

---

## 7.3 Transiciones no permitidas

El sistema debe rechazar cualquier transición no definida explícitamente.

Ejemplos:

- SOLICITADA -> ENTREGADA
- SOLICITADA -> DEVUELTA
- RECHAZADA -> APROBADA
- CANCELADA -> APROBADA
- DEVUELTA -> ENTREGADA
- ENTREGADA -> CANCELADA

Cuando se intente realizar una transición inválida, la aplicación deberá:

1. impedir el cambio de estado
2. informar el motivo al usuario
3. mantener el estado anterior
4. registrar el intento en los logs cuando corresponda.

---

## 7.4 Estado de los equipos

Cada equipo podrá encontrarse en uno de los siguientes estados:

| Estado        | Descripción                                                                    |
| ------------- | ------------------------------------------------------------------------------ |
| DISPONIBLE    | El equipo puede ser considerado para nuevas solicitudes.                       |
| PRESTADO      | El equipo fue entregado y se encuentra actualmente en poder de un solicitante. |
| MANTENIMIENTO | El equipo no puede ser solicitado ni prestado.                                 |

Una reserva futura aprobada no cambia inmediatamente el equipo a PRESTADO. El cambio a `PRESTADO` ocurre solamente cuando se registra la entrega.

Al registrarse la devolución, el equipo pasa nuevamente a `DISPONIBLE`, salvo que haya sido cambiado explícitamente a `MANTENIMIENTO`.

---

## 7.5 Cálculo de disponibilidad

La disponibilidad deberá calcularse para el período completo solicitado y no únicamente a partir del estado actual del equipo.

Un equipo se considerará disponible para un período si:

1. no se encuentra en estado `MANTENIMIENTO`
2. no existe otro préstamo `APROBADO` o `ENTREGADO` cuyo período se superponga con el solicitado
3. cumple las demás reglas de negocio aplicables.

Las solicitudes en estado `SOLICITADA` no bloquearán automáticamente el equipo. Por lo tanto, podrán existir dos solicitudes pendientes para un mismo equipo y período, pero una vez que una sea aprobada, cualquier otra solicitud incompatible deberá ser rechazada al intentar aprobarse.

Los préstamos `RECHAZADOS`, `CANCELADOS` y `DEVUELTOS` no bloquean períodos futuros.

---

## 7.6 Regla de solapamiento

Dos períodos se consideran superpuestos cuando comparten al menos parte del intervalo de préstamo.

Por ejemplo:

- Préstamo A: 10/09 al 11/09
- Préstamo B: 11/09 al 12/09

Se considerarán incompatibles si el equipo todavía debe permanecer prestado durante el día 11/09.

La implementación deberá utilizar un único criterio de inclusión de fechas para evitar diferencias entre el cálculo de disponibilidad y las pruebas.

---

## 7.7 Diagrama

```text
                     ┌─────────────┐
                     │  RECHAZADA  │
                     └──────▲──────┘
                            │
                            │
┌─────────────┐      ┌──────┴──────┐
│  CANCELADA  │◄─────│  SOLICITADA │
└─────────────┘      └──────┬──────┘
                            │
                            ▼
                     ┌─────────────┐
              ┌──────│  APROBADA   │
              │      └──────┬──────┘
              │             │
              ▼             ▼
       ┌─────────────┐ ┌─────────────┐
       │  CANCELADA  │ │  ENTREGADA  │
       └─────────────┘ └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │  DEVUELTA   │
                       └─────────────┘
```

# 8. Requisitos funcionales y no funcionales

## 8.1 Requisitos funcionales

### RF-01 — Inicio de sesión

El sistema deberá permitir que un usuario registrado inicie sesión mediante correo electrónico y contraseña.

Criterios asociados: CA-01, CA-02.

---

### RF-02 — Control de acceso por rol

El sistema deberá mostrar y permitir únicamente las operaciones correspondientes al rol del usuario autenticado.

Los roles considerados serán:

- Solicitante.
- Encargado.

Un Solicitante no podrá ejecutar operaciones exclusivas de un Encargado.

---

### RF-03 — Gestión de usuarios

El Encargado deberá poder:

- registrar usuarios
- consultar usuarios
- modificar usuarios
- deshabilitar usuarios.

Cada usuario deberá contener:

- ID
- nombre
- correo
- contraseña
- rol.

---

### RF-04 — Gestión de equipos

El Encargado deberá poder:

- registrar equipos
- consultar equipos
- modificar sus datos
- cambiar su estado.

Cada equipo deberá contener:

- ID
- nombre
- categoría
- descripción
- estado.

Los estados posibles serán:

- DISPONIBLE
- PRESTADO
- MANTENIMIENTO.

---

### RF-05 — Consulta de equipos

Un Solicitante deberá poder consultar los equipos registrados y visualizar:

- datos básicos del equipo
- estado actual
- disponibilidad para un período determinado.

---

### RF-06 — Crear solicitud de préstamo

Un Solicitante autenticado deberá poder crear una solicitud para uno o más equipos indicando:

- equipos solicitados
- fecha de inicio
- fecha de devolución.

La solicitud solo podrá registrarse si cumple las reglas de negocio correspondientes.

Reglas relacionadas: RN-01, RN-02, RN-03, RN-05, RN-06 y RN-11.

Criterios asociados: CA-03, CA-04, CA-05, CA-07 y CA-08.

---

### RF-07 — Consultar solicitudes propias

Un Solicitante deberá poder consultar sus solicitudes y visualizar al menos:

- ID
- equipos asociados
- fechas
- estado actual.

---

### RF-08 — Cancelar solicitud

Un Solicitante deberá poder cancelar una solicitud propia únicamente cuando se encuentre en estado `SOLICITADA` o `APROBADA` y la entrega no haya sido registrada.

Regla relacionada: RN-10.

Criterio asociado: CA-11.

---

### RF-09 — Consultar solicitudes pendientes

El Encargado deberá poder consultar las solicitudes que se encuentren pendientes de revisión.

---

### RF-10 — Aprobar solicitud

El Encargado deberá poder aprobar una solicitud en estado `SOLICITADA`.

Antes de aprobarla, el sistema deberá volver a verificar:

- disponibilidad de los equipos
- ausencia de solapamientos
- estado del usuario
- cumplimiento de las reglas de negocio.

Si alguna condición ya no se cumple, la aprobación deberá ser rechazada.

Reglas relacionadas: RN-04, RN-05, RN-06 y RN-07.

Criterio asociado: CA-06.

---

### RF-11 — Rechazar solicitud

El Encargado deberá poder rechazar una solicitud que se encuentre en estado `SOLICITADA`.

Al rechazarla, la solicitud deberá cambiar a estado `RECHAZADA`.

---

### RF-12 — Registrar entrega

El Encargado deberá poder registrar la entrega de los equipos asociados a una solicitud previamente aprobada.

Al registrar la entrega:

- la solicitud deberá cambiar a `ENTREGADA`
- los equipos asociados deberán cambiar a `PRESTADO`.

Regla relacionada: RN-08.

Criterio asociado: CA-09.

---

### RF-13 — Registrar devolución

El Encargado deberá poder registrar la devolución de un préstamo en estado `ENTREGADA`.

Al registrar la devolución:

- la solicitud deberá cambiar a `DEVUELTA`
- los equipos deberán volver a estar disponibles, salvo que hayan sido puestos en mantenimiento.

Regla relacionada: RN-09.

Criterio asociado: CA-10.

---

### RF-14 — Consultar préstamos vigentes

El sistema deberá permitir al Encargado consultar los préstamos que actualmente se encuentran en estado `ENTREGADA` y cuya fecha de devolución aún no ha vencido.

---

### RF-15 — Consultar préstamos futuros

El sistema deberá permitir al Encargado consultar solicitudes aprobadas cuya fecha de inicio sea posterior a la fecha actual.

---

### RF-16 — Consultar préstamos atrasados

El sistema deberá permitir al Encargado consultar los préstamos cuyo estado sea `ENTREGADA` y cuya fecha comprometida de devolución ya haya vencido.

Regla relacionada: RN-12.

---

### RF-17 — Verificar disponibilidad

El sistema deberá determinar la disponibilidad de cada equipo considerando:

- estado del equipo
- reservas aprobadas
- préstamos entregados
- fechas solicitadas
- posibles solapamientos.

Las solicitudes únicamente en estado `SOLICITADA` no bloquearán automáticamente la disponibilidad.

---

### RF-18 — Persistencia de datos

El sistema deberá almacenar localmente los datos necesarios para mantener la información entre ejecuciones.

Como mínimo deberán persistirse:

- usuarios
- equipos
- solicitudes y préstamos.

Criterio asociado: CA-12.

---

### RF-19 — Registro de eventos

El sistema deberá registrar mediante logs eventos relevantes, incluyendo al menos:

- inicios de sesión exitosos
- intentos de acceso fallidos
- creación de solicitudes
- aprobaciones
- rechazos
- cancelaciones
- entregas
- devoluciones
- errores relevantes.

---

### RF-20 — Manejo de errores

El sistema deberá detectar entradas y operaciones inválidas y mostrar un mensaje comprensible sin finalizar abruptamente la aplicación.

---

## 8.2 Requisitos no funcionales

### RNF-01 — Aplicación de línea de comandos

La aplicación deberá poder utilizarse completamente desde una interfaz de línea de comandos.

---

### RNF-02 — Facilidad de ejecución

La aplicación deberá poder instalarse y ejecutarse siguiendo únicamente las instrucciones documentadas en el archivo `README.md`.

---

### RNF-03 — Tecnología

La implementación será desarrollada en Python.

---

### RNF-04 — Persistencia local

La persistencia deberá implementarse localmente sin requerir una base de datos remota o servicio externo para el funcionamiento principal.

---

### RNF-05 — Confiabilidad

Una operación inválida no deberá dejar los datos almacenados en un estado inconsistente.

Por ejemplo, si una aprobación falla por falta de disponibilidad, la solicitud deberá conservar su estado anterior.

---

### RNF-06 — Trazabilidad

Los requisitos, reglas de negocio, criterios de aceptación y casos de prueba deberán utilizar identificadores consistentes en:

- documentación
- código cuando corresponda
- matriz de trazabilidad
- casos de prueba
- Issues.

---

### RNF-07 — Registro de errores

Los errores relevantes deberán registrarse localmente mediante logs y, cuando corresponda, reportarse mediante Sentry.

---

### RNF-08 — Seguridad básica

Las contraseñas, tokens y credenciales de servicios externos no deberán almacenarse directamente en el repositorio.

Los datos sensibles de configuración deberán manejarse mediante variables de entorno.

---

### RNF-09 — Mantenibilidad

El código deberá organizarse separando las principales responsabilidades del sistema, evitando concentrar toda la lógica en un único archivo.

---

### RNF-10 — Testabilidad

Las reglas de negocio deberán implementarse de forma que puedan ser probadas de manera independiente mediante pruebas automatizadas o casos de prueba reproducibles.

---

## 8.3 Resumen de trazabilidad inicial

| Requisito | Reglas / criterios principales                                               |
| --------- | ---------------------------------------------------------------------------- |
| RF-01     | CA-01, CA-02                                                                 |
| RF-06     | RN-01, RN-02, RN-03, RN-05, RN-06, RN-11 / CA-03, CA-04, CA-05, CA-07, CA-08 |
| RF-08     | RN-10 / CA-11                                                                |
| RF-10     | RN-04, RN-05, RN-06, RN-07 / CA-06                                           |
| RF-12     | RN-08 / CA-09                                                                |
| RF-13     | RN-09 / CA-10                                                                |
| RF-16     | RN-12                                                                        |
| RF-17     | RN-04, RN-06                                                                 |
| RF-18     | CA-12                                                                        |
| RF-19     | RNF-07                                                                       |

# 9. Matriz de trazabilidad

La matriz permite relacionar los requisitos definidos con sus criterios de aceptación, implementación y casos de prueba. Los campos de evidencia y resultado se completarán una vez implementado y probado el sistema.

| ID requisito | Criterio de aceptación / regla                                                                            | Evidencia de implementación | Caso(s) de prueba                 | Resultado |
| ------------ | --------------------------------------------------------------------------------------------------------- | --------------------------- | --------------------------------- | --------- |
| RF-01        | CA-01: credenciales válidas permiten iniciar sesión. CA-02: credenciales inválidas son rechazadas.        | Pendiente                   | TC-01, TC-02                      | Pendiente |
| RF-02        | Solo se permiten operaciones correspondientes al rol autenticado.                                         | Pendiente                   | TC-03                             | Pendiente |
| RF-04        | El encargado puede registrar y modificar equipos y sus estados.                                           | Pendiente                   | TC-04                             | Pendiente |
| RF-06        | CA-03, CA-04, CA-05, CA-07 y CA-08. La solicitud debe cumplir RN-01, RN-02, RN-03, RN-05, RN-06 y RN-11.  | Pendiente                   | TC-05, TC-06, TC-07, TC-08, TC-09 | Pendiente |
| RF-08        | CA-11 / RN-10: solo pueden cancelarse solicitudes SOLICITADAS o APROBADAS antes de la entrega.            | Pendiente                   | TC-10                             | Pendiente |
| RF-10        | CA-06 / RN-04: no se puede aprobar una solicitud si existe un préstamo incompatible para el mismo equipo. | Pendiente                   | TC-11                             | Pendiente |
| RF-12        | CA-09 / RN-08: solo una solicitud APROBADA puede pasar a ENTREGADA.                                       | Pendiente                   | TC-12                             | Pendiente |
| RF-13        | CA-10 / RN-09: solo un préstamo ENTREGADO puede pasar a DEVUELTO.                                         | Pendiente                   | TC-13                             | Pendiente |
| RF-16        | RN-12: un préstamo entregado cuya fecha de devolución venció debe identificarse como atrasado.            | Pendiente                   | TC-14                             | Pendiente |
| RF-17        | RN-04 y RN-06: la disponibilidad debe considerar estado, período y reservas aprobadas.                    | Pendiente                   | TC-11, TC-15                      | Pendiente |
| RF-18        | CA-12: los datos deben mantenerse luego de cerrar y volver a ejecutar la aplicación.                      | Pendiente                   | TC-16                             | Pendiente |
| RF-19        | Los eventos relevantes deben quedar registrados mediante logs.                                            | Pendiente                   | TC-17                             | Pendiente |
| RF-20        | Las entradas u operaciones inválidas deben ser rechazadas sin cerrar inesperadamente el programa.         | Pendiente                   | TC-18                             | Pendiente |
| RNF-02       | La aplicación puede instalarse y ejecutarse siguiendo únicamente el README.                               | Pendiente                   | TC-19                             | Pendiente |
| RNF-05       | Una operación fallida no debe dejar información en un estado inconsistente.                               | Pendiente                   | TC-20                             | Pendiente |

## 9.1 Forma de completar la matriz

Una vez implementado el sistema, la columna Evidencia de implementación deberá indicar elementos concretos, por ejemplo:

- archivo
- clase
- función
- módulo
- Pull Request o commit asociado.

Ejemplo:

| ID requisito | Evidencia de implementación                                 |
| ------------ | ----------------------------------------------------------- |
| RF-01        | `src/services/auth_service.py`, función `login()`           |
| RF-10        | `src/services/loan_service.py`, función `approve_request()` |
| RF-18        | `src/repositories/json_repository.py`                       |

La columna Resultado deberá completarse únicamente después de ejecutar los casos correspondientes, indicando al menos:

- `PASS`, si el comportamiento obtenido coincide con el esperado
- `FAIL`, si existe una diferencia
- referencia al Issue correspondiente cuando se detecte un defecto.

Ejemplo:

`FAIL — Issue #12: se permite aprobar reserva superpuesta`

Después de corregir y reejecutar:

`PASS — reejecutado en Ciclo 2`

# 10. Estrategia de pruebas

## 10.1 Objetivo

La estrategia de pruebas busca comprobar que el sistema de préstamo de equipos cumple los requisitos funcionales, reglas de negocio y criterios de aceptación definidos.

Las pruebas estarán orientadas principalmente a:

- comprobar el flujo completo de solicitudes y préstamos
- validar límites y reglas de negocio
- detectar entradas inválidas
- verificar transiciones de estado
- comprobar disponibilidad y solapamientos
- verificar persistencia
- comprobar manejo de errores
- comprobar que los datos no queden inconsistentes después de una operación fallida.

---

## 10.2 Alcance

Se probarán las siguientes funcionalidades:

- inicio de sesión
- control de acceso según rol
- gestión de equipos
- creación de solicitudes
- límite de equipos activos
- duración máxima del préstamo
- anticipación máxima
- usuarios con préstamos atrasados
- equipos en mantenimiento
- aprobación y rechazo
- detección de solapamientos
- cancelaciones
- entregas
- devoluciones
- detección de atrasos
- persistencia
- logs
- manejo de entradas inválidas.

Quedan fuera del alcance las funcionalidades declaradas previamente como exclusiones del proyecto.

---

## 10.3 Ambiente de pruebas

Las pruebas serán ejecutadas localmente sobre la versión del proyecto almacenada en GitHub.

Ambiente previsto:

- Sistema operativo: Windows.
- Lenguaje: Python.
- Interfaz: línea de comandos.
- Persistencia: archivos locales.
- Framework de pruebas automatizadas: `pytest`.
- Registro de errores: `logging` y Sentry.
- Repositorio: GitHub.

La versión exacta de Python deberá registrarse en el `README.md` y en la evidencia de ejecución.

---

## 10.4 Datos de prueba

Se utilizarán datos de demostración controlados para permitir la reproducción de los casos.

### Usuarios iniciales

| ID   | Nombre            | Correo                                            | Rol         | Condición             |
| ---- | ----------------- | ------------------------------------------------- | ----------- | --------------------- |
| U-01 | Ana Solicitante   | [ana@fablab.cl](mailto:ana@fablab.cl)             | SOLICITANTE | Sin préstamos         |
| U-02 | Pedro Solicitante | [pedro@fablab.cl](mailto:pedro@fablab.cl)         | SOLICITANTE | Con préstamo atrasado |
| U-03 | Elena Encargada   | [encargada@fablab.cl](mailto:encargada@fablab.cl) | ENCARGADO   | Usuario administrador |

### Equipos iniciales

| ID    | Nombre       | Estado        |
| ----- | ------------ | ------------- |
| EQ-01 | Cámara Canon | DISPONIBLE    |
| EQ-02 | Trípode      | DISPONIBLE    |
| EQ-03 | Micrófono    | DISPONIBLE    |
| EQ-04 | Notebook     | MANTENIMIENTO |
| EQ-05 | Grabadora    | DISPONIBLE    |

Los datos podrán ampliarse según las necesidades específicas de las pruebas.

---

## 10.5 Criterios de entrada

Una ronda de pruebas podrá comenzar cuando:

- la funcionalidad correspondiente esté implementada
- el proyecto pueda ejecutarse sin errores de instalación
- existan datos de prueba definidos
- los requisitos y reglas asociados estén documentados
- se conozca la versión de la aplicación que será probada.

---

## 10.6 Criterios de salida

Un ciclo de pruebas se considerará finalizado cuando:

- todos los casos planificados hayan sido ejecutados
- cada caso tenga resultado obtenido y evidencia
- los defectos encontrados estén registrados como Issues
- los defectos corregidos hayan sido reejecutados
- no existan defectos críticos conocidos sin documentar.

---

## 10.7 Registro de resultados

Cada caso deberá registrar:

- ID del caso
- requisitos asociados
- categoría
- precondiciones
- entrada o pasos
- resultado esperado
- resultado obtenido
- PASS o FAIL
- fecha y hora
- versión probada
- evidencia
- observaciones.

Los resultados de ejecución se registrarán en la planilla entregada para la tarea.

---

# 11. Diseño de casos de prueba

## TC-01 — Inicio de sesión correcto

Categoría: Funcional
Requisito: RF-01 / CA-01

Precondición: Existe un usuario registrado.

Entrada:

- correo válido
- contraseña correcta.

Resultado esperado:
El sistema autentica al usuario y muestra el menú correspondiente a su rol.

---

## TC-02 — Contraseña incorrecta

Categoría: Negativo
Requisito: RF-01 / CA-02

Entrada:

- correo válido
- contraseña incorrecta.

Resultado esperado:
El acceso es rechazado y el programa continúa funcionando.

---

## TC-03 — Solicitante intenta realizar operación de Encargado

Categoría: Negativo / Funcional
Requisito: RF-02

Precondición: Usuario autenticado con rol SOLICITANTE.

Acción:
Intenta acceder a una operación exclusiva del Encargado.

Resultado esperado:
La operación es rechazada.

---

## TC-04 — Registrar un equipo

Categoría: Funcional
Requisito: RF-04

Precondición: Encargado autenticado.

Entrada:
Datos válidos de un nuevo equipo.

Resultado esperado:
El equipo queda registrado y puede consultarse posteriormente.

---

## TC-05 — Crear solicitud válida

Categoría: Funcional
Requisito: RF-06 / CA-03

Precondición:

- solicitante sin atrasos
- equipo disponible
- período válido.

Resultado esperado:
Se crea una solicitud en estado `SOLICITADA`.

---

## TC-06 — Solicitar exactamente 3 equipos

Categoría: Borde
Requisito: RF-06 / RN-01

Precondición:
El usuario no posee otros equipos activos.

Entrada:
Solicitud con exactamente 3 equipos disponibles.

Resultado esperado:
La solicitud es aceptada.

---

## TC-07 — Intentar superar el máximo de 3 equipos

Categoría: Borde / Negativo
Requisito: RF-06 / RN-01 / CA-04

Precondición:
El usuario ya tiene 3 equipos asociados a préstamos activos.

Acción:
Intenta solicitar un equipo adicional.

Resultado esperado:
La solicitud es rechazada.

---

## TC-08 — Solicitud exactamente por 2 días hábiles

Categoría: Borde
Requisito: RF-06 / RN-02

Entrada:
Período cuya duración corresponde exactamente a 2 días hábiles.

Resultado esperado:
La solicitud es aceptada si cumple las demás reglas.

---

## TC-09 — Solicitud superior a 2 días hábiles

Categoría: Borde / Negativo
Requisito: RF-06 / RN-02 / CA-07

Entrada:
Período superior a 2 días hábiles.

Resultado esperado:
El sistema rechaza la solicitud.

---

## TC-10 — Fecha de devolución anterior a fecha de inicio

Categoría: Negativo
Requisito: RF-06 / RN-11

Entrada:

- inicio: 15/09
- devolución: 14/09.

Resultado esperado:
La solicitud es rechazada y se informa que el período es inválido.

---

## TC-11 — Usuario con préstamo atrasado intenta solicitar

Categoría: Negativo / Regla combinada
Requisito: RF-06 / RN-05 / CA-05

Precondición:
El usuario posee un préstamo `ENTREGADO` con fecha de devolución vencida.

Resultado esperado:
No se permite crear una nueva solicitud.

---

## TC-12 — Equipo en mantenimiento

Categoría: Negativo
Requisito: RF-06 / RN-06 / CA-08

Precondición:
EQ-04 se encuentra en `MANTENIMIENTO`.

Acción:
El usuario intenta solicitarlo.

Resultado esperado:
La solicitud es rechazada.

---

## TC-13 — Aprobar solicitud válida

Categoría: Funcional
Requisito: RF-10

Precondición:
Existe una solicitud `SOLICITADA` que cumple todas las reglas.

Resultado esperado:
La solicitud cambia a `APROBADA`.

---

## TC-14 — Aprobar dos solicitudes superpuestas

Categoría: Regla combinada / Borde
Requisito: RF-10 / RF-17 / RN-04 / CA-06

Precondición:
Existen dos solicitudes para el mismo equipo con períodos superpuestos.

Acciones:

1. aprobar la primera
2. intentar aprobar la segunda.

Resultado esperado:
La primera queda aprobada y la segunda no puede aprobarse debido al conflicto.

---

## TC-15 — Cancelar solicitud aprobada antes de la entrega

Categoría: Funcional
Requisito: RF-08 / RN-10 / CA-11

Precondición:
Solicitud en estado `APROBADA`.

Resultado esperado:
La solicitud cambia a `CANCELADA`.

---

## TC-16 — Intentar cancelar después de la entrega

Categoría: Negativo / Regla combinada
Requisito: RF-08 / RN-10

Precondición:
Préstamo en estado `ENTREGADA`.

Acción:
Se intenta cancelar.

Resultado esperado:
El sistema rechaza la transición y mantiene el estado `ENTREGADA`.

---

## TC-17 — Registrar entrega

Categoría: Funcional
Requisito: RF-12 / RN-08 / CA-09

Precondición:
Solicitud en estado `APROBADA`.

Resultado esperado:

- la solicitud pasa a `ENTREGADA`
- los equipos pasan a `PRESTADO`.

---

## TC-18 — Registrar devolución

Categoría: Funcional
Requisito: RF-13 / RN-09 / CA-10

Precondición:
Préstamo en estado `ENTREGADA`.

Resultado esperado:

- préstamo pasa a `DEVUELTA`
- los equipos vuelven a estar disponibles.

---

## TC-19 — Persistencia después de reiniciar

Categoría: Funcional
Requisito: RF-18 / CA-12

Pasos:

1. registrar información
2. cerrar la aplicación
3. volver a ejecutarla
4. consultar la información registrada.

Resultado esperado:
Los datos permanecen disponibles.

---

## TC-20 — Flujo completo del préstamo

Categoría: Escenario completo
Requisitos: RF-05, RF-06, RF-09, RF-10, RF-12, RF-13, RF-17 y RF-18

Pasos:

1. Solicitante inicia sesión.
2. Consulta equipos.
3. Selecciona un equipo disponible.
4. Crea una solicitud válida.
5. Encargado inicia sesión.
6. Consulta las solicitudes pendientes.
7. Aprueba la solicitud.
8. Registra la entrega.
9. Se comprueba que el préstamo aparece vigente.
10. Registra la devolución.
11. Se comprueba que la solicitud queda `DEVUELTA`.
12. Se verifica que el equipo vuelve a estar disponible.

Resultado esperado:
El ciclo completo termina correctamente sin inconsistencias.

---

# 11.1 Cobertura mínima exigida

La suite diseñada contiene:

| Categoría requerida   | Mínimo solicitado | Casos incluidos                                        |
| --------------------- | ----------------: | ------------------------------------------------------ |
| Funcionales           |                 5 | TC-01, TC-04, TC-05, TC-13, TC-15, TC-17, TC-18, TC-19 |
| Borde                 |                 4 | TC-06, TC-07, TC-08, TC-09, TC-14                      |
| Negativos / inválidos |                 3 | TC-02, TC-03, TC-07, TC-09, TC-10, TC-11, TC-12, TC-16 |
| Combinación de reglas |                 2 | TC-11, TC-14, TC-16                                    |
| Escenario completo    |                 1 | TC-20                                                  |

Por lo tanto, la estrategia supera los mínimos establecidos para la tarea.

# 12. Diseño general y arquitectura

## 12.1 Enfoque de arquitectura

La aplicación se implementará en Python utilizando una arquitectura simple separada por responsabilidades.

Se dividirá en cuatro áreas principales:

- Modelos: representan usuarios, equipos y solicitudes.
- Servicios: contienen las reglas de negocio y operaciones principales.
- Persistencia: administra la lectura y escritura de datos locales.
- Interfaz CLI: permite interactuar con el sistema mediante línea de comandos.

La lógica de negocio no se implementará directamente en el menú principal, con el objetivo de facilitar las pruebas y mantener el código organizado.

---

## 12.2 Estructura propuesta

```text
PruebasdeSoftware/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── equipment.py
│   │   └── loan.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── equipment_service.py
│   │   └── loan_service.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── json_repository.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── date_utils.py
│       └── logger.py
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_equipment.py
│   └── test_loans.py
│
├── data/
│   ├── users.json
│   ├── equipment.json
│   └── loans.json
│
├── docs/
│   └── requerimientos.md
│
├── logs/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 12.3 Responsabilidad de cada componente

## `main.py`

Será el punto de entrada de la aplicación.

Sus responsabilidades serán:

- iniciar el sistema
- cargar los datos
- mostrar los menús
- solicitar información al usuario
- llamar a los servicios correspondientes
- mostrar resultados y mensajes.

No deberá contener directamente las reglas de negocio.

---

## `models/user.py`

Representará a un usuario.

Cada usuario tendrá:

- ID
- nombre
- correo
- contraseña
- rol
- estado habilitado/deshabilitado.

Roles:

```text
SOLICITANTE
ENCARGADO
```

---

## `models/equipment.py`

Representará un equipo tecnológico.

Cada equipo tendrá:

- ID
- nombre
- categoría
- descripción
- estado.

Estados:

```text
DISPONIBLE
PRESTADO
MANTENIMIENTO
```

---

## `models/loan.py`

Representará una solicitud o préstamo.

Cada registro contendrá:

- ID
- ID del solicitante
- IDs de los equipos
- fecha de inicio
- fecha de devolución
- estado
- fecha de creación.

Estados:

```text
SOLICITADA
APROBADA
RECHAZADA
ENTREGADA
DEVUELTA
CANCELADA
```

---

# 12.4 Servicios

## `auth_service.py`

Responsable de:

- validar correo y contraseña
- autenticar usuarios
- identificar el rol
- rechazar usuarios inválidos o deshabilitados.

Relacionado con:

- RF-01
- RF-02
- CA-01
- CA-02.

---

## `user_service.py`

Responsable de:

- registrar usuarios
- consultar usuarios
- modificar usuarios
- habilitar o deshabilitar usuarios.

Relacionado con:

- RF-03.

---

## `equipment_service.py`

Responsable de:

- registrar equipos
- modificar equipos
- consultar equipos
- cambiar su estado
- consultar disponibilidad básica.

Relacionado con:

- RF-04
- RF-05.

---

## `loan_service.py`

Será el componente principal de lógica de negocio.

Responsable de:

- crear solicitudes
- comprobar límite de equipos
- comprobar duración
- comprobar anticipación
- validar fechas
- detectar atrasos
- verificar disponibilidad
- detectar solapamientos
- aprobar solicitudes
- rechazar solicitudes
- cancelar solicitudes
- registrar entregas
- registrar devoluciones
- consultar préstamos vigentes, futuros y atrasados.

Aquí se implementarán principalmente:

```text
RN-01 a RN-12
```

---

# 12.5 Persistencia

## `json_repository.py`

Se utilizarán archivos JSON como mecanismo de persistencia local.

El repositorio será responsable de:

- cargar información desde archivos
- guardar información
- crear archivos si no existen
- manejar errores de lectura
- evitar pérdida de información ante operaciones inválidas.

Archivos previstos:

```text
data/users.json
data/equipment.json
data/loans.json
```

La lógica de negocio no deberá conocer los detalles de cómo se guardan físicamente los datos.

---

# 12.6 Utilidades

## `date_utils.py`

Contendrá operaciones relacionadas con fechas, especialmente:

- validación de fechas
- cálculo de días hábiles
- comprobación del máximo de 2 días hábiles
- comprobación de los 30 días máximos de anticipación
- detección de períodos superpuestos
- detección de préstamos atrasados.

Esto permite centralizar una de las partes más sensibles del proyecto.

---

## `logger.py`

Configurará el sistema de logs.

Se registrarán eventos como:

- login exitoso
- login fallido
- creación de solicitud
- aprobación
- rechazo
- cancelación
- entrega
- devolución
- errores inesperados.

Los errores relevantes también podrán enviarse a Sentry.

---

# 12.7 Dependencias entre componentes

El flujo general será:

```text
Usuario
   ↓
main.py
   ↓
Services
   ↓
Models + reglas de negocio
   ↓
Repository
   ↓
Archivos JSON
```

Por ejemplo, al crear una solicitud:

```text
main.py
   ↓
loan_service.create_request()
   ↓
validar usuario
validar fechas
validar límite
validar disponibilidad
validar atraso
   ↓
crear Loan
   ↓
json_repository.save()
```

---

# 12.8 Principio para manejo de errores

Las operaciones deberán validarse antes de modificar los datos persistidos.

Por ejemplo:

```text
Intentar aprobar solicitud
        ↓
¿Estado = SOLICITADA?
        ↓
¿Usuario habilitado?
        ↓
¿Equipos disponibles?
        ↓
¿Existe solapamiento?
        ↓
¿Cumple reglas?
        ↓
Sí → guardar cambio a APROBADA

No → rechazar operación
     mantener estado anterior
```

Esto permitirá cumplir el requisito RNF-05 relacionado con consistencia de datos.

---

# 12.9 Estrategia de pruebas del código

Las pruebas automatizadas se concentrarán principalmente en los servicios.

Por ejemplo:

```text
tests/test_auth.py
→ login válido
→ login inválido
→ permisos por rol
```

```text
tests/test_equipment.py
→ creación de equipo
→ mantenimiento
→ disponibilidad
```

```text
tests/test_loans.py
→ máximo de equipos
→ duración máxima
→ fechas inválidas
→ atrasos
→ solapamientos
→ aprobación
→ cancelación
→ entrega
→ devolución
```

De esta forma, las reglas de negocio pueden probarse sin tener que interactuar manualmente con todo el menú de la aplicación.
