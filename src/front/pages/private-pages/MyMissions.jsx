import { useEffect } from "react"
import useGlobalReducer from "../../hooks/useGlobalReducer"
import { getSailorMissions } from "../../services/missionsServices"
import { MissionCard } from "../../components/my-missions/MissionCard"
import { AddMissionComponent } from "../../components/my-missions/AddMissionComponent"

export const MyMissions = () => {


    const { sailorId } = localStorage.length != 0 ? localStorage : sessionStorage

    const { store, dispatch, load, loadOff } = useGlobalReducer()

    const loadMissions = async () => {
        load()
        const missions = await getSailorMissions(sailorId)
        dispatch({ type: "SAVE_MISSIONS", payload: missions })
        loadOff()
    }



    useEffect(()=>{
        loadMissions()
    },[])


    return (
        <div>
            <button type="button">Hacer fetch misiones marinero</button>
            <p className="display-5">MISIONES</p>

            <AddMissionComponent/>

            <div>
                <h2>Incompletas</h2>
                {store.missions.incompleted?.map((mission,index) => {
                    return <MissionCard key={index}  color="danger" mission={mission} />
                })}
            </div>
            <div>
                <h2>Completas</h2>
                {store.missions.completed?.map((mission,index) => {
                    return <MissionCard key={index} color="success" mission={mission} />
                })}

            </div>
        </div>
    )
}