export default function LoginForm() {
    return (
        <form className="main-form login-form">
            <label>Username Or Email</label>
            <input className="main-input" type="text" placeholder="Enter Username Or Email" />
            <label>Password</label>
            <input className="main-input" type="password" placeholder="Enter Password" />
            <button className="main-button">Login</button>
        </form>
    )
}