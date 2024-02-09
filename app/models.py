from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
import time

class Admin(Base):
    __tablename__= "admin"
    id= Column(Integer, primary_key=True, index= True)
    role= Column(String)
    username= Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True)
    phone_no = Column(String)
    registration_date= Column(String, default= time.strftime("%Y%m%d-%H%M%S"))
    user_id= Column(Integer, ForeignKey('users.id'))
    user= relationship("Users", back_populates="admin")


class Users(Base):
    __tablename__= "users"
    activated= Column(String, default= True)
    id= Column(Integer, primary_key=True, index= True)
    username= Column(String, unique=True)
    email= Column(String, unique=True)
    password= Column(String)
    registration_date= Column(String, default= time.strftime("%Y%m%d-%H%M%S"))

    admin= relationship("Admin", back_populates="user")
    image_label= relationship("ImageLabels", back_populates="users")


class ImageLabels(Base):
    __tablename__ = "image_labels"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)

    images= relationship("Images", back_populates="image_label")
    user_id= Column(Integer, ForeignKey('users.id'))
    users= relationship("Users", back_populates="image_label")

class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String)
    ingredient = Column(String)
    image_path= Column(String)

    image_label_id= Column(Integer, ForeignKey('image_labels.id'))
    image_label= relationship("ImageLabels", back_populates="images")

