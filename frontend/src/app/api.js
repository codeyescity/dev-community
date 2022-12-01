const api = 'https://jsonplaceholder.typicode.com/posts';

export const getPosts = () => fetch(api).then(res => res.json()); 
