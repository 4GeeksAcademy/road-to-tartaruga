import { Outlet, useNavigate } from "react-router-dom/dist"
import ScrollToTop from "../components/ScrollToTop"
import { Navbar } from "../components/Navbar"
import { Footer } from "../components/Footer"
import useGlobalReducer from "../hooks/useGlobalReducer"
import { useEffect } from "react"
import { fetchPrivate } from "../services/authServices"

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const PrivateLayout = () => {

    const {dispatch, load, store} = useGlobalReducer()
    const navigate = useNavigate()
    const storage = localStorage.length == 0 ? sessionStorage : localStorage
    const token = storage.token

    const privatePage = async(token)=> {
        load()
        const fetchPrivatePage = await fetchPrivate(token)
        load()
        if(!fetchPrivatePage && !store.loading){
            navigate("/auth-need")
        }
    }

    useEffect(()=>{
        privatePage(token)
    },[])

    return (
        <ScrollToTop>
            <Navbar />
                <Outlet />
            <Footer />
        </ScrollToTop>
    )
}