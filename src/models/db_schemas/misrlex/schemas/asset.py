from time import timezone
from .misrlex_base import SQLAlchemyBase
from sqlalchemy import Column, func, Integer, DateTime, String, ForeignKey, Index 
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship



class Asset(SQLAlchemyBase):

    __tablename__ = "assets"
    asset_id = Column(Integer, primary_key = True, autoincrement = True)
    
    asset_type = Column(String, nullable = False)
    asset_name = Column(String, nullable = False)
    asset_size = Column(Integer, nullable = False)
    asset_config = Column(JSONB, nullable = True)
    asset_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable = False)

    created_at = Column(DateTime(timezone = True), default = func.now(), nullable = False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)


    project = relationship("Project", back_populates = "assets")
    chunks = relationship("DataChunk", back_populates="asset")

    __table_args__ = (
        Index("asset_project_id_index", "asset_project_id"),
        Index("asset_type_index", "asset_type"),
    )