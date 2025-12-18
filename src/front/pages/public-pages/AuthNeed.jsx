import { useEffect } from "react"
import useGlobalReducer from "../../hooks/useGlobalReducer"
import { fetchPrivate } from "../../services/authServices"
import { useNavigate } from "react-router-dom"

export const AuthNeed = () => {

    const { store} = useGlobalReducer()
    const navigate = useNavigate()

    useEffect(()=>{

        if(store.login){
           navigate(-1)   
        }

    },[store.login])
    
    return (
        <div>
            Hola, soy el componente Auth Need
        </div>
    )
}