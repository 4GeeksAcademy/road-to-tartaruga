import { BACKEND_URL } from "../main"


export const fetchLogin = async (form) => {
    const response = await fetch(`${BACKEND_URL}api/auth/token`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
    })

    const data = await response.json()
    return data
}


export const fetchSignup = async (form) => {
    const response = await fetch(`${BACKEND_URL}api/sailors`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
    })

    return response
}


export const fetchPrivate = async (token) => {

        if(!token){
            console.log("No se ha enviado un token")
            return false
        }
        const response = await fetch(`${BACKEND_URL}api/auth/private`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })

       return response.ok
            
}