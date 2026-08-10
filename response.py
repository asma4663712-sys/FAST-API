from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
users_list = []

# ---------- Models ----------

class User(BaseModel):          # what user sends IN (includes password)
    id: int
    name: str
    age: int
    password: str

class User_Response(BaseModel): # what you send OUT (hide password)
    id: int
    name: str
    age: int

# ---------- Custom Exception ----------

class User_Not_Found(Exception):
    def __init__(self, id: int):
        self.id = id            # store the id so handler can use it

# ---------- Exception Handler ----------
#---------------------Global Handler------------------------------
@app.exception_handler(User_Not_Found) #whenever User_Not_Found exception is raised following funct is called
async def user_not_found_handler(request: Request, exc: User_Not_Found):
    return JSONResponse(                    # parentheses ✅
        status_code=404,
        content={
            "status": "error",
            "message": f"User {exc.id} not found"
        }
    )

# ---------- Routes ----------

@app.post("/users", status_code=status.HTTP_201_CREATED)  # keyword arg ✅
def create_user(new: User):
    users_list.append(new)
    return {
        "message": "User created successfully",
        "data": new
    }

@app.get("/users")
def get_users():
    return users_list           # just return the whole list

@app.get("/users/{user_id}")    # ← this is how you fetch ONE user
def get_user(user_id: int):
    for user in users_list:
        if user.id == user_id:
            return user
    raise User_Not_Found(id=user_id)   # no user found → fire your exception