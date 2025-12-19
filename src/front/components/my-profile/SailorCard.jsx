import { useEffect, useState } from "react"
import useGlobalReducer from "../../hooks/useGlobalReducer"
import Swal from "sweetalert2"
import { fetchLogin } from "../../services/authServices"

export const SailorCard = () => {

    const { store } = useGlobalReducer()
    const { user } = store
    const [editProfile, setEditProfile] = useState(false)
    const [editPhoto, setEditPhoto] = useState(false)
    const [inputLink, setInputLink] = useState(false)
    const [inputFile, setInputFile] = useState(false)
    const [seeConfirmPassword, setSeeConfirmPassword] = useState(false)
    const [formData, setFormData] = useState({
        sailorName: user?.sailorName,
        email: user?.email,
        profilePhoto: user?.profilePhoto
    })

    const handleLinkButton = () => {
        setInputLink(true)
        setInputFile(false)
    }
    const handleFileButton = () => {
        setInputFile(true)
        setInputLink(false)
    }


    const handleSubmit = (event) => {
        event.preventDefault()
        console.log("Cambios enviados")
        console.log(formData)
    }

    const handleEditInfoBtn = () => {
        // setEditProfile(prev => !prev)
        // setEditPhoto(prev => prev == true ? false : prev)
        Swal.fire({
            title: "Confirmando identidad",
            input : "password",
            inputPlaceholder: "Ingresa tu contraseña",
            showCancelButton: true,
            confirmButtonText: "Confirmar",
            cancelButtonText: "Cancelar",
            inputValidator: value => {
                if(!value) return "No te olvides de escribir la contraseña"
            }
        }).then(response =>{
            if (response.isConfirmed){
               fetchLogin({identificator: user.email, password: response.value}).then(fetchResponse =>{
               if(fetchResponse.token){
                Swal.fire({
                    title: "Marinero confirmado",
                    icon: "success",
                    confirmButtonText: "Genial!"
                })
               } else {
                Swal.fire({
                    title: "Marinero no confirmado",
                    text: "Tal parece que no recuerdas tu contraseña",
                    icon: "error",
                    confirmButtonText: "Intentar otra vez"
                })
               }
               })
            }
        })
        }


    return (
            <div>
                <form onSubmit={handleSubmit}>

                    <div className="bg-dark">
                        <img src={user?.profilePhoto} />

                        <button type="button" disabled={!editProfile} onClick={() => {
                            setEditPhoto(prev => !prev)
                            setInputFile(false)
                            setInputLink(false)
                        }}>Cambiar foto</button>


                        <button onClick={handleLinkButton} type="button" disabled={!editPhoto || !editPhoto && inputLink}>Enlace</button>
                        <input type="text" placeholder="Ingresa url imagen" disabled={inputLink && editPhoto ? false : true}></input>
                        <button onClick={handleFileButton} type="button" disabled={!editPhoto || !editPhoto && inputLink}>Ordenador</button>
                        <input type="file" disabled={inputFile && editPhoto ? false : true} />
                    </div>
                    <input type="text" value={user?.sailorName || ""} disabled={!editProfile}></input>
                    <input type="text" value={user?.email || ""} disabled={!editProfile} ></input>
                    <button onClick={handleEditInfoBtn} type="button">Editar perfil</button>
                <button onClick={() => setEditProfile(false)} type="submit" disabled={!editProfile}>Confirmar</button>
                <button onClick={() => setEditProfile(false)} type="reset" disabled={!editProfile}>Cancelar</button>
            </form>
        </div >
    )
}