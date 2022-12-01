import './style.css';

export default function UserProfileShowcase({ userId, date }) {
    return (
        <div className="profile">
            <div className="profile-img"></div>
            <p className="profile-username">{`user#${userId}`}</p>
            { date && <p className="post-date">{ date }</p>}
        </div>
    )
}