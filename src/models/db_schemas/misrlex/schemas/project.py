from time import timezone
from .misrlex_base import SQLAlchemyBase
from sqlalchemy import Column, func, Integer, DateTime, String


class Project(SQLAlchemyBase):

    __tablename__ = "projects"
    project_id = Column(Integer, primary_key = True, autoincrement = True)

    created_at = Column(DateTime(timezone = True), default = func.now(), nullable = False)
    updated_at = Column(DateTime(timezone = True), default = func.now(), onupdate = func.now(), nullable = False)

    name = Column(String, nullable = False)
    description = Column(String, nullable = True)
