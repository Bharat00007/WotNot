from ..database import database
from sqlalchemy import Integer,Column,String,BigInteger,TIMESTAMP,func


# user model


class User(database.Base):
    __tablename__="Users"
    id=Column(Integer, primary_key=True)
    username=Column(String)
    email=Column(String)
    password_hash=Column(String)
    WABAID=Column(BigInteger)
    PAccessToken=Column(String)
    Phone_id=Column(BigInteger)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())