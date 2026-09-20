# Gestor de Documentos

Sistema web para almacenar y administrar contratos en PDF (documentos de empleados/parcelas), con búsqueda, control de permisos por usuario y auditoría de cambios.

## Requisitos

- Python 3.10+
- MariaDB 10.5+ o MySQL 8.0.11+ corriendo localmente (versiones más viejas no son compatibles con Django 5.2)

## Instalación en una VM/máquina Ubuntu desde cero

1. Clonar el repositorio y entrar a la carpeta:

   ```bash
   git clone <url-del-repo>
   cd proyecto-digital
   ```

2. Instalar y configurar MariaDB nativa (con `apt`, **no** con XAMPP/LAMPP — esas versiones embebidas suelen ser viejas y no cumplen el mínimo que pide Django):

   ```bash
   sudo apt update
   sudo apt install mariadb-server -y
   sudo systemctl enable --now mariadb
   ```

   Crear la base de datos y un usuario dedicado para la app (evitar usar `root`, que en Ubuntu no tiene contraseña y se autentica distinto):

   ```bash
   sudo mysql
   ```

   Dentro del prompt de `mysql`:

   ```sql
   CREATE DATABASE gestor_documentos CHARACTER SET utf8mb4;
   CREATE USER 'gestor_app'@'localhost' IDENTIFIED BY 'ELEGÍ-UNA-CONTRASEÑA-ACÁ';
   GRANT ALL PRIVILEGES ON gestor_documentos.* TO 'gestor_app'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. Crear y activar un entorno virtual. Los sistemas Linux modernos (Ubuntu 23.04+, Debian 12+) no dejan instalar paquetes con `pip` directamente sobre el Python del sistema («externally-managed-environment»), así que este paso es obligatorio:

   ```bash
   sudo apt install python3-venv python3-full -y   # una sola vez, Ubuntu/Debian
   python3 -m venv venv
   source venv/bin/activate
   ```

   En Windows sería `python -m venv venv` y luego `venv\Scripts\activate`.

   Con el entorno activado, la línea de comandos empieza con `(venv)`. Hay que activarlo de nuevo (`source venv/bin/activate`) cada vez que se abre una terminal nueva para trabajar en el proyecto.

4. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

5. Entrar a la carpeta del proyecto Django (donde está `manage.py`):

   ```bash
   cd proyecto
   ```

6. Copiar `.env.example` a `.env` y completar los valores: clave secreta, y las credenciales creadas en el paso 2 (`DB_NAME=gestor_documentos`, `DB_USER=gestor_app`, `DB_PASSWORD=` la contraseña elegida, `DB_HOST=localhost`, `DB_PORT=3306`):

   ```bash
   cp .env.example .env
   ```

7. Aplicar las migraciones:

   ```bash
   python manage.py migrate
   ```

8. Levantar el servidor de desarrollo:

   ```bash
   python manage.py runserver
   ```

   La aplicación queda disponible en `http://127.0.0.1:8000/`.

### (Opcional) phpMyAdmin, para administrar la base de datos con una interfaz visual

```bash
sudo apt install phpmyadmin
```

Durante la instalación:
- **"Web server to configure automatically"** → marcar `apache2` con la barra espaciadora y confirmar (instala Apache si hace falta).
- **"Configure database for phpmyadmin with dbconfig-common?"** → `Yes`.

Después, con Apache corriendo (`sudo systemctl status apache2`), entrar desde el navegador de la VM a `http://localhost/phpmyadmin` e iniciar sesión con el usuario `gestor_app` (no con `root`, que no tiene contraseña configurada en Ubuntu).

### Arrancar todo de nuevo después de reiniciar la VM

`mariadb` y `apache2` quedan habilitados como servicios del sistema, así que arrancan solos. Lo único que hay que levantar a mano es Django:

```bash
cd ~/ruta/al/proyecto-digital
source venv/bin/activate
cd proyecto
python manage.py runserver
```

Si por algún motivo la base de datos o phpMyAdmin no responden, verificar y (re)iniciar los servicios:

```bash
sudo systemctl status mariadb
sudo systemctl status apache2
sudo systemctl start mariadb    # si estuviera inactivo
sudo systemctl start apache2    # si estuviera inactivo
```

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
