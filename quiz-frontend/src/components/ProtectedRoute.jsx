import React from "react";
import { Route, Redirect } from "react-router-dom";


// Component to protect a route. checks if user is logged in when accessing a protected route
// If not logged in, show login page
const PrivateRoute = ({ component: Component, render, isLoggedIn, ...rest }) => {
    return (
        <Route
            {...rest}
            render={props =>
                isLoggedIn === true ? (
                    render ? render(props) :
                    <Component {...props} />
                ) : (
                    <Redirect to={{ pathname: "/login" }} />
                )
            }
        />
    );
};

export default PrivateRoute;
