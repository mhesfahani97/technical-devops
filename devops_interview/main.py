from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select

from devops_interview.config import settings
from devops_interview.database import get_session, create_db_and_tables
from devops_interview.models import (
    User,
    UserCreate,
    UserRead,
    UserUpdate,
    UserReadWithPosts,
    Post,
    PostCreate,
    PostRead,
    PostUpdate,
    PostReadWithAuthor,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown - nothing to do for sync


app = FastAPI(
    title=settings.app.title,
    description=settings.app.description,
    version=settings.app.version,
    debug=settings.app.debug,
    lifespan=lifespan,
)


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "devops-interview-api"}


# User endpoints
@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """Create a new user"""
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserRead])
def get_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """Get all users"""
    statement = select(User).offset(skip).limit(limit)
    result = session.exec(statement)
    return result.all()


@app.get("/users/{user_id}", response_model=UserReadWithPosts)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a user by ID with their posts"""
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement)
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Get user's posts
    posts_statement = select(Post).where(Post.author_id == user_id)
    posts_result = session.exec(posts_statement)
    posts = posts_result.all()

    return UserReadWithPosts(
        **user.model_dump(), posts=[PostRead(**post.model_dump()) for post in posts]
    )


@app.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)
):
    """Update a user"""
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement)
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user_update.model_dump(exclude_unset=True)
    for field, value in user_data.items():
        setattr(user, field, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Delete a user"""
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement)
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    session.delete(user)
    session.commit()


# Post endpoints
@app.post("/posts/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    """Create a new post"""
    # Verify user exists
    user_statement = select(User).where(User.id == post.author_id)
    user_result = session.exec(user_statement)
    user = user_result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Author not found"
        )

    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@app.get("/posts/", response_model=List[PostReadWithAuthor])
def get_posts(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """Get all posts with author information"""
    statement = select(Post, User).join(User).offset(skip).limit(limit)
    result = session.exec(statement)

    posts_with_authors = []
    for post, author in result:
        posts_with_authors.append(
            PostReadWithAuthor(
                **post.model_dump(), author=UserRead(**author.model_dump())
            )
        )

    return posts_with_authors


@app.get("/posts/{post_id}", response_model=PostReadWithAuthor)
def get_post(post_id: int, session: Session = Depends(get_session)):
    """Get a post by ID with author information"""
    statement = select(Post, User).join(User).where(Post.id == post_id)
    result = session.exec(statement)
    post_with_author = result.first()

    if not post_with_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    post, author = post_with_author
    return PostReadWithAuthor(
        **post.model_dump(), author=UserRead(**author.model_dump())
    )


@app.put("/posts/{post_id}", response_model=PostRead)
def update_post(
    post_id: int, post_update: PostUpdate, session: Session = Depends(get_session)
):
    """Update a post"""
    statement = select(Post).where(Post.id == post_id)
    result = session.exec(statement)
    post = result.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    post_data = post_update.model_dump(exclude_unset=True)
    for field, value in post_data.items():
        setattr(post, field, value)

    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    """Delete a post"""
    statement = select(Post).where(Post.id == post_id)
    result = session.exec(statement)
    post = result.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    session.delete(post)
    session.commit()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "devops_interview.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.debug,
    )
