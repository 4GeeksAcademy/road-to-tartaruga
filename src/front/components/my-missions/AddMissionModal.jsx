import { useEffect, useState } from "react"
import Swal from "sweetalert2"
import { addSailorMission } from "../../services/missionsServices"
import useGlobalReducer from "../../hooks/useGlobalReducer"


export const AddMissionModal = () => {

    const [objectives, setObjectives] = useState([])
    const { sailorId } = localStorage.length == 0 ? sessionStorage : localStorage
    const { dispatch, load, loadOff } = useGlobalReducer()
    const [objectiveInput, setObjectiveInput] = useState("")
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        objectives
    })

    const handleObjectiveInput = (event) => {
        const value = event.target.value
        setObjectiveInput(value)
    }

    const handleChange = (event) => {
        const value = event.target.value
        const name = event.target.name
        setFormData({ ...formData, [name]: value })
    }


    const handleKeyDown = (event) => {
        if (event.key == "Enter") {
            event.preventDefault()
            setObjectives([...objectives, objectiveInput])
            setObjectiveInput("")
        }
    }

    const resetModalData = () => {
        setFormData({
            title: "",
            description: "",
            objectives: []
        })
        setObjectiveInput("")
        setObjectives([])
    }

    const handleDeleteObjective = (indexToDelete) => {
        const filteredObjectives = objectives.filter((_, index) => index != indexToDelete)
        setObjectives(filteredObjectives)
    }

    const handleSubmit = async (event) => {
        event.preventDefault()

        if (objectives.length < 2) {
            Swal.fire({
                title: "Deben haber al menos 2 objetivos por misión",
                icon: "warning"
            })
            return
        }
        load()
        const newMission = await addSailorMission(formData, sailorId)
        dispatch({ type: "ADD_MISSION", payload: newMission })
        loadOff()
    }

    useEffect(() => {
        setFormData({ ...formData, objectives })
    }, [objectives])

    return (
        <div className="modal fade" id="addMissionModal" tabIndex="-1" aria-hidden="true">
            <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                    <div className="modal-header">
                        <h1 className="modal-title fs-5">Agregar mision</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <form onSubmit={handleSubmit}>
                        <div className="modal-body">
                            <label htmlFor="title">Titulo</label>
                            <input value={formData.title} name="title" onChange={handleChange} className="form-control" id="title" type="text" required></input>

                            <label htmlFor="description">Descripción</label>
                            <input value={formData.description} name="description" onChange={handleChange} className="form-control" id="description" type="text" required></input>

                            <label htmlFor="title">Objetivos</label>
                            <input value={objectiveInput} onChange={handleObjectiveInput} onKeyDown={handleKeyDown} className="form-control" id="title" type="text"></input>


                            {objectives.map((objective, index) => {
                                return <div key={index} className="d-flex justify-content-between bg-secondary">
                                    <p>{objective}</p>
                                    <button type="button" onClick={() => handleDeleteObjective(index)} >X</button>
                                </div>
                            })}

                        </div>
                        <div className="modal-footer">
                            <button type="submit">Guardar</button>
                            <button type="button" data-bs-dismiss="modal" onClick={resetModalData}>Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

    )
}