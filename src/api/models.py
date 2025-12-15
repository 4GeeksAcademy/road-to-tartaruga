from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, select, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import timezone
import datetime
from typing import List
from api.extensions import bcrypt
from api.extensions import db
from flask import jsonify
import enum
import string
import random



class Sailor(db.Model):
    __tablename__ = "sailor"

    id: Mapped[int] = mapped_column(primary_key=True)
    sailor_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    is_ocean_god : Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    profile_photo : Mapped[str] = mapped_column(String(200), nullable=False)

    #relationships

    crew_sailors : Mapped[List["CrewSailor"]] = relationship(back_populates="sailor")
    contributions : Mapped[List["Contribution"]] = relationship(back_populates="sailor", cascade="all, delete-orphan")
    created_crews : Mapped[List["Crew"]] = relationship(back_populates="creator")
    created_missions : Mapped[List["Mission"]] = relationship(foreign_keys="Mission.creator_id", back_populates="creator")
    missions : Mapped[List["Mission"]] = relationship(foreign_keys="Mission.sailor_owner_id", back_populates="sailor_owner", cascade="all, delete-orphan")
    assigned_objectives: Mapped[List["Objective"]] = relationship(back_populates="assigned_to")
    claude_missions_created: Mapped[List["ClaudeMission"]] = relationship(back_populates="creator")



    def serialize(self):

        return {
            "id": self.id,
            "sailor_name": self.sailor_name,
            "email": self.email,
            "is_ocean_god": self.is_ocean_god,
            "crews": [crew_sailor.crew.get_basic_info() for crew_sailor in self.crew_sailors],
            "missions" : self.get_missions_by_state(),
            "assigned_objectives": self.get_assigned_objectives(),
            "profile_photo": self.profile_photo
        }
        

    def set_password(self, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.password_hash = hashed_password

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_basic_info(self):
        return{
            "id": self.id,
            "sailor_name": self.sailor_name,
            "email": self.email,
            "is_ocean_god": self.is_ocean_god,
            "profile_photo": self.profile_photo
        }

    def get_contributions(self):
        return {
            "contributions": [contribution.get_basic_info() for contribution in self.contributions if contribution.contributed_points > 0]
        }

    def get_created_crews(self):
        return {
            "created_crews": [crew.get_basic_info() for crew in self.created_crews]
        }
    
    def get_created_missions(self):
        return {
            "individual": [mission.get_basic_info() for mission in self.created_missions if mission.sailor_owner],
            "crews": [mission.serialize() for mission in self.created_missions if mission.crew_owner],
            "claude_missions": [claude_mission.get_basic_info() for claude_mission in self.claude_missions_created]
        }

    def get_missions_by_state(self):
        return {
            "missions":
                { "completed": [mission.get_basic_info() for mission in self.missions if mission.completed_at],
                  "incompleted": [mission.get_basic_info() for mission in self.missions if not mission.completed_at]}
                 }
    
    def get_assigned_objectives(self):
        return {
            "individuals": {
                "completed": [objective.get_basic_info() for objective in self.assigned_objectives if objective.is_crew is False and objective.completed_at is not None],
                "incompleted": [objective.get_basic_info() for objective in self.assigned_objectives if objective.is_crew is False and objective.completed_at is  None]
            },
            "crews" : 
            {"completed":  [objective.serialize() for objective in self.assigned_objectives if objective.is_crew is not False and objective.completed_at is not None] ,
             "incompleted": [objective.serialize() for objective in self.assigned_objectives if objective.is_crew is not False and objective.completed_at is  None]}
           
            }

    def get_crews(self):
        return {
            "crews": [
                crew_sailor.get_crew() for crew_sailor in self.crew_sailors
            ]
        }



#Funciones para generar codigo de Crew -------------------------

def generate_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(8))
    
def get_unique_crew_code():
    while True:
        code = generate_code()
        exist_code = db.session.execute(select(Crew).where(Crew.code == code)).scalars().first()
        if not exist_code: 
            return code
            
#---------------------------------------------

