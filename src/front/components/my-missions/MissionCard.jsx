export const MissionCard = ({mission, color}) => {
    return (
        <div className="card" style={{ width: "18rem" }}>
            <div className={`card-body bg-${color}`}>
                <h5 className="card-title">{mission.title}</h5>
                <p className="card-text">{mission.description}</p>
                <ul className="list-group">
                    {mission.objectives.map((objective,index) => {
                        return <li key={index} className="list-group-item">{objective.title}</li>
                    })}
                </ul>
            </div>
        </div>
    )
}