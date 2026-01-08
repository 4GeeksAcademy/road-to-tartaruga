import { useEffect, useState } from "react"
import { ObjectiveCard } from "./ObjectiveCard"
import { changeObjectiveState } from "../../services/objectivesServices"
import useGlobalReducer from "../../hooks/useGlobalReducer"

export const MissionModal = ({ objectivesFields, formFields, setFormFields, mission: { title, description, objectives, id } }) => {

    const [completed, setCompleted] = useState(false)
    const [checks, setChecks] = useState(0)
    const {dispatch, load, loadOff} = useGlobalReducer()

 
    const handleChange = (event) => {
        
        const id = event.target.id
        const checked = event.target.checked
        if (checked) {
            setChecks(prev => prev + 1)
        } else {
            setChecks(prev => prev - 1)
        }
        setFormFields(prev =>{
            return prev?.map((element)=>{
                if(element.id == id){
                    return {...element, completed_at : checked}
                }
                return element
            })
        })
    }

        

    const resetFormFields = () =>{
        setFormFields(objectivesFields.map(o => ({...o})))
    }

    const handleSubmit = async(event) => {
       
        event.preventDefault()

        objectivesFields.forEach(async(original, index)=>{
            
            const current = formFields.find(field => field.id === original.id)

            if(!current) return

            if(original.completed_at != current.completed_at){
               
                load()
                const completedAt = await changeObjectiveState(original.id)
                dispatch({type: "UPDATE_OBJECTIVE", payload: {missionId: id, completedAt, objectiveId: original.id}})
                loadOff()
                
            }
        })
    }

    useEffect(() => {
        objectives.forEach((objective) => {
            if (objective.completed_at) {
                setChecks(prev => prev + 1)
            }
        })
    }, [])



    return (
        <div className="modal fade" id={`missionModal${id}`} tabIndex="-1" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <form onSubmit={handleSubmit}>
                        <div className="modal-body bg-light">

                            <h1 className="modal-title fs-3">{title}</h1>
                            <p>{description}</p>

                            <ul className="list-group">
                                {formFields.map((objective, index) => {
                                    return <li key={index} className="list-group-item">
                                                <label>{objective?.title}</label>
                                                <input id={objective?.id} checked={objective?.completed_at ? true : false} onChange={handleChange} type="checkbox">
                                                </input>
                                            </li>
                                })}
                            </ul>

                            {completed && <div className="alert alert-success" role="alert">
                                <h3>Mision completada</h3>
                                <p>Bien hecho, guarda los cambios y marcala como completa, sigue asi marinero!</p>
                            </div>}
                        </div>
                        <div className="modal-footer">
                            <button data-bs-dismiss="modal" type="submit">Guardar</button>
                            <button onClick={resetFormFields} data-bs-dismiss="modal" type="button">Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}