import { useEffect, useState } from "react"
import Swal from 'sweetalert2'
import { fetchSignup } from "../../services/authServices"
import { useNavigate } from "react-router-dom"
import { BACKEND_URL } from "../../main"
import useGlobalReducer from "../../hooks/useGlobalReducer"
import { uploadToCloudinary } from "../../services/cloudinaryServices"


export const Signup = () => {


    const { load } = useGlobalReducer()
    const [seePassword, setSeePassword] = useState(false)
    const navigate = useNavigate()
    const [includeCM, setIncludeCM] = useState(true)
    const [oceanGod, setOceanGod] = useState(false)
    const [profilePhoto, setProfilePhoto] = useState("")
    const [isPhotoFile, setIsPhotoFile] = useState(true)
    const [inputPhotoLink, setinputPhotoLink] = useState("")
    const [filePhotoLink, setFilePhotoLink] = useState("")
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

   

    const handleProfilePhoto = async (event) => {
        const selected = event.target.files[0]

        if (selected) {
            load()
            const image = await uploadToCloudinary(selected)
            load()
            setFormData({ ...formData, profile_photo: image })
            setProfilePhoto(image)
            setFilePhotoLink(image)
        }

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
        if (name == "profile_photo") {
            setProfilePhoto(value)
            setinputPhotoLink(value)
        }
    }


    const handleSubmit = async (event) => {
        event.preventDefault()
        const target = event.target
        const password = target[6].value
        const confirmPassword = target[8].value
       
        if (confirmPassword != password) {
            Swal.fire({
                title: "Las contraseñas no coinciden",
                confirmButtonText: "Intentar otra vez",
                icon: "error"
            })
            return
        }

        const profilePhoto = formData.profile_photo

        if(!profilePhoto){
            Swal.fire({
                title: "Elige una foto de perfil",
                confirmButtonText: "Está bien",
                icon: "question"
            })
            return
        }

        const { claude_mission_id, ...resto } = formData

        const payload = includeCM ? formData : resto


        load()
        const response = await fetchSignup(payload)
        await load()
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


    const handleCheckBox = (event) => {
        setIncludeCM(event.target.checked)
    }


    const handleLinkPhotoBtn = () => {
        setIsPhotoFile(false)
        setProfilePhoto("")
        setFormData((prev) => {
            return { ...prev, profile_photo: "" }
        })
    }

    const handleFilePhotoBtn = () => {
        setIsPhotoFile(true)
        setProfilePhoto(filePhotoLink)
        setinputPhotoLink("")
        setFormData((prev) => {
            return { ...prev, profile_photo: filePhotoLink }
        })
    }


    return (

        <form onSubmit={handleSubmit}>
            {profilePhoto &&
                <div style={{ width: "20rem" }}>
                    <div className="ratio ratio-1x1">
                        <img className="object-fit-cover"
                            src={profilePhoto}
                            alt="profilePhoto" />
                    </div>
                </div>
            }
            <label>Foto de perfil</label>
            <button
            type="button"
                onClick={handleFilePhotoBtn}>
                Usar foto
            </button>
            <label
                className="btn btn-primary"
                htmlFor="fileInput"
            >Subir</label>
            <input
                id="fileInput"
                className="d-none"
                onChange={handleProfilePhoto}
                type="file"
                disabled={!isPhotoFile}
            ></input>

            <button
                onClick={handleLinkPhotoBtn}
                type="button">
                Usar enlace
            </button>
            <input name="profile_photo"
                value={inputPhotoLink}
                onChange={handleChange}
                type="text"
                disabled={isPhotoFile}
            ></input>

            <label>Nombre marinero</label>
            <input onChange={handleChange} name="sailor_name" type="text" required></input>
            <label >Correo electrónico</label>
            <input onChange={handleChange} name="email" type="email" required></input>
            <label>Contraseña</label>
            <input type={seePassword ? "text" : "password"}
                onChange={handleChange}
                name="password"
                required
                ></input>
            <button onClick={() => setSeePassword(prev => !prev)}
                type="button">
                Ojo
            </button>
            <label>Confirmar contraseña</label>
            <input type={seeConfirmPassword ? "text" : "password"}></input>
            <button onClick={() => setSeeConfirmPassword(prev => !prev)}
                type="button">
                Ojo
            </button>
            {oceanGod &&
                <>
                    <label>Incluir Claude mission</label>
                    <input onChange={handleCheckBox}
                        checked={includeCM}
                        type="checkbox"></input>
                </>
            }
            <button type="submit">Registrarse</button>
        </form>
    )
}
