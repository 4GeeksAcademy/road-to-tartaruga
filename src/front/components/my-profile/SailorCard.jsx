import { useEffect, useState } from "react"
import useGlobalReducer from "../../hooks/useGlobalReducer"

export const SailorCard = () => {

    const { store } = useGlobalReducer()
    const { user } = store
    const [editProfile, setEditProfile] = useState(false)
    const [editPhoto, setEditPhoto] = useState(false)
    const [inputLink, setInputLink] = useState(false)
    const [inputFile, setInputFile] = useState(false)
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


    const handleSubmit = (event)=>{
        event.preventDefault()
        console.log("Cambios enviados")
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>

                <div className="bg-dark">
                    <img src={user?.profilePhoto} />

                    <button type="button" disabled={!editProfile} onClick={() => setEditPhoto(prev => !prev)}>Cambiar foto</button>
                    <button type="button">Confirmar cambio</button>
                    <button type="button">Cancelar cambio</button>


                    <button onClick={handleLinkButton} type="button" disabled={!editPhoto || !editPhoto && inputLink}>Enlace</button>
                    <input type="text" placeholder="Ingresa url imagen" disabled={!inputLink}></input>
                    <button onClick={handleFileButton} type="button" disabled={!editPhoto || !editPhoto && inputLink}>Ordenador</button>
                    <input type="file" disabled={!inputFile} />
                </div>
                <input type="text" value={user?.sailorName || ""} disabled={!editProfile}></input>
                <input type="text" value={user?.email || ""} disabled={!editProfile} ></input>
                <button onClick={() => setEditProfile(prev => !prev)} type="button">Editar perfil</button>
                <button onClick={() => setEditProfile(false)} type="submit" disabled={!editProfile}>Confirmar</button>
                <button onClick={() => setEditProfile(false)} type="reset" disabled={!editProfile}>Cancelar</button>
            </form>
        </div>
    )
}