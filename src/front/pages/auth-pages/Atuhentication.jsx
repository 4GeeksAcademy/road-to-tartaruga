import { useEffect, useState } from "react"

import { Navigate, useLocation, useNavigate } from "react-router-dom"
import { Login } from "../../components/authentication/Login"
import { Signup } from "../../components/authentication/Signup"

export const Authentication = () => {

    const [seePassword, setSeePassword] = useState(false)
    const location = useLocation()
    const [login, setLogin] = useState(false)

    useEffect(() => {
        setLogin(location.state.login)
    }, [location])

    const handleSignUpSubmit = async () => {

    }

    return (
        <div>
            <h1>{login ? "Ingreso" : "Registro"}</h1>
            {login ? <Login />
                :
                <Signup />
            }
        </div>
    )
}