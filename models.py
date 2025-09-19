import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/crewai")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    raw_text = Column(Text, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_analysis_result(result_json, metadata):
    db = SessionLocal()
    try:
        record = AnalysisResult(task_id=result_json.get("task_id"), metadata=metadata, result=result_json, raw_text=result_json.get("raw_text"))
        db.add(record)
        db.commit()
        db.refresh(record)
        return record.id
    finally:
        db.close()
 