class Crew(db.Model):

    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, default=get_unique_crew_code)

    #foreign keys
    creator_id: Mapped[int]= mapped_column(ForeignKey("sailor.id"), nullable=True)
    creator_name : Mapped[str] = mapped_column(String(120), nullable=False)

    #relationships

    contributions : Mapped[List["Contribution"]] = relationship(back_populates="crew")
    crew_sailors : Mapped[List["CrewSailor"]] = relationship(back_populates="crew", cascade="all, delete-orphan")
    missions : Mapped[List["Mission"]] = relationship(back_populates="crew_owner")

    creator: Mapped["Sailor"] = relationship(back_populates="created_crews")



    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "crew_sailors": [crew_sailor.sailor.sailor_name for crew_sailor in self.crew_sailors],
            "crew_sailors_id": [sailor.sailor.id for sailor in self.crew_sailors],
            "contributions": [contribution.get_basic_info() for contribution in self.contributions],
            "missions": self.get_missions_by_state(),
            "creator_id": self.creator_id,
            "code": self.code
        } 
    
    
    def get_basic_info(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def get_contributions(self):
        return {
            "contributions": [contribution.get_basic_info() for contribution in self.contributions]
        }
    

    def get_crew_sailors(self):
        return {
            "crew_sailors": [crew_sailor.get_sailor() for crew_sailor in self.crew_sailors]
        }

    def get_missions_by_state(self):
        return{
            "missions":{
                "completed": [mission.get_basic_info() for mission in self.missions if mission.completed_at],
                "incompleted": [mission.get_basic_info() for mission in self.missions if not mission.completed_at]
                }
        }
    




class CrewSailorStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    KICKED = "kicked"



class CrewSailor(db.Model):


    __tablename__= "crew_sailor"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_captain: Mapped[bool] = mapped_column(Boolean(), default=False)
    joined_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.datetime.now(timezone.utc))


    #foreign keys
    sailor_id: Mapped[int] = mapped_column(ForeignKey("sailor.id"))
    crew_id: Mapped[int] = mapped_column(ForeignKey("crew.id"))
    status: Mapped[CrewSailorStatus] = mapped_column(Enum(CrewSailorStatus, name="crew_sailor_status"), default=CrewSailorStatus.ACTIVE, nullable= False)
    
    
    #relationships
    sailor: Mapped["Sailor"] = relationship(back_populates="crew_sailors")
    crew: Mapped["Crew"] = relationship(back_populates="crew_sailors")

    

    def serialize(self):
        return{
            "id": self.id,
            "is_captain": self.is_captain,
            "sailor_id": self.sailor_id,
            "crew_id": self.crew_id,
            "joined_at" : self.joined_at.isoformat(),
            "status": self.status.value
        }
    
    def get_crew(self):
        return {
            "crew": self.crew.name,
            "crew_id": self.crew_id,
            "joined_at": self.joined_at.isoformat()
        }
    
    def get_sailor(self):
        return{
            "sailor": self.sailor.sailor_name,
            "sailor_id": self.sailor_id,
            "joined_at": self.joined_at.isoformat()
        }


    
