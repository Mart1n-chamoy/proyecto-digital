# Gestor de Documentos

Sistema web para almacenar y administrar contratos en PDF (documentos de empleados/parcelas), con búsqueda, control de permisos por usuario y auditoría de cambios.

## Requisitos

- Python 3.11+
- MySQL o MariaDB corriendo localmente

## Instalación

1. Instalar las dependencias:

   ```
   pip install -r requirements.txt
   ```

2. Copiar `.env.example` a `.env` y completar los valores (clave secreta, credenciales de la base de datos, etc.):

   ```
   cp .env.example .env
   ```

3. Crear la base de datos en MySQL (el nombre debe coincidir con `DB_NAME` en el `.env`):

   ```sql
   CREATE DATABASE gestor_documentos;
   ```

4. Aplicar las migraciones:

   ```
   python manage.py migrate
   ```

5. Levantar el servidor de desarrollo:

   ```
   python manage.py runserver
   ```

   La aplicación queda disponible en `http://127.0.0.1:8000/`.

## Usuarios

Todas las vistas requieren haber iniciado sesión (`/accounts/login/`). No hay registro público: las cuentas las crea un administrador.

### Crear un superusuario (administrador)

El superusuario tiene acceso total: puede crear, editar y eliminar documentos, ver el historial de auditoría, y administrar usuarios desde `/admin/`.

```
python manage.py createsuperuser
```

Va a pedir un nombre de usuario, un email (opcional) y una contraseña. Con esa cuenta ya se puede entrar tanto a la aplicación (`/`) como al panel de administración de Django (`/admin/`).

### Crear un usuario normal (empleado)

Los usuarios normales **no tienen ningún permiso por defecto**: pueden iniciar sesión y ver/buscar documentos, pero no pueden crear, editar ni eliminar nada, ni ver la auditoría, a menos que se les otorgue el permiso explícitamente.

Para crear uno:

1. Entrar a `/admin/` con una cuenta de superusuario.
2. Ir a **Autenticación y autorización → Usuarios → Agregar usuario**.
3. Completar usuario y contraseña. **No** tildar "Es staff" ni "Es superusuario" (así no puede entrar al panel de administración, solo a la aplicación).
4. Guardar. Con eso ya puede iniciar sesión y consultar documentos.

#### Dar permisos puntuales a un empleado

Si además de consultar necesita poder crear, editar o eliminar documentos:

1. En `/admin/`, abrir la ficha del usuario.
2. En la sección **Permisos de usuario**, buscar y agregar los que correspondan:
   - `gestor | documento | Can add documento` — puede cargar documentos nuevos.
   - `gestor | documento | Can change documento` — puede editar documentos.
   - `gestor | documento | Can delete documento` — puede eliminar documentos.
   - `gestor | registro auditoría | Can view registro auditoría` — puede ver el historial de auditoría.
3. Guardar.

Si varios empleados necesitan los mismos permisos, conviene crear un **Grupo** (por ejemplo "Editores") con esos permisos en **Autenticación y autorización → Grupos**, y luego asignar el grupo a cada usuario en vez de repetir los permisos uno por uno.

## Funcionalidades

- Búsqueda de documentos por nombre, apellido, DNI, número de contrato o parcela.
- Listado paginado (20 documentos por página).
- Validación de archivos: solo PDF, máximo 15 MB.
- Confirmación antes de eliminar un documento.
- Historial de auditoría: registra quién creó, editó o eliminó cada documento y cuándo (visible en "Auditoría" para quien tenga el permiso correspondiente).
