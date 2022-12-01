import UserProfileShowcase from '../../../../../components/user-profile-showcase/UserProfileShowcase';
import { useGlobalState } from '../../../../../app/GlobalStateProvider';

export default function SharePostSection() {

    const { state } = useGlobalState();
    const { user } = state;

    return (
        <section className="share-post">
            <UserProfileShowcase userId={user.userId} />
            <textarea className="main-textarea" placeholder="Write Something"></textarea>
            <div className="functionalities">
                <button className="post main-button">Post</button>
            </div>
        </section>
    )
}