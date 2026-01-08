import { useEffect, useState } from "react"
import { MissionModal } from "./MissionModal"
import { completeMission } from "../../services/missionsServices"
import useGlobalReducer from "../../hooks/useGlobalReducer"


export const MissionCard = ({ store, mission, color }) => {

    const {sailorId} = localStorage.length ? localStorage : sessionStorage
    const {store: {claudeMissionId}} = useGlobalReducer()

    const handleCompleteMission = async (missionId) => {
        //Codigo para completar mision
        await completeMission(sailorId, missionId, claudeMissionId)
        //Va con la funcion en el archivo missionsServices
        //La cual hace fetch y completa la mision en el back
    }

    const [formFields, setFormFields] = useState([])
    const [objectivesFields, setObjectivesFields] = useState([])

    const [completed, setCompleted] = useState(false)

  

    useEffect(() => {     


        
        const initial = mission.objectives.map((objective)=>{
            return {...objective, completed_at : !!objective.completed_at}
        })
        
        setObjectivesFields(initial)
        setFormFields(initial.map(o=> ({...o})))
        setCompleted(!initial.some(o => !o.completed_at))

    }, [store])


  


    



    return (

        <div className="card" style={{ width: "18rem" }}>
            <div className={`card-body bg-${color}`}>
                <h5 data-bs-target={`#missionModal${mission.id}`} data-bs-toggle="modal" className="card-title">{mission?.title}</h5>
            </div>
            <div className="card-footer">
                <button className="btn btn-primary" onClick={()=>handleCompleteMission(mission.id)} disabled={!completed}>Completar</button>
            </div>
            <MissionModal objectivesFields={objectivesFields} formFields={formFields} setFormFields={setFormFields} mission={mission} />
        </div>
    )
}
