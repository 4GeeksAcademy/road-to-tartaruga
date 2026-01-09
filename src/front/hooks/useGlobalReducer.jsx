import { useContext, useReducer, createContext } from "react";
import storeReducer, { initialStore } from "../store"
import Swal from 'sweetalert2'

const StoreContext = createContext()


export function StoreProvider({ children }) {

    const [store, dispatch] = useReducer(storeReducer, initialStore())

    const load = () => {
        dispatch({ type: "LOADING" })
    }

    const loadOff = () => {
        dispatch({ type: "LOADING_OFF" })
        Swal.close()
    }

    const redirect = () => {
        dispatch({ type: "REDIRECTING" })
    }
    const redirectOff = () => {
        dispatch({ type: "REDIRECTING_OFF" })
    }

    const openSwal = () => {
        dispatch({ type: "OPEN_SWAL" })
    }
    const closeSwal = () => {
        dispatch({ type: "CLOSE_SWAL" })
    }

    const values = {
        store,
        dispatch,
        load,
        loadOff,
        redirect,
        redirectOff,
        openSwal,
        closeSwal
    }


    return <StoreContext.Provider value={values}>
        {children}
    </StoreContext.Provider>
}

export default function useGlobalReducer() {
    const { dispatch, store, load, loadOff, redirect, redirectOff, openSwal, closeSwal } = useContext(StoreContext)
    return { dispatch, store, load, loadOff, redirect, redirectOff, openSwal, closeSwal };
}