from pydantic import BaseModel, Field
from fastapi_users import schemas
import uuid

class PostCreate(BaseModel):
    title: str = Field(
        ...,
        description="Título del post.",
        examples=["Atardecer en la playa"],
    )
    content: str = Field(
        ...,
        description="Contenido o descripción del post.",
        examples=["Una foto tomada al final del día."],
    )
class PostResponse(BaseModel):
    title: str = Field(
        ...,
        description="Título del post.",
        examples=["Atardecer en la playa"],
    )
    content: str = Field(
        ...,
        description="Contenido o descripción del post.",
        examples=["Una foto tomada al final del día."],
    )

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass