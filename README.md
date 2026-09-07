# Pruebas de Software - Tarea 1

Sistema de gestión de préstamos de equipos tecnológicos para un FabLab universitario, desarrollado como parte de la Tarea 1 de Verificación y Validación.

La aplicación permite gestionar usuarios, equipos, solicitudes de préstamo, aprobaciones, entregas, devoluciones y cancelaciones mediante una interfaz de línea de comandos.

## Tecnologías utilizadas

- Python 3.14
- pytest
- JSON para persistencia local
- Python Logging
- Sentry
- python-dotenv
- Git y GitHub

## Requisitos

- Python 3.14 o compatible
- Git
- pip

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/BeatrizJVC/PruebasdeSoftware.git
cd PruebasdeSoftware
```

## Crear entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Instalar dependencias

Con el entorno virtual activado:

```powershell
python -m pip install -r requirements.txt
```

## Configuración de Sentry

La aplicación puede ejecutarse sin Sentry, pero para habilitar el monitoreo de errores se debe crear un archivo `.env` en la raíz del proyecto.

Usar `.env.example` como referencia:

```env
SENTRY_DSN=
SENTRY_ENVIRONMENT=development
```

El valor real de `SENTRY_DSN` no debe almacenarse en el repositorio.

## Ejecución

Desde la raíz del proyecto:

```powershell
python -m src.main
```

La primera ejecución genera automáticamente los archivos necesarios de persistencia y carga los datos de demostración.

## Usuarios de demostración

### Solicitante

```text
Correo: ana@fablab.cl
Contraseña: 1234
```

### Encargado

```text
Correo: encargada@fablab.cl
Contraseña: admin123
```

## Funcionalidades

### Solicitante

- iniciar sesión
- consultar equipos y su estado
- crear solicitudes de préstamo
- consultar solicitudes propias
- cancelar solicitudes permitidas

### Encargado

- consultar usuarios
- habilitar y deshabilitar usuarios
- registrar equipos
- consultar equipos
- cambiar el estado de equipos
- consultar solicitudes pendientes
- aprobar solicitudes
- rechazar solicitudes
- registrar entregas
- registrar devoluciones
- consultar préstamos vigentes
- consultar préstamos futuros
- consultar préstamos atrasados

## Reglas principales de negocio

- un solicitante puede mantener como máximo 3 equipos asociados a préstamos activos
- la duración máxima de un préstamo es de 2 días hábiles
- las reservas pueden realizarse con hasta 30 días de anticipación
- un mismo equipo no puede ser asignado a préstamos cuyos períodos se superpongan
- un usuario con préstamos atrasados no puede crear nuevas solicitudes
- un equipo en mantenimiento no puede ser solicitado
- solo un Encargado puede aprobar o rechazar solicitudes
- solo un Encargado puede registrar entregas y devoluciones
- una solicitud solo puede cancelarse antes de que la entrega haya sido registrada

Los días hábiles corresponden a lunes a viernes. No se consideran feriados.

## Estados de una solicitud o préstamo

El flujo principal de estados es:

```text
SOLICITADA
   ├── APROBADA
   │      ├── ENTREGADA
   │      │      └── DEVUELTA
   │      └── CANCELADA
   ├── RECHAZADA
   └── CANCELADA
```

Los estados `RECHAZADA`, `CANCELADA` y `DEVUELTA` se consideran estados finales.

El atraso no corresponde a un estado independiente. Un préstamo se considera atrasado cuando permanece en estado `ENTREGADA` después de superar su fecha comprometida de devolución.

## Estados de los equipos

Los equipos pueden encontrarse en los siguientes estados:

- `DISPONIBLE`
- `PRESTADO`
- `MANTENIMIENTO`

Un equipo cambia a `PRESTADO` únicamente cuando se registra la entrega de una solicitud aprobada.

Al registrar la devolución, el equipo vuelve a `DISPONIBLE`.

## Persistencia

La información se almacena localmente mediante archivos JSON dentro de la carpeta:

```text
data/
```

Se mantienen datos de:

- usuarios
- equipos
- solicitudes y préstamos

Los archivos JSON se generan durante la ejecución y no se versionan en Git.

## Logs

Los eventos relevantes de la aplicación quedan registrados en:

```text
logs/app.log
```

Entre los eventos registrados se encuentran:

- inicio de la aplicación
- cierre de la aplicación
- inicio de sesión exitoso
- intentos de inicio de sesión fallidos
- creación de solicitudes
- aprobaciones
- rechazos
- cancelaciones
- entregas
- devoluciones
- errores inesperados

Los archivos de logs generados durante la ejecución no se versionan en Git.

## Monitoreo de errores con Sentry

La aplicación integra Sentry para registrar errores inesperados.

Si `SENTRY_DSN` está configurado en el archivo `.env`, los errores no controlados podrán ser enviados al proyecto configurado en Sentry.

La aplicación puede ejecutarse normalmente aunque Sentry no esté configurado.

## Ejecución de pruebas automatizadas

Desde la raíz del proyecto:

```powershell
python -m pytest -v
```

La suite automatizada incluye pruebas sobre:

- autenticación
- control de roles
- gestión de usuarios
- gestión de equipos
- reglas relacionadas con fechas
- duración máxima de préstamos
- anticipación máxima
- solapamiento de períodos
- préstamos atrasados
- creación de solicitudes
- aprobación y rechazo
- cancelación
- entrega
- devolución
- persistencia

## Estructura del proyecto

```text
PruebasdeSoftware/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   ├── equipment.py
│   │   └── loan.py
│   ├── repositories/
│   │   └── json_repository.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── equipment_service.py
│   │   └── loan_service.py
│   ├── utils/
│   │   ├── date_utils.py
│   │   └── logger.py
│   ├── bootstrap.py
│   ├── main.py
│   └── seed_demo.py
├── tests/
├── docs/
├── data/
├── logs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Documentación

La documentación asociada al análisis y verificación del proyecto se encuentra en la carpeta `docs/`.

Esta documentación incluye:

- análisis del requerimiento
- ambigüedades detectadas
- supuestos y acuerdos
- requerimiento mejorado
- reglas de negocio
- alcance y exclusiones
- criterios de aceptación
- estados y transiciones
- requisitos funcionales y no funcionales
- matriz de trazabilidad
- estrategia de pruebas
- diseño de casos de prueba

## Datos de demostración

La aplicación incluye un proceso de carga inicial de datos mediante:

```text
src/seed_demo.py
```

Los datos de demostración permiten ejecutar y revisar el sistema sin necesidad de ingresar manualmente todos los usuarios y equipos desde cero.

## Autor

BeatrizJVC - Beatriz Vásquez Cea

## Licencia

Proyecto desarrollado con fines académicos para la asignatura Pruebas de Software - INF331 de la Universidad Técnica Federico Santa María.
