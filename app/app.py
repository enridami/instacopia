from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
import uuid


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/upload")
async def upload_file(
    file:UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
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


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []

    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "created_at": post.created_at.isoformat()    
            }
        )

    return {"posts": posts_data}


@app.delete("/posts/{post-id}")
async def  delete_post(post_id:str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        await session.delete(post)
        await session.commit()

        return {"sucess": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=(str(e)))