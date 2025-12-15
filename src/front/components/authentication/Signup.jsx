import { useEffect, useState } from "react"
import Swal from 'sweetalert2'
import { fetchSignup } from "../../services/authServices"
import { useNavigate } from "react-router-dom"
import { BACKEND_URL } from "../../main"


export const Signup = () => {

    const [seePassword, setSeePassword] = useState(false)
    const navigate = useNavigate()
    const [includeCM, setIncludeCM] = useState(true)
    const [oceanGod, setOceanGod] = useState(false)
    const [profilePhoto, setProfilePhoto] = useState("")
    const [seeConfirmPassword, setSeeConfirmPassword] = useState(false)
    const [formData, setFormData] = useState(
        {
            sailor_name: "",
            email: "",
            password: "",
            profile_photo: "",
            claude_mission_id: 1
        }
    )

    const uploadToCloudinary = async(file) => {
        const cloudinaryForm = new FormData()
        cloudinaryForm.append("image", file)


        const response = await fetch(`${BACKEND_URL}api/upload-image`,{
            method : "POST",
            body: cloudinaryForm
        })

        const data = await response.json()


        return data.secure_url


    }

    const handleProfilePhoto = async(event) =>{
        const file = event.target.files[0]
       
        const image = await uploadToCloudinary(file)
        setFormData({...formData, profile_photo: image})
        setProfilePhoto(image)
    }


    const handleChange = (event) => {

        const target = event.target
        const value = target.value
        const name = target.name
        if (name == "password") {
            if (value == "Clan1234!") {
                setOceanGod(true)
            } else {
                setOceanGod(false)
            }
        }
        setFormData({ ...formData, [name]: value })
    }


        const handleSubmit = async (event) => {
            event.preventDefault()
            const target = event.target
            const password = target[3].value
            const confirmPassword = target[5].value

            if (confirmPassword != password) {
                Swal.fire({
                    title: "Las contraseñas no coinciden",
                    confirmButtonText: "Intentar otra vez",
                    icon: "error"
                })
                return
            }

            const {claude_mission_id, ...resto} = formData

            const payload = includeCM ? formData : resto

            console.log(resto)
            console.log(payload)

            const response = await fetchSignup(payload)
            if (response.status == 200) {
                Swal.fire({
                    title: "Marinero creado correctamente",
                    confirmButtonText: "Vamos!",
                    icon: "success"
                }).then((result) => {
                    if (result.isConfirmed) {
                        navigate("/auth", {
                            state: {
                                login: true
                            }
                        })
                    }
                })
            } else if (response.status == 400) {
                Swal.fire({
                    title: "Ya existe un marinero con dicho email o nombre",
                    confirmButtonText: "Está bien",
                    icon: "error"
                })
            }

        }
    

        const handleCheckBox = (event) =>{
            setIncludeCM(event.target.checked)
        }

 

    return (
      
        <form onSubmit={handleSubmit}>
            {profilePhoto &&
            <div style={{width:"20rem"}}>
                <div className="ratio ratio-1x1">
                <img className="object-fit-cover" src={profilePhoto} alt="profilePhoto" />
                </div>
            </div>
            }
            <label>Foto de perfil</label>
            <input  onChange={handleProfilePhoto} type="file" ></input>
            <label>Nombre marinero</label>
            <input onChange={handleChange} name="sailor_name" type="text"></input>
            <label >Correo electrónico</label>
            <input onChange={handleChange} name="email" type="email"></input>
            <label>Contraseña</label>
            <input type={seePassword ? "text" : "password"} onChange={handleChange} name="password"></input>
            <button onClick={() => setSeePassword(prev => !prev)} type="button">Ojo</button>
            <label>Confirmar contraseña</label>
            <input type={seeConfirmPassword ? "text" : "password"}></input>
            <button onClick={() => setSeeConfirmPassword(prev => !prev)} type="button">Ojo</button>
            {oceanGod &&
                <>
                    <label>Incluir Claude mission</label>
                    <input onChange={handleCheckBox} checked={includeCM} type="checkbox"></input>
                </>
            }
            <button type="submit">Registrarse</button>
        </form>
    )
}
