export const initialStore=()=>{
  return{
   login: false,
   loading:false
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
   case 'login':
    return {...store, login: action.payload}

  case 'loading':
    return {...store, loading: !store.loading}

    default:
      throw Error('Unknown action.');
  }    
}
