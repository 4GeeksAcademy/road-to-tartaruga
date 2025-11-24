from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from api.extensions import bcrypt
from api.extensions import db



class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)


    #relationships

    missions : Mapped[List["Mission"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    crew_users : Mapped[List["CrewUser"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    blocked_users : Mapped[List["BlockedUser"]] = relationship(back_populates="user", cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
    
    def get_info(self):

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "crews": [crew_user.crew_id for crew_user in self.crew_users],
            "blocked_crews": [blocked_user.crew_id for blocked_user in self.blocked_users],
            "missions": [mission.serialize() for mission in self.missions]
        }
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return {"message": "password saved"}
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)



class CrewUser(db.Model):
    __tablename__ = "crew_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    #foreign keys

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    crew_id: Mapped[int] = mapped_column(ForeignKey("crew.id"), nullable=False)


    #relationships

    user : Mapped["User"] = relationship("User", back_populates="crew_users")
    crew: Mapped["Crew"] = relationship("Crew", back_populates="crew_users")



    def serialize(self):
        return {
            "id": self.id,
            "joined_at": self.joined_at,
            "user_id": self.user_id,
            "crew_id": self.crew_id,
            "is_admin": self.is_admin
        }
    



class BlockedUser(db.Model):
    __tablename__ = "blocked_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    blocked_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)


    #foreign keys

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    crew_id: Mapped[int] = mapped_column(ForeignKey("crew.id"), nullable=False)

    
    #relationships

    user : Mapped["User"] = relationship("User", back_populates="blocked_users")
    crew: Mapped["Crew"] = relationship("Crew", back_populates="blocked_users")


    def serialize(self):
        return {
            "id": self.id,
            "blocked_at": self.blocked_at,
            "user_id": self.user_id,
            "crew_id": self.crew_id
        }
    



class Crew(db.Model):
    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at : Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now) 


    #relationships

      
    missions : Mapped[List["Mission"]] = relationship(back_populates="crew", cascade="all, delete-orphan")
    crew_users : Mapped[List["CrewUser"]] = relationship(back_populates="crew", cascade="all, delete-orphan")
    blocked_users : Mapped[List["BlockedUser"]] = relationship(back_populates="crew", cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "created_at": self.created_at
        }
    

    def get_info(self):
        return {
            "name": self.name,
            "created_at": self.created_at,
            "members": [member.user.username for member in self.crew_users],
            "members_id": [member.user.id for member in self.crew_users],
            "blocked_members":  [member.user.username for member in self.blocked_users],
            "blocked_members_id":  [member.user.id for member in self.blocked_users],
        }
    
    def get_admins(self):
        return {
            "admins": [
               { "username":member.user.username,
                "id": member.user.id}
                  for member in self.crew_users if member.is_admin
                ]      
        }
    
   
    



class Mission(db.Model):
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    completed_at : Mapped[datetime] = mapped_column(DateTime, nullable=True) 
    is_group : Mapped[bool] = mapped_column(Boolean, nullable=False, default=False) 


    #foreign keys

    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    crew_id : Mapped[int] = mapped_column(ForeignKey("crew.id"), nullable=True)

    #relationships

    user: Mapped["User"] = relationship("User", back_populates="missions")
    crew: Mapped["Crew"] = relationship("Crew", back_populates="missions")


    def serialize(self):
        return {
            "id" : self.id,
            "description": self.description,
            "completed_at": self.completed_at,
            "is_group": self.is_group
        }
    
    def get_owner(self):

        if self.is_group:
            return {
                "id": self.crew.id,
                "name": self.crew.name
            }
        elif(not self.is_group):
            return {
                "id": self.user.id,
                "email": self.user.email,
                "username": self.user.username 
            }

    



    
class ClaudeProgress(db.Model):
    __tablename__ = "claude_progress"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_missions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


    def get_progress(self):
        return {
            "id" : self.id,
            "total_missions": self.total_missions
        }
    
    def increase_progress(self,quantity):
        self.total_missions = self.total_missions + quantity
        return {"claude_progress": f"{self.total_missions}/10000"}