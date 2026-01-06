import { useEffect, useState } from "react"
import { ObjectiveCard } from "./ObjectiveCard"

export const MissionModal = ({ mission: { title, description, objectives, id } }) => {

    const [completed, setCompleted] = useState(false)
    const [checks, setChecks] = useState(0)
    const [updatedObj, setUpdatedObj] = useState([])

    const handleChange = (event) => {
        const checked = event.target.checked
        if (checked) {
            setChecks(prev => prev + 1)
        } else {
            setChecks(prev => prev - 1)
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault()
       
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
                                {objectives.map((objective, index) => {

                                    return <li key={index} className="list-group-item">
                                                <label>{title}</label>
                                                <input defaultChecked={objective.completed_at ? true : false} onChange={handleChange} type="checkbox">
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
                            <button type="submit">Guardar</button>
                            <button data-bs-dismiss="modal" type="button">Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}