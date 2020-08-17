import React from "react";
import axios from "axios";
import { Link } from 'react-router-dom';

const BACKEND_LOGIN_ENDPOINT = 'http://localhost:8001/api/user/login/';
const HEADERS = {
    "Content-type": "Application/json",
};

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            msg: ''
        }
    }

    onSubmit = (e) => {
        e.preventDefault();
        const email = e.target.username.value;
        const password = e.target.password.value;

        axios({
            method: 'post',
            url: BACKEND_LOGIN_ENDPOINT,
            headers: HEADERS,
            data: {
                email,
                password,
            }
        }).then((res) => {
            const token = res.data.token;
            localStorage.setItem("userToken",token);
            this.props.setUserToken(token);
            this.props.history.push('/');

        }).catch(e => {
            this.setState({
                msg: 'Login Failed. Please verify email/password.'
            })
        })
    };

    componentDidMount() {
        if (localStorage.getItem('userToken')){
            this.props.history.push('/');
        }
    }

    render() {
        return (
            <div className="base-container login-container" ref={this.props.containerRef}>
                <h1>Login</h1><div className="content">
                    <form className="form login-form" onSubmit={this.onSubmit}>
                        <div className="form-group">
                            <label htmlFor="username">Email</label>
                            <input type="text" name="username" placeholder="username" />
                        </div>
                        <div className="form-group">
                            <label htmlFor="password">Password</label>
                            <input type="password" name="password" placeholder="password" />
                        </div>
                        <p className='login-message'>{this.state.msg}</p>
                        <div className="footer">
                            <button type="submit" className="btn">
                                Login
                            </button>
                        </div>
                        <Link to='/register' className='register-link' id='register'>New User?</Link>
                    </form>
                </div>
            </div>
        );
    }
}

export default Login;
