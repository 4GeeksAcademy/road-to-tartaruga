import { useContext, useReducer, createContext } from "react";
import storeReducer, { initialStore } from "../store"  


const StoreContext = createContext()


export function StoreProvider({ children }) {
   
    const [store, dispatch] = useReducer(storeReducer, initialStore())

    const load = () =>{
        dispatch({type: "loading"})
    }

    const redirect = () =>{
        dispatch({type: "redirecting"})
    }
    const redirectOff = () =>{
        dispatch({type: "redirecting-off"})
    }


    return <StoreContext.Provider value={{ store, dispatch, load, redirect, redirectOff}}>
        {children}
    </StoreContext.Provider>
}

export default function useGlobalReducer() {
    const { dispatch, store, load, redirect, redirectOff } = useContext(StoreContext)
    return { dispatch, store, load, redirect, redirectOff };
}