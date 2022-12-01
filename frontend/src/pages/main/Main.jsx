import Header from '../../sections/header/Header';
import NavSideBar from './sections/nav-side-bar/NavSideBar'
import MeetPeople from './sections/meet-people/MeetPeople'
import './style.css'

export default function Main({ children }) {

    return (
        <>
            <Header />
            <section className="main">
                <div className="container">
                    <NavSideBar />
                    {children}
                    <MeetPeople />
                </div>
            </section>
        </>
    )
}