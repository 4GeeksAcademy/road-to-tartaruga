import { useState } from "react"
import { useNavigate } from "react-router-dom"
import Swal from 'sweetalert2'
import { fetchLogin } from "../../services/authServices"
import useGlobalReducer from "../../hooks/useGlobalReducer"

export const Login = () => {
    const [seePassword, setSeePassword] = useState(false)
    const {dispatch, load, loadOff} = useGlobalReducer()

    const [formData, setFormData] = useState({ identificator: "", password: "" })
    const [checked, setChecked] = useState(false)
    const navigate = useNavigate()

    const handleSubmit = async (event) => {
        event.preventDefault()
        load()
        const fetchResponse = await fetchLogin(formData)
        loadOff()
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

            const isOceanGod = fetchResponse.is_ocean_god

            Swal.fire({
                icon: "success",
                title: `Bienvenido ${isOceanGod ? "señor Dios del Oceano!": "querido Marinero!"}`,
                confirmButtonText: "Vamos!",

            }).then((result) => {
                if (result.isConfirmed) {
                    dispatch({type:"login", payload: true})
                    
                    navigate("/")
                }
            })


        } else if (fetchResponse.message == "sailor not found") {
            Swal.fire({
                icon: "error",
                title: "Marinero no encontrado",
                confirmButtonText: "Acepto",
            })
        } else if (fetchResponse.message == "invalid password") {
            Swal.fire({
                icon: "error",
                title: "Contraseña incorrecta",
                confirmButtonText: "Intentar otra vez",
            })
        }
    }

    const handleChange = (event) => {
        const target = event.target
        setFormData({ ...formData, [target.name]: target.value })
    }

    return (
        <form onSubmit={handleSubmit}>
            <label>Nombre marinero / email</label>
            <input name="identificator" onChange={handleChange} type="text" required />
            <label>Contraseña</label>
            <input name="password" onChange={handleChange} minLength="6" type={seePassword ? "text" : "password"} required ></input>
            <button type="button" onClick={() => setSeePassword(prev => !prev)}>Ojo</button>
            <label htmlFor="remember">Remember me</label>
            <input onChange={(e) => setChecked(e.target.checked)} id="remember" type="checkbox"></input>
            <button type="submit">Ingresar</button>
        </form>
    )
}