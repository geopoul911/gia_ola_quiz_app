import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Quiz from './components/Quiz';
import Summary from './components/Summary';
import History from './components/History';
import ProtectedRoute from './components/ProtectedRoute';

// Initialization point for application
function App() {

    const [userToken, setUserToken] = useState(localStorage.getItem("userToken"));

    // Route management is done here
    return (
      <Router>
            <Switch>
              {!!userToken !== true && (
                  <Route
                      exact
                      path="/login"
                      render={props => <Login {...props} setUserToken={setUserToken} />}
                  />
              )}
                {!!userToken !== true && (
                    <Route
                        exact
                        path="/register"
                        render={props => <Register {...props} setUserToken={setUserToken} />}
                    />
                )}
                {/* Protected routes. only logged in user can access these routes*/}
                <ProtectedRoute isLoggedIn={!!userToken} path="/" exact render={props => <Home {...props} setUserToken={setUserToken} />}/>
                <ProtectedRoute isLoggedIn={!!userToken} path='/quiz' exact component={Quiz}/>
                <ProtectedRoute isLoggedIn={!!userToken} path='/summary' exact component={Summary}/>
                <ProtectedRoute isLoggedIn={!!userToken} path='/history' exact component={History}/>
          </Switch>
      </Router>
    );
}

export default App;
