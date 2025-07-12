from sqlmodel import SQLModel, create_engine, Session

from devops_interview.config import settings


# Create sync engine
engine = create_engine(
    settings.database.database_url,
    echo=settings.app.debug,
)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
