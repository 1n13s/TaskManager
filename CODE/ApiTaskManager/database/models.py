from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from .connection import Base,relationship

class Users(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=True)

    tasks = relationship("Tasks", back_populates="owner")

class Tasks(Base):
    __tablename__="tasks"
    id = Column(Integer,primary_key=True,index=True)
    description = Column(String)
    priority = Column(Integer)
    title = Column(String)
    complete = Column(Boolean)
    id_user = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="tasks")
