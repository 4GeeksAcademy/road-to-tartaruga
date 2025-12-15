import { useEffect, useState } from "react"
import Swal from 'sweetalert2'
export const Signup = () => {

    const [seePassword, setSeePassword] = useState(false)
    const [seeConfirmPassword, setSeeConfirmPassword] = useState(false)
    const [formData, setFormData] = useState(
        {
            sailor_name: "",
            email: "",
            password: "",
            claude_mission_id: 1
        }
    )


    const handleChange = (event) =>{

        const target = event.target
        const value = target.value
        const name = target.name

        setFormData({...formData, [name] : value})
    }


    const handleSubmit = (event) =>{
        event.preventDefault()
        const target = event.target
        const password = target[2].value
        const confirmPassword = target[4].value
    
        if(confirmPassword != password){
            Swal.fire({
                title: "Las contraseñas no coinciden",
                confirmButtonText : "Intentar otra vez",
                icon: "error"
            })
        }


    }
 
    useEffect(()=>{

        // console.log("se ha modificado formData --> ", formData);
        
    },[formData])

    return (
        <form onSubmit={handleSubmit}>
            <label>Nombre marinero</label>
            <input onChange={handleChange} name="sailor_name" type="text"></input>
            <label >Correo electrónico</label>
            <input onChange={handleChange} name="email" type="email"></input>
            <label>Contraseña</label>
            <input type={seePassword ? "text": "password"} onChange={handleChange} name="password"></input>
            <button onClick={()=> setSeePassword(prev => !prev)} type="button">Ojo</button>
            <label>Confirmar contraseña</label>
            <input type={seeConfirmPassword ? "text": "password"}></input>
            <button onClick={()=> setSeeConfirmPassword(prev => !prev)} type="button">Ojo</button>
            <button type="submit">Registrarse</button>
        </form>
    )
}