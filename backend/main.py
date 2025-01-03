from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Database configuration
DATABASE_URL = "sqlite:///./test_management.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database Models
class TestCase(Base):
    __tablename__ = "test_cases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(String)

# Create database tables
Base.metadata.create_all(bind=engine)

# Pydantic Models for Input Validation
class TestCaseCreate(BaseModel):
    name: str
    description: str
    status: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints

@app.get("/testcases/")
def read_test_cases(db: Session = Depends(get_db)):
    """
    Fetch all test cases from the database.
    """
    test_cases = db.query(TestCase).all()
    return test_cases

@app.post("/testcases/")
def create_test_case(test_case: TestCaseCreate, db: Session = Depends(get_db)):
    """
    Add a new test case to the database.
    """
    new_test_case = TestCase(
        name=test_case.name,
        description=test_case.description,
        status=test_case.status,
    )
    db.add(new_test_case)
    db.commit()
    db.refresh(new_test_case)
    return new_test_case

@app.get("/")
def root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "Test Management Backend is running."}
