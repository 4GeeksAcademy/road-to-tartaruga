import { BACKEND_URL } from "../main"

 export const uploadToCloudinary = async (file) => {
        const cloudinaryForm = new FormData()
        cloudinaryForm.append("image", file)


        const response = await fetch(`${BACKEND_URL}api/upload-image`, {
            method: "POST",
            body: cloudinaryForm
        })

        const data = await response.json()

        return data.secure_url


    }


export const checkImageLink = async(url)=>{

    return await new Promise((resolve)=>{
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);
        img.src = url
    })
}