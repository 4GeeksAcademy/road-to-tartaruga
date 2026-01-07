
import { BACKEND_URL } from "../main"

export const changeObjectiveState = async(objectiveId) =>{
const response = await fetch(BACKEND_URL + `api/objectives/${objectiveId}/complete`,{
    method: "PATCH"
})

const data = await response.json()

return data.completed_at
}