import { BACKEND_URL } from "../main"

export const getSailorMissions = async(sailorId) =>{
    const response = await fetch(`${BACKEND_URL}api/missions/sailor/${sailorId}`)

    if(response.ok){
        const data = await response.json()
        return data.missions
    }else{
        console.log("Error fetch getSailorMissions")
    }
}



export const addSailorMission = async(formData, sailorId)=>{

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    }

    const response = await fetch(`${BACKEND_URL}api/missions/sailor/${sailorId}`, options)
        const data = await response.json()
        return data
    
}