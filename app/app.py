from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate

app = FastAPI()


text_posts = {
    1: {"title": "New post,", "content": "cool post"},
    2: {"title": "Aprendiéndo FastAPI", "content": "Construir APIs con Python es sumamente rápido y divertido."},
    3: {"title": "Consejo del día", "content": "No olvides escribir pruebas unitarias para tus endpoints."},
    4: {"title": "Herramientas modernas", "content": "Usar uv para gestionar proyectos acelera mucho el flujo de trabajo."},
    5: {"title": "Bug misterioso", "content": "Pasé dos horas buscando un error y solo era un espacio de más."},
    6: {"title": "¡Hola Mundo!", "content": "Esta es la publicación final de prueba para rellenar la base de datos."},
    7: {"title": "Rendimiento puro", "content": "FastAPI es uno de los frameworks de Python más rápidos gracias a Starlette y Pydantic."},
    8: {"title": "Tips de Python", "content": "Los f-strings hacen que formatear texto sea legible y eficiente."},
    9: {"title": "Configurando el entorno", "content": "Crear un entorno virtual limpio evita conflictos entre librerías."},
    10: {"title": "Introducción a las APIs", "content": "REST es un estilo de arquitectura estándar para diseñar servicios web."},
    11: {"title": "Documentación automática", "content": "Solo entra a /docs para ver la interfaz interactiva de Swagger UI."},
    12: {"title": "El poder de Pydantic", "content": "Pydantic se encarga de la validación de datos y tipos de forma estricta."},
    13: {"title": "Código asíncrono", "content": "Usar async y await permite manejar múltiples peticiones concurrentes."},
    14: {"title": "Manejo de errores", "content": "Lanzar HTTPException personalizadas mejora la experiencia del cliente de la API."},
    15: {"title": "Seguridad básica", "content": "Nunca subas contraseñas ni llaves secretas a tu repositorio de GitHub."},
    16: {"title": "Variables de entorno", "content": "Usa archivos .env para guardar configuraciones sensibles de tu app."},
    17: {"title": "Middlewares", "content": "Los middlewares procesan las peticiones antes de que lleguen a tus rutas."},
    18: {"title": "Bases de datos", "content": "Pronto cambiaremos este diccionario en memoria por SQLite o PostgreSQL."},
    19: {"title": "Despliegue", "content": "Puedes subir tu API de FastAPI de forma sencilla usando Docker."},
    20: {"title": "Fin de las pruebas", "content": "Con veinte elementos ya puedes probar la paginación en tus endpoints."}
}


@app.get("/posts")
def get_all_posts(limit:int=None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_post(id:int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

@app.post("/posts")
def create_post(post:PostCreate):
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post