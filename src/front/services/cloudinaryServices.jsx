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