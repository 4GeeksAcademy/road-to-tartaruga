// Import necessary components and functions from react-router-dom.

import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";
import { PublicLayout } from "./layouts/PublicLayout";
import { Home } from "./pages/public-pages/Home";
import { AboutMe } from "./pages/public-pages/AboutMe";
import { AboutTartaruga } from "./pages/public-pages/AboutTartaruga";
import { PrivateLayout } from "./layouts/PrivateLayout";
import { AuthLayout } from "./layouts/AuthLayout";
import { MyProfile } from "./pages/private-pages/MyProfile";
import { MyMissions } from "./pages/private-pages/MyMissions";
import { MyCrews } from "./pages/private-pages/MyCrews";
import { MyContributions } from "./pages/private-pages/MyContributions";
import { Crew } from "./pages/private-pages/Crew";
import { ClaudeMissions } from "./pages/private-pages/ClaudeMissions";
import { Authentication } from "./pages/auth-pages/Atuhentication";
import { NotFound } from "./pages/public-pages/NotFound";
import { AuthNeed } from "./pages/public-pages/AuthNeed";

export const TartarugaRoutes = () =>{
return(

  <BrowserRouter>
  <Routes>

      <Route  path="/" element={<PublicLayout/>} >
        <Route index element={<Home />} />
        <Route path="about-me" element={<AboutMe />} />
        <Route path="about-tartaruga" element={<AboutTartaruga />} />
        <Route path="*" element={<NotFound/>} />
        <Route path="auth-need" element={<AuthNeed/>} />
        
        
      </Route>

      <Route  element={<PrivateLayout/>}>
        <Route path="my-profile" element={<MyProfile/>} />
        <Route path="my-missions" element={<MyMissions/>} />
        <Route path="my-crews" element={<MyCrews/>} />
        <Route path="my-contributions" element={<MyContributions/>} />
        <Route path="crew" element={<Crew/>} />
        <Route path="claude-missions" element={<ClaudeMissions/>} />
      </Route>

      <Route element={<AuthLayout/>}>
        <Route path="auth" element={<Authentication/>} />
      </Route>

    </Routes>
  </BrowserRouter>
  )
    }
 