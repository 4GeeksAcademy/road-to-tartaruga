import { useEffect, useState } from "react"
import { MissionModal } from "./MissionModal"


export const MissionCard = ({ mission, color }) => {

    const handleCompleteMission = async () => {
        //Codigo para completar mision
        //Va con la funcion en el archivo missionsServices
        //La cual hace fetch y completa la mision en el back
    }

    const [formFields, setFormFields] = useState([])
    const [objectivesFields, setObjectivesFields] = useState([])

    const [completed, setCompleted] = useState(false)

    const objectivesCompleted = () => {

        const result = mission?.objectives?.map((objective) => {
            return objective.completed_at
        })

        const finalResult = !result.includes(null)
        return finalResult
    }

    useEffect(() => {

        setCompleted(objectivesCompleted())

        mission?.objectives?.forEach((objective) => {
            setFormFields(prev => ([...prev, {...objective, completed_at : objective.completed_at ? true : false}]))
            setObjectivesFields(prev => ([...prev, {...objective, completed_at : objective.completed_at ? true : false}]))
        })
    }, [])



    return (

        <div className="card" style={{ width: "18rem" }}>
            <div className={`card-body bg-${color}`}>
                <h5 data-bs-target={`#missionModal${mission.id}`} data-bs-toggle="modal" className="card-title">{mission?.title}</h5>
            </div>
            <div className="card-footer">
                <button className="btn btn-primary" onClick={handleCompleteMission} disabled={!completed}>Completar</button>
            </div>
            <button onClick={() => console.log("objectives es -->", mission.objectives)} type="button">Ver objectivos</button>
            <MissionModal objectivesFields={objectivesFields} formFields={formFields} setFormFields={setFormFields} mission={mission} />
        </div>
    )
}
