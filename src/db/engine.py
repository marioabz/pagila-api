from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import Settings


def get_engine(db_settings: Settings):

    return create_engine(
        f"postgresql+psycopg2://{db_settings.database_user}:{db_settings.database_password}@{db_settings.database_url}:{db_settings.database_port}/{db_settings.database_db}"
    )


db_engine = get_engine(Settings())

SessionLocal = sessionmaker(bind=db_engine)


def get_db():
    with SessionLocal() as session:
        yield session
