export default function RegisterForm() {
    return (
        <form className="main-form">
            <label>First Name</label>
            <input className="main-input" type="text" placeholder="Enter Your First Name"/>
            <label>Last Name</label>
            <input className="main-input" type="text" placeholder="Enter Your Last Name"/>
            <label>Email</label>
            <input className="main-input" type="email" placeholder="Enter Your Email"/>
            <label>Password</label>
            <input className="main-input" type="password" placeholder="Enter Password"/>
            <label>Confirm Password</label>
            <input className="main-input" type="password" placeholder="Confirm Password"/>
            <button className="main-button">Register</button>
        </form>
    )
}