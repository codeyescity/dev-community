import { Link } from 'react-router-dom';
import LoginForm from './sections/login-form/LoginForm'; 
import './style.css'; 

export default function Login() {
    return (
        <div className="main-form-wrapper login-form-wrapper">
            <h1>Login</h1>
            <LoginForm />
            <Link to='/register'>Create An Account</Link>
        </div>
    )
}