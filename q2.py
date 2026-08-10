from fastapi import FastAPI , Depends , Header , HTTPException ,File , UploadFile
import os
import shutil
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import create_engine , Boolean , Integer , Column ,ForeignKey, String #sqlachemy is pyhton library which enable us to talk to sqlite data base
from sqlalchemy.orm import sessionmaker , Session , declarative_base 
from datetime import timedelta , datetime , timezone
from jose import jwt
from passlib.context import CryptContext
app = FastAPI()
#step 1 : creating the upload folder if it does not exist to store the files in it
UPLOAD_DIR = "upload" 
if not os.path.exists(UPLOAD_DIR): 
    os.mkdir(UPLOAD_DIR) 

#step 2 : connecting the browser to that upload folder
app.mount("/files" , StaticFiles(directory = UPLOAD_DIR) ,name = "files" )
#step 3 : uploading file

@app.post("/upload")
def post_file(file : UploadFile = File[...]): #file is an bj of type UploadFile 
    filename = file.filename
    path = os.path.join(UPLOAD_DIR , filename ) 

    if not filename:
        raise HTTPException(status_code= 400 , detail= "File not found.")
    with open(path , "wb") as buffer: #with means will automatically close the file and buffer is the var created here
        shutil.copyfileobj(file.file , buffer ) #file.file stores the binary form of the file
        return {
            "message" : "file uploaded successfully.",
            "filename" : filename,
            "fileurl" : f"http://127.0.0.1:65092/files/{filename}"
        }
@app.get("/download/{filename}")
def get_all_files(filename : str):
    file_path = os.path.join(UPLOAD_DIR , filename )
    if not file_path:
        raise HTTPException(status_code= 400 , detail= "File path does not exist.")
    return{
            "fileurl" : f"http://127.0.0.1:65092/files/{filename}"
    }
#------------------Connecting to data base -----------------------------

#STEP 1: engine creation

Database_URL = "sqlite:///./mynotes.db"
Engine = create_engine(Database_URL , connect_args= { "check_same_thread" : False})

#STEP 2: Session factory creation 
SessionLocal = sessionmaker(bind = Engine)
#STEp 3: Base parent class creation from which all table classes will be inheriting here
Base = declarative_base()

#STEP 4: blue print for tables
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True) 
    password = Column(String) #can be common dude!!

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

#STEP 5: Table creation 
Base.metadata.create_all(bind = Engine)

#STEP 6: session creation 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() #we are not returning here

#---------------Pydantic models--------------------------------

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class NoteRequest(BaseModel):
    title: str
    content: str

#------------Autehntication----------------------------------------
ALGORITHM = "HS256"
SECRET_KEY = "Regiistering_Request"

# password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token( data : dict ):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours = 1)
    to_encode.update({ "exp" : expire } ) 
    token = jwt.encode( to_encode , SECRET_KEY , algorithm = ALGORITHM )
    return token

def token_verification( token :  str  =  Header( None ) ):
    try:
        payload = jwt.decode( token , SECRET_KEY , algorithms = [ALGORITHM])
        return payload #contains the username only not the password
    except:
        raise HTTPException( status_code = 401 , detail = "Invalid")

@app.post("/login")
def create_login_req( data : LoginRequest , db: Session=Depends(get_db)):
    #we will match the user  
    exist = db.query(User).filter(User.username == data.username).first()
    if not exist:
        raise HTTPException(status_code= 404 , detail= "User not found.") 
    pass_exist = pwd_context.verify( data.password, exist.password)
    #plain pass , hashed pass (from the db)
    # return either T or F(we are comparing the pass of exist (only the user whose username macthes here))
    if not pass_exist:
        raise HTTPException(status_code= 401 , detail= "Incorrect password.") 
    token = create_token( { "sub" : data.username})    
    return{
    "Access token" : token
            }

@app.post("/request_registration" )
def post_registration( data : RegisterRequest , db: Session = Depends ( get_db) ):
  exist = db.query(User).filter(User.username == data.username).first()
  if exist:
      raise HTTPException(status_code= 409 , detail= "User already exists.")
  hashed_pass = pwd_context.hash(data.password)
  user = User(username = data.username , password = hashed_pass)
  
  #if does not exists register the user 
  db.add(user)
  db.commit()
  db.refresh(user)
  return{
      "message" : "Request added to the table successfully.",
      "data" : { "id" :  user.id ,
                "username" : user.username
                  }
  }

def get_currrent_user(db: Session = Depends(get_db) , payload : dict = Depends(token_verification)):
     username = payload["sub"]
     found = db.query(User).filter(User.username == username ).first()
     if not found:
         raise HTTPException(status_code=400 , detail= "user does not exist")
     return found

@app.post("/cretenotes")
def create_notes( data : NoteRequest ,current: User = Depends(get_currrent_user), db:Session=Depends(get_db) ):
    flag = db.query(Note).filter(Note.title == data.title , current.id == Note.owner_id).first() #for the current user
    if flag:
        raise HTTPException(status_code= 409 , detail="Notes with the same title already exists in the table for this user.")
    note = Note(owner_id = current.id , content = data.content , title = data.title)
    db.add(note)
    db.commit()
    db.refresh(note)
    return {
     "message" : "Note added to the table successfully.",
         "data" : {
             "id" : note.id,
            "title" : note.title,
            "Content" : note.content, 
            "owner_id" : note.owner_id
        }   
        }

@app.get("/getnotes")
def read_all_notes(db:Session = Depends(get_db) , current : User = Depends(get_currrent_user)):
    all_notes = db.query(Note).filter(Note.owner_id == current.id).all()
    if not all_notes:
        raise HTTPException(status_code= 404 , detail= "No notes found.")
    return {
        "Number of notes" : len(all_notes) ,
        "data" : [
            {
            "id" : note.id,
            "owner_id" : note.owner_id,
            "title" : note.title,
            "Content" : note.content,
            } for note in all_notes
              ]
        }    

@app.put("/updatenotes/{notes_id}")
def update_notes(notes_id: int, data: NoteRequest, db: Session = Depends(get_db), current: User = Depends(get_currrent_user)):
    note = db.query(Note).filter(Note.id == notes_id, Note.owner_id == current.id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"No note found with id {notes_id}.")

    note.title = data.title
    note.content = data.content
    db.commit()
    db.refresh(note)

    return {
        "message": "Note updated successfully.",
        "data": {
            "id": note.id,
            "title": note.title,
            "Content": note.content,
            "owner id": note.owner_id,
        },
    }


@app.delete("/deletenotes/{notes_id}")
def delete_notes(notes_id: int, db: Session = Depends(get_db), current: User = Depends(get_currrent_user)):
    note = db.query(Note).filter(Note.id == notes_id, Note.owner_id == current.id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"No note found with id {notes_id}.")

    db.delete(note)
    db.commit()
    return {
        "message": "Note deleted successfully.",
        "data": [{
            "id": note.id,
            "title": note.title,
            "Content": note.content,
            "owner id": note.owner_id,
        }],
    }
     
