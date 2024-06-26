import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import MainApp from './page/main.js'
import RegisterApp from './page/register.js';
import LoginApp from './page/login.js';


const router = createBrowserRouter([
  {
    path: "/",
    element: <MainApp />,
  }, {
    path: '/register/',
    element: <RegisterApp />
  }, {
    path: '/login/',
    element: <LoginApp />
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
