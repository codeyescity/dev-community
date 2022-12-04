const api = 'https://jsonplaceholder.typicode.com/posts';
export const headers = { 'Content-Type': 'application/json' };

export const getPosts = () => fetch(api).then(res => res.json()); 
