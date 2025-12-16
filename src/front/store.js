export const initialStore=()=>{
  return{
   login: false,
   loading:false,
   redirecting: false
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
   case 'login':
    return {...store, login: action.payload}

  case 'loading':
    return {...store, loading: !store.loading}

  case 'redirecting':
    return {...store, redirecting: true}
    
  case 'redirecting-off':
    return {...store, redirecting: false}

    default:
      throw Error('Unknown action.');
  }    
}
