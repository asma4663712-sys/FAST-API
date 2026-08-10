# from fastapi import FastAPI,HTTPException,Depends
# from pydantic import BaseModel
# from sqlalchemy import create_engine,Column, Integer,String, Boolean
# from sqlalchemy.orm import sessionmaker,Session, declarative_base

# app = FastAPI()

# Database_URL = "sqlite:///./crud.db"

# Engine = create_engine(Database_URL, connect_args= {"check_same_thread" : False}) #creatign engine 
# SessionLocal = sessionmaker( bind = Engine) #session factory
# Base = declarative_base()
# class Todo(Base): #class using Base instead of using base model
#     __tablename__ = "todos"
#     id = Column(Integer, index = True , primary_key = True)
#     name =Column(String )
#     completed = Column(Boolean)
# #all table creation
# Base.metadata.create_all(bind=Engine) 

# def get_db(): #we will use dependency later  
#     db = SessionLocal() 
#     try:
#         yield db
#     finally:
#         db.close()

# #---------------------------functions creation-----------------------------------
# @app.post("/todos")
# def create_todo(title:str , db:Session = Depends(get_db)):
#     todo = Todo(name = title , completed = False )
#     db.add(todo)
#     db.commit()
#     db.refresh(todo)
#     return{
#         "message" : "toddo added to the table successfully",
#         # "data" : todo
#     }
# @app.get("/todos")
# def read_todos(db:Session=Depends(get_db)):
#     todos = db.query(Todo).all() #are we jsut refering it to the table orobj we created it was never the list but it is a table so it will be able to store that all?
#     return{ 
#         "Length of data":len(todos),
#         "Data" : todos
#     }
# @app.get("/todos/{todo_id}")
# def read_todos_byid(todo_id : int ,db:Session=Depends(get_db)):
#     todo = db.query(Todo).filter(Todo.id == todo_id).first() #Todo is a class how can we compare its id and wht is first and filter explain it all
#     if not todo:
#         raise HTTPException(status_code=404 , detail= "Todo not found in the table")
#     return todo
# @app.put("/todos/{todo_id}")
# def update_todos(todo_id : int ,title:str ,db:Session=Depends(get_db)):
#     todo = db.query(Todo).filter(Todo.id == todo_id).first() #Todo is a class how can we compare its id and wht is first and filter explain it all
#     if not todo:
#         raise HTTPException(status_code=404 , detail= "Todo not found in the table")
#     todo.name =title
#     db.commit()
#     db.refresh(todo)
#     return {
#         "Message" : "Todo updated successfully",
#         "Data" : todo
#     }
# @app.delete("/todos/{todo_id}")
# def delete_todos(todo_id : int ,db:Session=Depends(get_db)):
#     todo = db.query(Todo).filter(Todo.id == todo_id).first() #Todo is a class how can we compare its id and wht is first and filter explain it all
#     if not todo:
#         raise HTTPException(status_code=404 , detail= "Todo not found in the table")
#     db.delete(todo)
#     db.commit()
#     return {
#         "Message" : "Todo deleted successfully"
#     }