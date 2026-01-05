import { useEffect, useState } from "react"
import useGlobalReducer from "../../hooks/useGlobalReducer"
import { AddMissionModal } from "./AddMissionModal"
import { MissionLimitModal } from "./MissionLimitModal"

export const AddMissionComponent = () =>{

    const {store: {missions:{incompleted}}} = useGlobalReducer()
    const [missionsLimitReached, setMissionsLimitReached] = useState(false)
    


  useEffect(()=>{

    if(incompleted?.length >= 3){
        setMissionsLimitReached(true)
    }else{
        setMissionsLimitReached(false)
    }

  },[incompleted])


    return (
        <>
        <button type="button" data-bs-toggle="modal" data-bs-target={`#${missionsLimitReached ? "missionLimitModal" : "addMissionModal" }`}>Agregar</button>
            <AddMissionModal />
            <MissionLimitModal/>
        </>
    )
}