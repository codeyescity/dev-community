import Header from '../../sections/header/Header';
import NavSideBar from './sections/nav-side-bar/NavSideBar'
import WorkingRooms from './sections/working-rooms/WorkingRooms';
import Model from '../../components/model/Model'
import './style.css'

export default function Main({ children }) {

    return (
        <>
            <Header />
            <section className="main">
                <div className="container">
                    <NavSideBar />
                    {children}
                    <WorkingRooms />
                </div>
            </section>
        </>
    )
}