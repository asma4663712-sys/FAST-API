from fastapi import FastAPI,HTTPException,Request,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
app = FastAPI()
students_list = []

#----------------Student------------------------
class Student(BaseModel):
    id : int
    name : str
    grade : int 


#------------------Custom exception classes--------------------------------

class student_not_found(Exception): #will raise in get user by id
      def __init__(self, id:int):
          self.id = id
    
@app.exception_handler(student_not_found)
def student_not_found_handler(request : Request , exc : student_not_found):
    return JSONResponse(
       status_code= 404,
       content={
           "Message":f"student with {exc.id} not found"
       }
    )



class Invalidgrade( Exception ): #it will raise in post user
    def __init__(self, g : int):
        self.g = g #exc.g became feasible we keep the track of the grade that was invalid

@app.exception_handler(Invalidgrade) #registring the custom exception
def invalidgrade_exception_handler(request : Request , exc : Invalidgrade): #we donot raise exception here 
    return JSONResponse(
        status_code=406,
        content= {
        "Message" : f"Grade {exc.g} is invalid. Must be between 0 and 100"
        }
    )

@app.post("/students" , status_code=status.HTTP_201_CREATED)
def post_studdent(new_student : Student):
    if(new_student.grade >= 0 and new_student.grade <= 100):
        students_list.append(new_student)
        return{
            "Message" : "User created successfully"
        }
    else:
        raise Invalidgrade(new_student.grade) #type hint must not be written there in fucntion call it is not definition of a funct

@app.get("/students")
def get_students():
    return students_list

@app.get("/students/{student_id}")
def get_by_id(student_id : int):
    for student in students_list:
        if(student.id == student_id):
            return {"Message" : f"student with {student_id} found"}         
    raise student_not_found(student_id)