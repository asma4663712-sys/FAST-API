from fastapi import FastAPI ,HTTPException , Depends ,Header
from jose import jwt
from datetime import datetime,timedelta , timezone

app = FastAPI()

SECRET_KEY = "My-token"
AlGORITHM = "HS256"  #symmetric signing cuz same key unlike RLC algorithm 

#------creating token-----------------

def create_token(data:dict): #this data will come from user login credentials
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30) 
    to_encode.update({"exp":expire}) 
    token = jwt.encode(to_encode , SECRET_KEY , AlGORITHM) # format xxxx.yyyy.zzzz
    return token  #to encode is destroyed here

#--------Generating token-------------

@app.post("/login")
def login(password : str , user_name : str):
    if user_name != "admin" or password != 1234: 
        raise HTTPException(status_code=401 , detail= "Invalid credintials") #HTTP when we need error code
    token = create_token({"sub" : user_name}) # never put password here it will be written in payload part which can be read by anyone
    return {"Access token" : token}

#----------Token verification ----------
def token_verif(token:str = Header(None)): #what is the Header none here how token is in str?
    try: #cause we do not want to stop the execution of the remaining program
        payload = jwt.decode(token , SECRET_KEY , algorithms=[AlGORITHM]) 
        return payload
    except:
        raise HTTPException(status_code=401 , detail= "Invalid credintials")
    
    