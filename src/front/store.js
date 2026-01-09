import Swal from "sweetalert2";

export const initialStore = () => {
  return {
    login: false,
    loading: false,
    redirecting: false,
    swalClosed : false,
    user: {},
    missions: [],
    claudeMissionId: 1
  };
};

export default function storeReducer(store, action = {}) {
  switch (action.type) {
    case "LOGIN":
      if (!action.payload) {
        return { ...store, login: action.payload, user: {} };
      }

      return { ...store, login: action.payload };

    case "LOADING":
      return { ...store, loading: true };

    case "LOADING_OFF":
      return { ...store, loading: false };

    case "REDIRECTING":
      return { ...store, redirecting: true };

    case "REDIRECTING_OFF":
      return { ...store, redirecting: false };

    case "CLOSE_SWAL":
      return {...store, swalClosed: true}

    case "OPEN_SWAL":
      return {...store, swalClosed: false}

    case "SAVE_USER":
      return { ...store, user: action.payload };

    case "SAVE_MISSIONS":
      return {...store, missions : action.payload}

    case "ADD_MISSION":
      return {...store, missions: [...store.missions, action.payload]}

    case "UPDATE_OBJECTIVE":

      const newIncompleted = store.missions.incompleted.map((mission)=>{
        if(mission.id === action.payload.missionId){
          const newObjectives = mission.objectives.map((objective)=>{
            if(objective.id === action.payload.objectiveId){
              return {...objective, completed_at: action.payload.completedAt}
            }
            return objective
          })
          return {...mission, objectives : newObjectives}
        }
        return mission
      })

      return {...store, missions: {...store.missions, incompleted: newIncompleted }}

    case 'COMPLETE_MISSION':

      const filteredMissions = store.missions.incompleted.filter((mission)=> mission.id != action.payload.missionId)

      const newCompletedMissions = [...store.missions.completed, action.payload.newCompleted]

      return {...store, missions: {incompleted: filteredMissions, completed: newCompletedMissions}}

    default:
      throw Error("Unknown action.");
  }
}
