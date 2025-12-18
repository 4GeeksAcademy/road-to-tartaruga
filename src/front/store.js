import Swal from 'sweetalert2'

export const initialStore=()=>{
  return{
   login: false,
   loading:false,
   redirecting: false,
   user: {}
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
   case 'login':

   if(!action.payload){
    return {...store, login: action.payload, user: {}}
   }

    return {...store, login: action.payload}

  case 'loading':
    return {...store, loading: true}

  case 'loadingOff':
    return {...store, loading: false}

  case 'redirecting':
    return {...store, redirecting: true}
    
  case 'redirecting-off':
    return {...store, redirecting: false}

  case 'saveUser':
    return {...store, user: action.payload}


    default:
      throw Error('Unknown action.');
  }    
}
