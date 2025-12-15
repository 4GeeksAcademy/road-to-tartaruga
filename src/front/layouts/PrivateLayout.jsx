import { Outlet, useNavigate } from "react-router-dom/dist"
import ScrollToTop from "../components/ScrollToTop"
import { Navbar } from "../components/Navbar"
import { Footer } from "../components/Footer"
import useGlobalReducer from "../hooks/useGlobalReducer"
import { useEffect } from "react"

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const PrivateLayout = () => {

    const {store} = useGlobalReducer()
    const navigate = useNavigate()

    useEffect(()=>{
        if(!store.login){
            navigate("/auth-need")
        }
    })

    return (
        <ScrollToTop>
            <Navbar />
                <Outlet />
            <Footer />
        </ScrollToTop>
    )
}