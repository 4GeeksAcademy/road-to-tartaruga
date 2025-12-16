import { Link } from "react-router-dom";
import useGlobalReducer from "../hooks/useGlobalReducer";
import { useEffect } from "react";
import { fetchPrivate } from "../services/authServices";

export const Navbar = () => {

	const { store, dispatch } = useGlobalReducer()


	const handleLogOut = () =>{
		const storage = localStorage.length == 0 ? sessionStorage : localStorage
		 storage.clear()
		dispatch({type: "login", payload: false})
	}
	

	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">Home</span>
				</Link>
				<div className="ml-auto">
					<Link to="/about-me">
						<button className="btn btn-primary">About me</button>
					</Link>
					<Link to="/about-tartaruga">
						<button className="btn btn-primary">About Tartaruga</button>
					</Link>
					<Link to="/my-profile">
						<button className="btn btn-primary">My profile</button>
					</Link>
					<Link to="/my-missions">
						<button className="btn btn-primary">My missions</button>
					</Link>
					<Link to="/my-crews">
						<button className="btn btn-primary">My crews</button>
					</Link>
					<Link to="/my-contributions">
						<button className="btn btn-primary">My contributions</button>
					</Link>
					<Link to="/crew">
						<button className="btn btn-primary">Crew</button>
					</Link>
					<Link to="/claude-missions">
						<button className="btn btn-primary">Claude missions</button>
					</Link>

					{store.login ?

							<button onClick={handleLogOut} className="btn btn-danger">Salir</button>
						:
						<>
							<Link to="/auth" state={{ login: true }}>
								<button className="btn btn-primary">Ingresar</button>
							</Link>
							<Link to="/auth" state={{ login: false }}>
								<button className="btn btn-primary">Registro</button>
							</Link>
						</>
					}

					<Link to="/jamon-serrano">
						<button className="btn btn-primary">Not found</button>
					</Link>
					<Link to="/auth-need">
						<button className="btn btn-primary">Need Auth</button>
					</Link>
				</div>
			</div>
		</nav>
	);
};