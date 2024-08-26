from pydantic import BaseModel




class newuser(BaseModel):
    id:int
    username:str
    email:str
    password:str
    WABAID:int
    PAccessToken:str
    Phone_id:int


class register_user(BaseModel):
    username:str
    email:str
    password:str
    WABAID:int
    PAccessToken:str
    Phone_id:int

# login user model

class LoginUser(BaseModel):
    username:str
    password:str