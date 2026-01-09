import { useEffect, useState } from "react"
import { MissionModal } from "./MissionModal"
import { completeMission } from "../../services/missionsServices"
import useGlobalReducer from "../../hooks/useGlobalReducer"
import Swal from "sweetalert2"


export const MissionCard = ({ store, mission, color }) => {

    const {sailorId} = localStorage.length ? localStorage : sessionStorage
    const {dispatch, load, loadOff,openSwal, closeSwal, store: {claudeMissionId, loading, swalClosed}} = useGlobalReducer()

    const handleCompleteMission = async (missionId) => {
        //Codigo para completar mision
        load()
        const newCompleted = await completeMission(sailorId, missionId, claudeMissionId)
        loadOff()
        
        if(newCompleted.message){
            console.log("newCompleted tiene message")
            if(newCompleted.message.includes("maximum")){
                if(swalClosed){
                    openSwal()
                    // setTimeout(()=>{
                        Swal.fire({
                            title: "Maximo diario alcanzado",
                            text: "Bien hecho marinero, has alcanzado el limite de misiones personales. A partir de mañana puedes seguir ayudando a Claude de forma personal, pero puedes intentar haciendolo ayudando a tu tripulación",
                            confirmButtonText: "Genial!"
                        }).then(()=>{
                            closeSwal()
                        })

                    // }, 5000)
                    
                }
            }
        }
        // dispatch({type: "COMPLETE_MISSION", payload: {missionId, newCompleted}})
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
