from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse, UserCreate, UserRead, UserUpdate
from app.db import Post, create_db_and_tables, get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
import uuid
from app.users import auth_backend, current_active_user, current_user_optional, fastapi_users

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="InstaAPI")

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])


@app.post(
    "/upload",
    tags=["App"],
    summary="Subir una imagen o video",
    description=(
        "Recibe un archivo multimedia y un caption, lo sube a ImageKit y crea un post "
        "asociado al usuario autenticado."
    ),
)
async def upload_file(
    file: UploadFile = File(..., description="Archivo de imagen o video a subir."),
    caption: str = Form("", description="Texto opcional que acompaña al post."),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> PostCreate:
    try:
        file_data = await file.read()

        upload_result = imagekit.files.upload(
            file=file_data,
            file_name=file.filename,
            use_unique_file_name=True,
            tags=["backend-upload"],
        )

        if not upload_result.url:
            raise HTTPException(status_code=500, detail="ImageKit no devolvió una URL")

        post = Post(
            user_id = user.id,
            caption=caption,
            url=upload_result.url,
            file_type="video" if file.content_type and file.content_type.startswith("video/") else "image",
            file_name=upload_result.name or file.filename,
        )
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()


@app.get(
    "/feed",
    tags=["App"],
    summary="Obtener el feed de posts",
    description="Devuelve todos los posts ordenados desde el más nuevo al más antiguo.",
)
async def get_feed(
    session: AsyncSession = Depends(get_async_session),
    user: User | None = Depends(current_user_optional)
) -> PostResponse:
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    result = await session.execute(select(User))
    users = [row[0] for row in result.all()]
    user_dict = {u.id: u.email for u in users}

    posts_data = []

    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "user_id": str(post.user_id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
                "is_owner": bool(user and post.user_id == user.id),
                "email": user_dict.get(post.user_id, "Unknown")   
            }
        )

    return {"posts": posts_data}


@app.delete(
    "/posts/{post_id}",
    tags=["App"],
    summary="Eliminar un post",
    description="Elimina un post solo si pertenece al usuario autenticado.",
)
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        if post.user_id != user.id:
            raise HTTPException(status_code=403, detail= "You don't have permission to delete this post")

        await session.delete(post)
        await session.commit()

        return {"sucess": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=(str(e)))