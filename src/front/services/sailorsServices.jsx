import { BACKEND_URL } from "../main"

export const getSailor = async(sailor_id) =>{
    const response = await fetch(`${BACKEND_URL}api/sailors?sailor_id=${sailor_id}`)
    
    if(!response.ok){
        console.log({"error": `Error ${response.status}, ${response.statusText}`})
    }
    const data = await response.json()

    const sailorInfo = {
        email: data.email,
        sailorName: data.sailor_name,
        profilePhoto: data.profile_photo
    }

    return sailorInfo
}


export const editSailor = async(sailor_id) =>{
    const response = await fetch(`${BACKEND_URL}`)
}