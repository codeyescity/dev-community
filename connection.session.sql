--@block
DROP DATABASE DevCommunityTest;

--@block
CREATE DATABASE DevCommunityTest;
USE DevCommunityTest;

--@block
USE DevCommunityTest;
CREATE TABLE IF NOT EXISTS users
(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) UNIQUE,
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone_number BIGINT
);

CREATE TABLE IF NOT EXISTS posts
(
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    post_owner_id INT,
    post_type TEXT,
    post_title TEXT,
    post_body TEXT,
    post_code TEXT,
    post_number_likes INT DEFAULT 0,
    post_number_comments INT DEFAULT 0,
    post_creation_date DATETIME,
    FOREIGN KEY(post_owner_id) REFERENCES users(user_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS users_comments_posts
(
    comment_id INT AUTO_INCREMENT PRIMARY KEY, 
    comment_owner_id INT,
    post_id INT,
    comment_body TEXT,
    comment_code TEXT,
    comment_number_likes INT DEFAULT 0,
    comment_date DATETIME,
    FOREIGN KEY(comment_owner_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users_likes_posts
(
    post_liker_id INT,
    post_id INT, 
    post_like_date DATETIME,
    PRIMARY KEY(post_id,post_liker_id),
    FOREIGN KEY(post_liker_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users_likes_comments
(
    comment_liker_id INT,
    comment_id INT, 
    comment_like_date DATETIME,
    PRIMARY KEY(comment_id,comment_liker_id),
    FOREIGN KEY(comment_liker_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(comment_id) REFERENCES users_comments_posts(comment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS technologies
(
    technology_id INT AUTO_INCREMENT PRIMARY KEY,
    technology_name TEXT
);

CREATE TABLE IF NOT EXISTS users_technologies
(
    user_id INT,
    technology_id INT, 
    PRIMARY KEY(user_id, technology_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(technology_id) REFERENCES technologies(technology_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS posts_technologies
(
    post_id INT,
    technology_id INT, 
    PRIMARY KEY(post_id, technology_id),
    FOREIGN KEY(post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY(technology_id) REFERENCES technologies(technology_id) ON DELETE CASCADE
);



--@block
USE DevCommunityTest;
INSERT INTO users (username, first_name, last_name, email, phone_number) VALUES
("bob","Drake" ,"Carroll","lorem@outlook.org","9824061330"),
("Yoko","Marsden", "Jefferson","at.arcu@outlook.com","9824061330"),
("star", "Palmer", "Barnes","nisi.sem@gmail.ca","9844061330"),
("Palmer" ,"Yoko", "Donaldson","vulputate.velit@gmail.com","9824061330"),
("Jefferson", "Fritz", "Joseph","eget.nisi.dictum@outlook.com","9824061330")
;

INSERT INTO posts (post_owner_id, post_type, post_title, post_body, post_code, post_creation_date) VALUES
(1,"post", "", "Lorem ipsum dolor sit amet", "", NOW()),
(1,"post", "", "Lorem ipsum dolor sit amet", "", NOW()),
(2,"question", "title", "Lorem ipsum dolor sit amet", "x = x+1", NOW()),
(3,"question", "title", "Lorem ipsum dolor sit amet", "let v = 5", NOW()),
(4,"job_offer", "", "Lorem ipsum dolor sit amet", "", NOW()),
(5,"job_offer", "", "Lorem ipsum dolor sit amet", "", NOW())
;


INSERT INTO users_comments_posts (comment_owner_id, post_id, comment_body, comment_date) VALUES
(1,1,"Lorem ipsum dolor sit amet",NOW()),
(2,1,"Lorem ipsum dolor sit amet",NOW()),
(3,1,"Lorem ipsum dolor sit amet",NOW()),
(1,2,"Lorem ipsum dolor sit amet",NOW()),
(1,3,"Lorem ipsum dolor sit amet",NOW()),
(1,4,"Lorem ipsum dolor sit amet",NOW())
;


--@block
SELECT * FROM users;

--@block
SELECT * FROM posts;

--@block
SELECT * FROM users_comments_posts;

--@block
SELECT * FROM users_likes_posts;

--@block
SELECT * FROM users_likes_comments;





--@block
select 
        c.post_id,
        c.post_creation_date,
        u.user_id,
        u.username,
        c.description,
        c.number_likes,
        json_arrayagg( json_object
                                ( 
                                'comment_id', p.comment_id, 
                                'user_id', u.user_id,
                                'username', u.username,
                                'comment_text', p.comment_text,
                                'comment_likes', p.comment_likes
                                )  
                        ) AS 'comments'
        from posts c
        inner join postscomments p on p.post_id = c.post_id
        inner join users u ON u.user_id = c.user_id
        group by c.post_id
        ;

--@block
SELECT *    
FROM posts 
LEFT JOIN users ON posts.user_id  = users.user_id
LEFT JOIN postlikes ON posts.post_id = postlikes.post_id

;
--@block
SELECT posts.post_id, posts.post_creation_date, users.user_id, users.username, posts.description, posts.number_likes,
            IF(10>20, '12', '13') AS "LIKED"
            
            FROM posts 
            LEFT JOIN users ON posts.user_id  = users.user_id
            LEFT JOIN postlikes ON posts.post_id = postlikes.post_id
            GROUP BY  posts.post_id


;