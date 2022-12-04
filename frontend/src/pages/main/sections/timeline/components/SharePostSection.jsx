import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom';
import { useGlobalState } from '../../../../../app/GlobalStateProvider';

export default function SharePostSection() {

    const [postBody, setPostBody] = useState('');
    const [showFunctionalities, setShowFunctionalities] = useState(false);

    const { state } = useGlobalState();
    const { userId } = state.user;

    const sharePost = () => {
        console.log({ user_id: userId, post_description: postBody });
        setPostBody('');
    }

    // const handleDivChange = ({ target }) => {
    //     setPostBody(target.innerHTML)
    //     target.style.overflowY = target.clientHeight > 100 ? 'scroll' : 'auto'
    // }

    const handleSharePostTextarea = ({ target }) => {
        setPostBody(target.value)
    }

    return (
        <>
            <section className="share-post">
                <div className="profile-img"></div>
                <textarea
                value={postBody}
                onChange={handleSharePostTextarea}
                onFocus={() => setShowFunctionalities(true)}
                className="main-textarea"
                placeholder="Write Something"
            ></textarea>

                {/* <div 
                onInput={handleDivChange} 
                contentEditable style={{ maxHeight: '100px' }}
                onFocus={() => setShowFunctionalities(true)}
                placeholder="Write Something"
                ></div> */}

                {showFunctionalities &&
                    <div className="functionalities">
                        <button onClick={sharePost} className="post main-button">Post</button>
                    </div>
                }
            </section>
            <section className="other-posts-types">
                <div className="or">
                    <hr />
                    <span>OR</span>
                    <hr />
                </div>
                <div className="functionalities">
                    <Link to="/new-question" className="secondary-button">Ask A Question</Link>
                    <Link to="/share-project" className="secondary-button">Share Your Work</Link>
                </div>
            </section>
        </>
    )
}