class Mission(db.Model):

    __tablename__="mission"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(245), unique=True, nullable=False)
    completed_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    #foreign keys
    creator_id: Mapped[int]= mapped_column(ForeignKey("sailor.id"))
    sailor_owner_id : Mapped[int] = mapped_column(ForeignKey("sailor.id"), nullable=True)
    crew_owner_id : Mapped[int] = mapped_column(ForeignKey("crew.id"), nullable=True)


    #relationships
    creator: Mapped["Sailor"] = relationship(foreign_keys=[creator_id], back_populates="created_missions")
    sailor_owner: Mapped["Sailor"] = relationship(foreign_keys=[sailor_owner_id], back_populates="missions")
    crew_owner: Mapped["Crew"] = relationship(back_populates="missions")
    
    objectives: Mapped[List["Objective"]] = relationship(back_populates="mission", cascade="all, delete-orphan")



    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "owner": self.sailor_owner.sailor_name if self.sailor_owner else self.crew_owner.name,
            "owner_id": self.sailor_owner_id if self.sailor_owner_id else self.crew_owner_id,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    def get_basic_info(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    def get_objectives(self):
        return{
            "objectives": [objective.get_info_for_mission() for objective in self.objectives]
        }






class Objective(db.Model):
    

    __tablename__="objective"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    is_crew: Mapped[bool]= mapped_column(Boolean(), default=False)
    completed_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # foreign keys
    
  
    mission_id : Mapped[int] = mapped_column(ForeignKey("mission.id"), nullable=False)
    assigned_to_id : Mapped[int] = mapped_column(ForeignKey("sailor.id"), nullable=True)
    

    #relationships

    mission: Mapped["Mission"] = relationship(back_populates="objectives")
    assigned_to: Mapped["Sailor"] = relationship(back_populates="assigned_objectives")

    
   
    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "is_crew": self.is_crew,
            "owner": self.mission.sailor_owner.sailor_name if self.mission.sailor_owner else self.mission.crew_owner.name,
            "assigned_to_id": self.assigned_to_id,
            "mission_id": self.mission_id,
            "mission_title": self.mission.title
        }
    

    def get_basic_info(self):
        return {
            "id": self.id,
            "title": self.title,
            "mission_title": self.mission.title,
            "mission_id": self.mission_id,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    

    def get_info_for_mission(self):
        return{
            "title": self.title,
            "assigned_to": self.assigned_to_id,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


    def get_crew_id_owner(self):
        return self.mission.crew_owner_id


class ClaudeMission(db.Model):

    __tablename__="claude_mission"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(String(245), nullable=False)
    objective: Mapped[str]= mapped_column(String(120), nullable=False)
    scrolls : Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    #foreign keys

    creator_id: Mapped[int] = mapped_column(ForeignKey("sailor.id"), nullable=False)


    #relationships
    contributions: Mapped[List["Contribution"]] = relationship(back_populates="claude_mission")
    creator: Mapped["Sailor"] = relationship(back_populates="claude_missions_created")


    def serialize(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "objective": self.objective,
            "scrolls": self.scrolls
        }
    
    def get_contributions(self):
        return {
            "contributions": [contribution.get_basic_info() for contribution in self.contributions]
        }
    
    def get_basic_info(self):
        return {
            "title": self.title,
            "description": self.description
        }



    


class Contribution(db.Model):


    __tablename__= "contribution"

    id: Mapped[int] = mapped_column(primary_key=True)
    contribution: Mapped[int] = mapped_column(Integer, default=0)
    is_crew: Mapped[bool] = mapped_column(Boolean(), default=False)


    #foreign keys
    sailor_id: Mapped[int] = mapped_column(ForeignKey("sailor.id"), nullable=True)
    crew_id: Mapped[int] = mapped_column(ForeignKey("crew.id"), nullable=True)
    claude_mission_id: Mapped[int] = mapped_column(ForeignKey("claude_mission.id"), nullable=False)
    
    
    #relationships
    sailor: Mapped["Sailor"] = relationship(back_populates="contributions")
    crew: Mapped["Crew"] = relationship(back_populates="contributions")
    claude_mission: Mapped["ClaudeMission"] = relationship(back_populates="contributions")
    


    def serialize(self):

        contributor = self.sailor if not self.is_crew else self.crew

        return{
            "id": self.id,
            "contributed_scrolls": self.contributed_scrolls,
            "contributor": contributor.sailor_name if not self.is_crew else contributor.name,
            "contributor_id": contributor.id,
            "is_crew": self.is_crew
        }
    
    def get_basic_info(self):
        return {
            "claude_mission": self.claude_mission.get_basic_info(),
            "contribution": self.contribution,
            "objective": self.claude_mission.objective
        }
    
    def increase_contribution_crew(self):
        self.contribution = self.contribution + 10
        db.session.commit()
        return {"contribution": self.contribution}
    
    def increase_contribution_sailor(self):
        self.contribution = self.contributions + 1
        db.session.commit()
        return {"contribution": self.contribution}



