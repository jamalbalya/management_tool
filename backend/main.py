from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database Setup
DATABASE_URL = "sqlite:///./test_management.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class TestCaseDB(Base):
    __tablename__ = "test_cases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    linked_issue = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/testcases/")
def create_test_case(name: str, description: str, db=Depends(get_db)):
    test_case = TestCaseDB(name=name, description=description)
    db.add(test_case)
    db.commit()
    db.refresh(test_case)
    return test_case

@app.get("/testcases/")
def list_test_cases(db=Depends(get_db)):
    return db.query(TestCaseDB).all()

@app.get("/testcases/{test_case_id}")
def get_test_case(test_case_id: int, db=Depends(get_db)):
    test_case = db.query(TestCaseDB).filter(TestCaseDB.id == test_case_id).first()
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    return test_case
