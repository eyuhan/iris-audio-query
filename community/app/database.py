from typing import Generator
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
import irisnative

from models.audio import AudioSegment
from app.config import AppConfig

DATABASE_URL = AppConfig.DATABASE_URL
RESET_DATABASE = AppConfig.RESET_DATABASE

engine = create_engine(DATABASE_URL)

connection = irisnative.createConnection(
    hostname=AppConfig.DATABASE_HOST,
    port=AppConfig.DATABASE_PORT,
    namespace=AppConfig.DATABASE_NAMESPACE,
    username=AppConfig.DATABASE_USER,
    password=AppConfig.DATABASE_PASSWORD,
)
db = irisnative.createIris(connection)

def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(engine) as session:
        yield session

def init_database(reset_data: bool = True):
    """Initialize database tables and sample data."""
    if reset_data:
        SQLModel.metadata.drop_all(engine)

    SQLModel.metadata.create_all(engine)