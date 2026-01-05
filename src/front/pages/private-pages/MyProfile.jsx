import { useEffect } from "react"
import { getSailor } from "../../services/sailorsServices"
import { SailorCard } from "../../components/my-profile/SailorCard"
import useGlobalReducer from "../../hooks/useGlobalReducer"

export const MyProfile = () => {

    const { sailorId } = localStorage.length != 0 ? localStorage : sessionStorage
    const { dispatch, load, loadOff, store } = useGlobalReducer()


    const saveSailorOnContext = async () => {

        if (sailorId) {
            load()
            const sailorInfo = await getSailor(sailorId)
            if (sailorInfo) {
                dispatch({ type: "SAVE_USER", payload: sailorInfo })
            }
            loadOff()
        }
    }

    useEffect(() => {
        saveSailorOnContext()
    }, [])

    return (
        <div>

            <SailorCard />
        </div>
    )
}