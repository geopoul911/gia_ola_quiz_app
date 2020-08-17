import React from "react";
import axios from "axios";

const BACKEND_LOGIN_ENDPOINT = 'http://localhost:8001/api/user/register/';
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
        const name = e.target.name.value;

        axios({
            method: 'post',
            url: BACKEND_LOGIN_ENDPOINT,
            headers: HEADERS,
            data: {
                email,
                password,
                name
            }
        }).then((res) => {
            this.setState({
                msg: 'Registration Successful. Redirecting to login page...'
            });
            setTimeout(() => {
                this.props.setUserToken(null);
                this.props.history.push('/login');
            }, 2000);

        }).catch(e => {
            this.setState({
                msg: 'Registration Failed. Please verify input data.'
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
                <h1>Register</h1><div className="content">
                <form className="form login-form" onSubmit={this.onSubmit}>
                    <div className="form-group">
                        <label htmlFor="password">Name</label>
                        <input type="text" name="name" placeholder="name" />
                    </div>
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
                            Submit
                        </button>
                    </div>
                </form>
            </div>
            </div>
        );
    }
}

export default Login;
