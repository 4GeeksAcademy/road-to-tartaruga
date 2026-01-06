export const ObjectiveCard = ({handleChange, objective: {title, completed_at}}) => {
     
    

    return (
    <li className="list-group-item">
        <label>{title}</label>
        <input defaultChecked={completed_at ? true : false} onChange={handleChange} type="checkbox"></input>
    </li>
    )
}