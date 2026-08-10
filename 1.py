from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
users_list = []
class User(BaseModel):
    id : int
    name : str
    age : int
    alive : bool
@app.post("/users")
def add_user(user:User):
    users_list.append(user)
    return{"Message" : "User added successfully.\n"}
@app.get("/users")
def get_user():
    return users_list
@app.put("/users{user_id}")
def update_user(user_id : int , Updated : User, alive:bool = True): #query param used if user did not explixitly tell us alive status tehn by default it is true this is query
    for a,b in enumerate(users_list): #b obj at index a in users_list
        if user_id == b.id: #if entered id is eq to the obj b id at index a
            users_list[a] = Updated #obj at ndex a is replaced by updated user from request body
            return{
                "Message" : "User updated.\n",
                "data" : users_list[ a ]
            }
    return{"Message":"Error occured while updating the user.\n"} 