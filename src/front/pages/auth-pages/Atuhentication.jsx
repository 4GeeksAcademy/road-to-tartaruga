import { useEffect, useState } from "react"
import { fetchLogin } from "../../services/authServices"
import Swal from 'sweetalert2'
import { Navigate, useLocation, useNavigate } from "react-router-dom"

export const Authentication = () => {

    const [seePassword, setSeePassword] = useState(false)
    const [formData, setFormData] = useState({ identificator: "", password: "" })
    const [checked, setChecked] = useState(false)

    const location = useLocation()

    const [login, setLogin] = useState(false)
    
    const navigate = useNavigate()

    


    useEffect(()=>{

       setLogin(location.state.login)

    },[location])



    const handleLoginSubmit = async (event) => {
        event.preventDefault()
        const fetchResponse = await fetchLogin(formData)
        if (fetchResponse.token) {


            const sailorName = fetchResponse.sailor_name
            const sailorId = fetchResponse.sailor_id
            const token = fetchResponse.token

            if (checked) {

                localStorage.setItem("sailorId", sailorId)
                localStorage.setItem("sailorName", sailorName)
                localStorage.setItem("token", token)
              

            } else {

                sessionStorage.setItem("sailorId", sailorId)
                sessionStorage.setItem("sailorName", sailorName)
                sessionStorage.setItem("token", token)
            }

            Swal.fire({
                icon:"success",
                title: "Bienvenido marinero",
                confirmButtonText: "Vamos!",
    
            }).then((result)=>{
                if(result.isConfirmed){
                    navigate("/")
                }
            })


        } else if (fetchResponse.message == "sailor not found") {
            Swal.fire({
                icon:"error",
                title: "Marinero no encontrado",
                confirmButtonText: "Acepto",
            }).then((result)=> console.log(result))
        } else if(fetchResponse.message == "invalid password"){
            Swal.fire({
                icon:"error",
                title: "Contraseña incorrecta",
                confirmButtonText: "Intentar otra vez",
            })
        }
    }


    const handleSignUpSubmit = async()=>{

    }



    const handleChange = (event) => {
        const target = event.target
        setFormData({ ...formData, [target.name]: target.value })
    }


    return (
        <div>
            <h1>{login ? "Ingreso" : "Registro"}</h1>
           {login ? <form onSubmit={handleLoginSubmit}>
                <label>Nombre marinero / email</label>
                <input name="identificator" onChange={handleChange} type="text" required />
                <label>Contraseña</label>
                <input name="password" onChange={handleChange} minLength="6" type={seePassword ? "text" : "password"} required ></input>
                <button type="button" onClick={() => setSeePassword(prev => !prev)}>Ojo</button>
                <label htmlFor="remember">Remember me</label>
                <input onChange={(e) => setChecked(e.target.checked)} id="remember" type="checkbox"></input>
                <button type="submit">Ingresar</button>
            </form>
            :
            <form>
            <label>Nombre marinero</label>
            <input type="text"></input>
            <label>Correo electrónico</label>
            <input type="email"></input>
            <label>Contraseña</label>
            <input type="password"></input>
            <label>Confirmar contraseña</label>
            <input type="password"></input>
            <button type="submit">Registrarse</button>
            </form>
                }
        </div>
    )
}