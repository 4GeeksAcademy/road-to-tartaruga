import { useEffect, useState } from "react"
import useGlobalReducer from "../../hooks/useGlobalReducer"
import Swal from "sweetalert2"
import { checkPassword, fetchLogin } from "../../services/authServices"
import { editSailor } from "../../services/sailorsServices"
import { checkImageLink, uploadToCloudinary } from "../../services/imagesServices"

export const SailorCard = () => {

    const { store, load, loadOff } = useGlobalReducer()
    const { user } = store
    const { sailorId: sailor_id } = localStorage.length != 0 ? localStorage : sessionStorage
    const [editProfile, setEditProfile] = useState(false)
    const [editPhoto, setEditPhoto] = useState(false)
    const [inputLink, setInputLink] = useState(false)
    const [inputFile, setInputFile] = useState(false)
    const [inputLinkUrl, setInputLinkUrl] = useState("")
    const [inputFileUrl, setInputFileUrl] = useState("")

    const [imageUrl, setImageUrl] = useState("")

    const [formData, setFormData] = useState({
        sailor_id,
        sailor_name: "",
        email: "",
        profile_photo: ""
    })

    const resetFormData = ()=>{
         setFormData({
               sailor_id: sailor_id,
                sailor_name: user?.sailorName,
                email: user?.email,
                profile_photo: user?.profilePhoto
            })
    }

    const handleLinkButton = () => {
        setInputLink(true)
        setInputFile(false)
    }
    const handleFileButton = () => {
        setInputFile(true)
        setInputLink(false)
    }


    const handleSubmit = async (event) => {
        event.preventDefault()
      
        const fetchEdit = await editSailor(formData)
        const data = await fetchEdit.json()
        const status = fetchEdit.status


        if (status === 409) {
            const existSailorName = data.message.includes("sailor_name")
            const existEmail = data.message.includes("email")
            const existBoth = existSailorName && existEmail
            const sameInfo = data.message.includes("different information")

            if (existBoth) {
                Swal.fire({
                    title: "Error al actualizar email y nombre de marinero",
                    text: "Email y nombre de Marinero en uso",
                    icon: "error",
                    confirmButtonText: "Intentar otra vez"
                })
            } else if (existSailorName) {
                Swal.fire({
                    title: "Error al actualizar nombre de marinero",
                    text: "Nombre de marinero en uso",
                    icon: "error",
                    confirmButtonText: "Intentar otra vez"
                })
            } else if (existEmail) {
                Swal.fire({
                    title: "Error al actualizar email",
                    text: "Email en uso",
                    icon: "error",
                    confirmButtonText: "Intentar otra vez"
                })
            
            }else if(sameInfo){
                Swal.fire({
                    title: "Sin cambios para guardar",
                    text : "No hay cambios en tu perfil, realiza alguno para actualizar tu informacion",
                    icon: "info",
                    confirmButtonText: "Entendido"
                })
            }
        } 

   
        

    }

    const handleEditInfoBtn = () => {
        // setEditProfile(prev => !prev)
        // setEditPhoto(prev => prev == true ? false : prev)
        Swal.fire({
            title: "Confirmando identidad",
            input: "password",
            inputPlaceholder: "Ingresa tu contraseña",
            showCancelButton: true,
            confirmButtonText: "Confirmar",
            cancelButtonText: "Cancelar",
            inputValidator: value => {
                if (!value) return "No te olvides de escribir la contraseña"
            }
        }).then(response => {
            if (response.isConfirmed) {
                checkPassword({ email: user.email, password: response.value }).then(fetchResponse => {
                    if (fetchResponse.status == 200) {
                        Swal.fire({
                            title: "Marinero confirmado",
                            icon: "success",
                            confirmButtonText: "Genial!"
                        }).then(response => {
                            if (response.isConfirmed || response.isDismissed) {
                                setEditProfile(true)
                            }
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

    useEffect(() => {
        resetFormData()
    }, [user])


    const handleChange = (event) => {
        const name = event.target.name
        const value = event.target.value
        setFormData({ ...formData, [name]: value })
    }

    const handleChangeImg = async(type, event) =>{
        if(type === "file"){
            const selected = event.target.files[0]

            if(selected){
                load()
                const image = await uploadToCloudinary(selected)
                loadOff()
                setInputFileUrl(image)
            }
           
        }else if(type === "link"){
            const url = event.target.value
            setInputLinkUrl(url)
        }
    }

    const handleCancelImg = ()=>{
        resetFormData()
        setEditPhoto(false)
        setInputFileUrl("")
        setInputLinkUrl("")
    }

    useEffect(()=>{

        console.log(inputFileUrl)

    },[inputFileUrl])

    const handleConfirmImg = () =>{
        setEditPhoto(false)
    }

    const handleReset = () => {
        setEditProfile(false)
        resetFormData()
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className="bg-dark">
                    <img src={formData.profile_photo} />
                    <button type="button" disabled={!editProfile || editPhoto} onClick={() => {
                        setEditPhoto(prev => !prev)
                        setInputFile(false)
                        setInputLink(false)
                    }}>Cambiar foto</button>

                    <button onClick={handleConfirmImg} type="button" disabled={!editPhoto}>Confirmar imagen</button>

                    <button onClick={handleCancelImg} type="button" disabled={!editPhoto}>Cancelar imagen</button>

                    <button onClick={handleLinkButton} type="button" disabled={!editPhoto || !editPhoto && inputLink}>Enlace</button>
                    <input onChange={(event)=>handleChangeImg("link", event)}  value={inputLinkUrl} type="text" placeholder="Ingresa url imagen" disabled={inputLink && editPhoto ? false : true}></input>
                    <button onClick={handleFileButton} type="button" disabled={!editPhoto || !editPhoto && inputLink}>Ordenador</button>
                    <input onChange={(event)=> handleChangeImg("file", event)} type="file" disabled={inputFile && editPhoto ? false : true} />
                </div>
                <input type="text" onChange={handleChange} name="sailor_name" value={formData.sailor_name || ""} disabled={!editProfile}></input>
                <input type="text" onChange={handleChange} name="email" value={formData.email || ""} disabled={!editProfile} ></input>
                <button onClick={handleEditInfoBtn} type="button" disabled={editProfile} >Editar perfil</button>
                <button type="submit" disabled={!editProfile || editPhoto} >Confirmar</button>
                <button onClick={handleReset} type="reset" disabled={!editProfile || editPhoto}>Cancelar</button>
            </form>
        </div>
    )
}