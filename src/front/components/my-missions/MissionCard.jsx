import { useEffect, useState } from "react"
import { MissionModal } from "./MissionModal"


export const MissionCard = ({mission, color}) => {

    const handleCompleteMission = async() =>{
        //Codigo para completar mision
        //Va con la funcion en el archivo missionsServices
        //La cual hace fetch y completa la mision en el back
    }

    const [completed, setCompleted] = useState(false)

    const objectivesCompleted  = ()=>{

        const result =  mission?.objectives?.map((objective)=>{
            return objective.completed_at
        })
    
        const finalResult = !result.includes(null)
        return !result.includes(null)
    }

    useEffect(()=>{
     setCompleted(objectivesCompleted())
    },[])
 
    return (
        
        <div  className="card" style={{ width: "18rem" }}>
            <div className={`card-body bg-${color}`}>
                <h5 data-bs-target={`#missionModal${mission.id}`} data-bs-toggle="modal"  className="card-title">{mission?.title}</h5>
            </div>
            <div className="card-footer">
                <button className="btn btn-primary" onClick={handleCompleteMission} disabled={!completed}>Completar</button>
            </div>
            <button onClick={()=> console.log("objectives es -->", mission.objectives)} type="button">Ver objectivos</button>
            <MissionModal mission={mission} />
        </div>
    )
}

 //Comento este codigo, para ver si una vez hecho el modal
 //Esta es necesaria para sacar informacion

{/* <ul className="list-group">
    {mission.objectives.map((objective,index) => {
        return <ObjectiveCard key={index} objective={objective} />
    })}
</ul> */} 