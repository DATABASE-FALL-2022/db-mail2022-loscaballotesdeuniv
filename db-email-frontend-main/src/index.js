import React from 'react';
import ReactDOM from 'react-dom/client';
import {Route, BrowserRouter, Routes} from 'react-router-dom';
import './index.css';
import '../node_modules/semantic-ui-css/semantic.min.css';
import HomePage from "./HomePage";
import UserView from "./UserView";
import Dashboard from "./Dashboard";
import App from "./App";
import SignUp from "./SignUp";
import FetchApi from "./components/FetchApi";


const root = ReactDOM.createRoot( document.getElementById('root') );
root.render(
    <BrowserRouter>
        <Routes>
            <Route exact path="/loscaballotesdeuniv/Home" element={<App/>} />
            <Route exact path="/loscaballotesdeuniv/Login" element={<HomePage/>} />
            <Route exact path="/loscaballotesdeuniv/UserView" element={<UserView/>} />
            <Route exact path="/loscaballotesdeuniv/Dashboard" element={<Dashboard/>} />
            <Route exact path="/loscaballotesdeuniv/SignUp" element={<SignUp/>} />
            <Route exact path="/loscaballotesdeuniv/Example" element={<FetchApi/>} />
        </Routes>
    </BrowserRouter>
);
