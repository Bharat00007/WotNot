from fastapi import APIRouter,Depends,HTTPException
from ..models import User
from ..Schemas import user
from ..database import database
from sqlalchemy.orm import Session
from .. import hashing
router=APIRouter(tags=['User'])

@router.post('/register')
def newuser(request:user.register_user,db: Session=Depends(database.get_db)):
    if(db.query(User.User).where(request.email==User.User.email).first()):
         raise HTTPException(
            status_code=400, detail="Contact with this email or phone already exists"
        )
    
    else:
        registeruser=User.User( 
            username=request.username,
            email=request.email,
            password_hash=hashing.Hash.bcrypt(request.password),  # Decode the hash to store it as a string
            WABAID=request.WABAID,
            PAccessToken=request.PAccessToken,
            Phone_id=request.Phone_id)
        db.add(registeruser)
        db.commit()
        db.refresh(registeruser)
        return registeruser
    
