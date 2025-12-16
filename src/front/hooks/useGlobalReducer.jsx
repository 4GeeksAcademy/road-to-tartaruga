import { useContext, useReducer, createContext } from "react";
import storeReducer, { initialStore } from "../store"  


const StoreContext = createContext()


export function StoreProvider({ children }) {
   
    const [store, dispatch] = useReducer(storeReducer, initialStore())

    const load = () =>{
        dispatch({type: "loading"})
    }


    return <StoreContext.Provider value={{ store, dispatch, load }}>
        {children}
    </StoreContext.Provider>
}

export default function useGlobalReducer() {
    const { dispatch, store, load } = useContext(StoreContext)
    return { dispatch, store, load };
}