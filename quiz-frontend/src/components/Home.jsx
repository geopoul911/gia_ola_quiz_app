import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';

// Home page of our application
const Home = ({history, setUserToken}) => {

     const handleLogout = () => {
         localStorage.removeItem('userToken');
         setUserToken(null);
         history.push('/login');
     };

     return (
        <Fragment>
            <div id='home'>
                <section>
                    <h1 className='app-title'>Gia Ola Quiz Application</h1>
                        <div className='auth-container'>
                            <Link to='/quiz' className='btn btn-primary' id='play-button'>Play</Link>
                            <Link to='/history' className='btn btn-secondary>' id='history-button'>History</Link>
                            <button onClick={handleLogout} className='btn btn-danger' id='logout-button'>Logout</button>
                        </div>
                </section>
            </div>
        </Fragment>
     );
};

export default Home;
