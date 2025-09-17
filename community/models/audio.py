from sqlmodel import Field, SQLModel, Column
from sqlalchemy.types import UserDefinedType
from typing import List

class Vector(UserDefinedType):
    def __init__(self, dimensions: int):
        self.dimensions = dimensions

    def get_col_spec(self):
        return f"VECTOR(FLOAT, {self.dimensions})"


class AudioSegment(SQLModel, table=True):
    __tablename__ = 'audio_segments'

    id: int = Field(primary_key=True)
    embedding: List[float] = Field(sa_column=Column(Vector(1024)))
    object_id: str