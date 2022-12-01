import { useQuery } from 'react-query';
import { getPosts } from '../../../../../app/api'
import Post from './Post';

/* For Testing */

function genId() {
    let id = '';
    for (let i = 0; i < 2; i++) id += Math.trunc(Math.random() * 9);
    return id;
}

function genDate() {
    let date = ''
    let unit = ['m', 'h', 'd', 'w', 'mo', 'y']; 
    date += unit[Math.trunc(Math.random() * (unit.length - 1))]; 
    switch (date) {
        case 'm': return ((Math.trunc(Math.random() * 58) + 1) + date)
        case 'h': return ((Math.trunc(Math.random() * 2) + 1) + date)
        case 'd': return ((Math.trunc(Math.random() * 5) + 1) + date)
        case 'w': return ((Math.trunc(Math.random() * 2) + 1) + date)
        case 'mo': return ((Math.trunc(Math.random() * 10) + 1) + date)
        case 'y': return ((Math.trunc(Math.random() * 2) + 1) + date)
    }
}

/* For Testing */

export default function Posts() {
    
    const { isLoading, error, data:posts } = useQuery(['get-posts'], getPosts);

    if (isLoading) return <h1>Loading...</h1>
    if (error) return <h1>{error.message}</h1>
    return (
        <section className="posts">
            {
                posts.map((post, idx) => {
                    let { userId: postOwnerId, id: postId, title, body } = post;
                    postOwnerId = Number(genId() + postOwnerId + genId());
                    return <Post key={idx} postOwnerId={postOwnerId} postId={postId} title={title} body={body} date={genDate()} />
                })

            }
        </section>
    )
}