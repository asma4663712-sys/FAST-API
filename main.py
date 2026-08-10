# from fastapi import FastAPI  #importing tools 
# from pydantic import BaseModel
# app = FastAPI() #class created
# class User(BaseModel): #user class created using BaseModel
#     name : str
#     age : int
#     gender : str 
# @app.post("/create_user")  #get -> read post -> cout
# def createuser(user : User): #function 
#     return{
#         "Message" :  "user created successfully",  #returning dictionary
#         "data"  : user
#         }

# from  fastapi import FastAPI
# from pydantic import BaseModel
# app = FastAPI()
# class address(BaseModel):
#     address:str
#     postal_code:int 
# class user(BaseModel):  #why we use base model?
#     name:str 
#     age:float
#     gender:str
#     Address:address #composition occured
# @app.post("/create_user")
# def create_usr(User:user):
#     return user  #returning dict of user data ???why

#-----------To do application------------------------------------------------------------
# from fastapi import FastAPI
# from pydantic import BaseModel
# app = FastAPI()

# todos = []  #list of objects

# class Todo(BaseModel):
#     id:int
#     name:str
#     completed:bool
# @app.post("/todos")    #post means post that task in the database
# def create_todo(todo:Todo):
#     todos.append(todo) #addign task in the list
#     return {
#         "Message":"To do added successfully",
#         "data":todo #object parameter returned which will be converted to pyhton due to pydantic library
#     }
# @app.get("/todos")  #get means testing the posting data by reading it from database
# def get_todod():
#     return todos

# @app.get("/todos/{todo_id}")
# def get_todo(todo_id:int):
#     for search in todos:
#         if (todo_id == search.id):
#             return search
#     else:
#         return{"Message":"Error occured.\n"}
# @app.put("/todos{todo_id}")
# def update_todo(todo_id:int , updated: Todo):
#     for index, todo in enumerate(todos): #todo in todos at some index
#         if todo.id == todo_id: #if at that index id is eq to  entered id
#             todos[ index ] = updated #replace the obj at that index with updated todo from request body
#             return{
#                 "message" : "Data updated.\n",
#                 "Data" : updated
#             }           
#     return{
#                 "Message" : "Error occured while updating data.\n"
#             }
# @app.delete("/todos{todo_id}")
# def delete_todo(todo_id : int , deleted : Todo):
#     for index, todo in enumerate(todos):
#         if todo_id == todo.id:
#             todos.pop(index)
#             return{
#                 "Message" : "Data deleted.\n"
#             }
#         else:
#             return{
#                 "Message" : "Error occured while deleting data.\n"
#             }
from fastapi import FastAPI,HTTPException,status,Depends,Header
def common_Function()