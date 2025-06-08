from time import timezone
from .misrlex_base import SQLAlchemyBase
from sqlalchemy import Column, func, Integer, DateTime, String
from sqlalchemy.orm import relationship


class Project(SQLAlchemyBase):

    __tablename__ = "projects"
    project_id = Column(Integer, primary_key = True, autoincrement = True)

    created_at = Column(DateTime(timezone = True), default = func.now(), nullable = False)
    updated_at = Column(DateTime(timezone = True), default = func.now(), onupdate = func.now(), nullable = False)

    chunks = relationship("DataChunk", back_populates="project")
    assets = relationship("Asset", back_populates="project")
