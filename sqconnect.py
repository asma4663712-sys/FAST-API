from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
# ==========================================
# 1. DATABASE CONFIGURATION & ENGINE (Phase 2)
# ==========================================
DATABASE_URL = "sqlite:///./test.db"
# Engine: Knows where the database file is and how to talk to it
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal: The factory that manufactures Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base: The parent class that tracks our database models
Base = declarative_base()
# ==========================================
# 2. SQLALCHEMY MODELS (Phase 2)
# ==========================================
class Todo(Base):
    __tablename__ = "todos"  # Name of the table inside SQLite

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
# Create the actual database tables in test.db (happens on execution)
Base.metadata.create_all(bind=engine)
# ==========================================
# 3. PYDANTIC SCHEMAS (FastAPI Validation)
# ==========================================
class TodoCreate(BaseModel):
    title: str
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models
# ==========================================
# 4. FASTAPI INSTANCE & DEPENDENCY
# ==========================================
app = FastAPI()
# Dependency: Gives a database session to a specific request, then closes it
def get_db():
    db = SessionLocal()  # Creates a new session using the factory
    try:
        yield db         # Hands the session over to the endpoint route
    finally:
        db.close()       # Automatically shuts down the connection when request finishes
# ==========================================
# 5. CRUD ROUTERS (Phase 3 & 4)
# ==========================================
@app.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_data: TodoCreate, db: Session = Depends(get_db)):
    # 1. Turn Pydantic request data into a database model instance
    new_todo = Todo(title=todo_data.title)
    # 2. Use the session to add and commit it
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo) # Grabs the auto-generated ID from SQLite
    return new_todo
@app.get("/todos/", response_model=list[TodoResponse])
def read_all_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()