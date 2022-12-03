import { Link, useLocation } from 'react-router-dom';
import { AiOutlineHome } from 'react-icons/ai';
import { BsQuestionSquare, BsFillFileEarmarkPostFill, BsCodeSquare } from 'react-icons/bs';

export default function NavSideBar() {

    const { pathname } = useLocation()

    return (
        <nav className="main-nav">
            <ul>
                <li><Link className={pathname === '/' ? 'active' : ''} to="/"><AiOutlineHome />Home</Link></li>
                <li><Link className={pathname === '/questions' ? 'active' : ''} to="/questions"><BsQuestionSquare />Questions</Link></li>
                <li><Link className={pathname === '/job-offers' ? 'active' : ''} to="/job-offers"><BsFillFileEarmarkPostFill />Job Offers</Link></li>
                <li><Link className={pathname === '/projects' ? 'active' : ''} to="/projects"><BsCodeSquare />Projects</Link></li>
            </ul>
        </nav>
    )
}