import UserProfileShowcase from '../../components/user-profile-showcase/UserProfileShowcase'
import { useGlobalState } from '../../app/GlobalStateProvider';
import './style.css'


export default function Header() {

    const { state } = useGlobalState();
    const { user } = state; 

    return (
        <header>
            <div className="container">
                <input type="text" className="main-input search" placeholder="search" />
                <UserProfileShowcase userId={user.userId} />
            </div>
        </header>
    )
}