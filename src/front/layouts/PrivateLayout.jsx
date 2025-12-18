import { Outlet, useNavigate } from "react-router-dom/dist"
import ScrollToTop from "../components/ScrollToTop"
import { handleLogOut, Navbar } from "../components/Navbar"
import { Footer } from "../components/Footer"
import useGlobalReducer from "../hooks/useGlobalReducer"
import { useEffect } from "react"
import { fetchPrivate } from "../services/authServices"
import Swal from 'sweetalert2'

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const PrivateLayout = () => {

    const { dispatch, redirect, store } = useGlobalReducer()
    const navigate = useNavigate()
    const storage = localStorage.length == 0 ? sessionStorage : localStorage
    const token = storage.token


    const notSigned = () =>{
        redirect()
        setTimeout(()=>{
            navigate("/auth-need")
        }, 1000)
    }

    const privatePage = async (token) => {

        if(!token && !store.redirecting){
          
            notSigned()
            return
        }
       
        const fetchPrivatePage = await fetchPrivate(token)

        const data = await fetchPrivatePage.json()
        const expiredToken = data.message == "The token has expire, log in again"
        console.log(expiredToken)
        if(expiredToken){
            Swal.fire({
                title: "Tu sesion ha caducado",
                text : "Vuelve a iniciar sesion para continuar con tu aventura",
                icon:"warning",
                confirmButtonText: "Vamos!"
            }).then(response => {
                if(response.isConfirmed || response.isDismissed){
                    handleLogOut(dispatch)
                    navigate("/auth", {state:{
                        login: true
                    }})
                }
            })
        }

        // if (!fetchPrivatePage.ok  && !store.redirecting) {
        //     notSigned()
        // }
    }

    useEffect(() => {
        privatePage(token)
    }, [])

    useEffect(()=>{
        if(!store.login && !token){
            notSigned()
        }

    },[store.login])

    return (
        <ScrollToTop>
            <Navbar />
            <Outlet />
            <Footer />
        </ScrollToTop>
    )
}