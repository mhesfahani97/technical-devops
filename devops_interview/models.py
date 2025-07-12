from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    """Base user model with shared attributes"""

    email: str = Field(unique=True, index=True, max_length=255)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """User database model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    posts: list["Post"] = Relationship(back_populates="author")


class UserCreate(UserBase):
    """User creation model"""

    pass


class UserRead(UserBase):
    """User read model"""

    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    """User update model"""

    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = Field(default=None)


class PostBase(SQLModel):
    """Base post model with shared attributes"""

    title: str = Field(max_length=200)
    content: str
    is_published: bool = Field(default=False)


class Post(PostBase, table=True):
    """Post database model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key
    author_id: int = Field(foreign_key="user.id")

    # Relationships
    author: User = Relationship(back_populates="posts")


class PostCreate(PostBase):
    """Post creation model"""

    author_id: int


class PostRead(PostBase):
    """Post read model"""

    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int


class PostUpdate(SQLModel):
    """Post update model"""

    title: Optional[str] = Field(default=None, max_length=200)
    content: Optional[str] = Field(default=None)
    is_published: Optional[bool] = Field(default=None)


class PostReadWithAuthor(PostRead):
    """Post read model with author information"""

    author: UserRead


class UserReadWithPosts(UserRead):
    """User read model with posts"""

    posts: list[PostRead] = []
