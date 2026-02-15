from sqlmodel import create_engine, Session, SQLModel
from backend.core.settings import settings

engine = create_engine(settings.DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
