# InstaAPI

Instacopia es un backend de práctica hecho con FastAPI para simular una red social simple. Permite registrar y autenticar usuarios, subir imágenes o videos, guardar publicaciones en SQLite y listar un feed de posts con información del autor.

## Tecnologías usadas

- FastAPI
- fastapi-users
- SQLAlchemy
- SQLite
- ImageKit
- python-dotenv
- Uvicorn

## Funcionalidades

- Registro de usuarios
- Login con JWT
- Usuario autenticado para subir contenido
- Subida de imágenes o videos a ImageKit
- Guardado de posts en la base de datos
- Feed ordenado de publicaciones
- Eliminación de posts propios

## Estructura del proyecto

- `main.py`: punto de entrada para ejecutar la app con Uvicorn
- `app/app.py`: rutas principales y configuración de FastAPI
- `app/db.py`: modelos y conexión a la base de datos
- `app/users.py`: autenticación y configuración de fastapi-users
- `app/schemas.py`: schemas de Pydantic para documentación y validación
- `app/images.py`: configuración de ImageKit

## Requisitos

- Python 3.12 o superior
- Una cuenta de ImageKit

## Instalación

1. Cloná el repositorio.
2. Creá y activá un entorno virtual.
3. Instalá las dependencias.

Ejemplo con `uv`:

```bash
uv sync
```

Si preferís `pip`:

```bash
pip install -e .
```

## Variables de entorno

Creá un archivo `.env` en la raíz del proyecto con estas variables:

```env
IMAGEKIT_PRIVATE_KEY=tu_private_key
IMAGEKIT_PUBLIC_KEY=tu_public_key
IMAGEKIT_URL=tu_url_de_imagekit
```

NOTA: el archivo original .env queda reservado por motivos de seguridad. Para realizar la prueba se debe crear una cuenta en ImageKit e introducir las respectivas claves privadas y publicas.

## Cómo ejecutar el proyecto

### Opción 1: ejecutar `main.py`

```bash
python main.py
```

### Opción 2: ejecutar con Uvicorn directamente

```bash
uvicorn app.app:app --reload
```

La API quedará disponible en:

- `http://127.0.0.1:8000`
- Documentación Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints principales

### Autenticación y usuarios

- `POST /auth/jwt/login`: inicia sesión y devuelve un token JWT.
- `POST /auth/register`: registra un nuevo usuario.
- `POST /auth/forgot-password`: inicia el flujo de recuperación de contraseña.
- `POST /auth/reset-password`: completa el reset de contraseña.
- `POST /auth/request-verify-token`: solicita verificación de usuario.
- `POST /auth/verify`: verifica el usuario con token.
- `GET /users/me`: devuelve el usuario autenticado.

### Posts

- `POST /upload`: sube una imagen o video y crea un post asociado al usuario autenticado.
- `GET /feed`: devuelve todos los posts ordenados por fecha.
- `DELETE /posts/{post_id}`: elimina un post si pertenece al usuario autenticado.

## Notas de desarrollo

- Este proyecto usa SQLite para facilitar la práctica y el desarrollo local.
- ImageKit se usa para almacenar los archivos multimedia y guardar solo la URL en la base de datos.
- Swagger UI es útil para probar los endpoints manualmente mientras desarrollás el frontend.


## Screenshots del Swagger UI
- 

