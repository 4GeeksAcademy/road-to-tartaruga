from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import List
from api.extensions import bcrypt
from api.extensions import db



class Sailor(db.Model):
    __tablename__ = "sailor"

    id: Mapped[int] = mapped_column(primary_key=True)
    sailorname: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    is_ocean_god : Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)

    #relationships



    def serialize(self):
        return {
            "id": self.id,
            "sailorname": self.sailorname,
            "email": self.email
        }
    
  

class Crew(db.Model):

    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    crew_code: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
     
    #relationships



    def serialize(self):
        return {
            "id": self.id,
            "sailorname": self.sailorname,
            "email": self.email
        }
    

class Mission(db.Model):

    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(230), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
     

    #relationships



    def serialize(self):
        return {
            "id": self.id,
            "sailorname": self.sailorname,
            "email": self.email
        }
    
class Objective(db.Model):

    __tablename__ = "objective"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    state: Mapped[str] = mapped_column(String(120, default="pending", nullable=False))
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True) 
    #relationships



    def serialize(self):
        return {
            "id": self.id,
            "sailorname": self.sailorname,
            "email": self.email
        }
    


class Input(db.Model):

    __tablename__ = "input"

    id: Mapped[int] = mapped_column(primary_key=True)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
       
    #relationships



    def serialize(self):
        return {
            "id": self.id,
            "sailorname": self.sailorname,
            "email": self.email
        }
    
class ClaudeMission(db.Model):

    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(230), nullable=False)
    points_to_achieve: Mapped[int] = mapped_column(Integer, nullable=False)
     
     
    #relationships



    def serialize(self):
        return {
            "id": self.id,
            "sailorname": self.sailorname,
            "email": self.email
        }


class CrewSailor(db.Model):

    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True)
    state: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
     
    #relationships



    def serialize(self):
        return {
            "id": self.id,
            "sailorname": self.sailorname,
            "email": self.email
        }
    