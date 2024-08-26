from ..database import database
from sqlalchemy import Integer,Column,String,ARRAY,Text
from . import User

from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, func

# broadcast List
class BroadcastList(database.Base):
    __tablename__="BroadcastList"
    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer,ForeignKey(User.User.id))
    name=Column(String)
    template=Column(String)
    contacts=Column(ARRAY(String))
    success=Column(Integer)
    failed=Column(Integer)
    status=Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())











class Template(database.Base):
    __tablename__ = 'templates'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  # Ensure id is auto-incrementing
    name = Column(String, nullable=False)
    components = Column(Text, nullable=False)