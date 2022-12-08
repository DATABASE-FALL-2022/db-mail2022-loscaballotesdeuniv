import React from 'react';
import ReactDOM from 'react-dom'
import './index.css';
import { Routes , BrowserRouter, Route } from 'react-router-dom';
import App from './App';
import HomePage from "./HomePage";
import 'semantic-ui-css/semantic.min.css'
// import reportWebVitals from './reportWebVitals';

// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
  // <React.StrictMode>
  //   <App />
  // </React.StrictMode>
ReactDOM.render(

    <BrowserRouter>
        <Routes>
            <Route exact path="/" element={<App/>} />
            <Route exact path="/Home" element={<HomePage/>} />
        </Routes>
    </BrowserRouter>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
