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
    user_name TEXT,
    user_password TEXT

);

CREATE TABLE IF NOT EXISTS posts
(
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    type TEXT,
    title TEXT,
    description TEXT,
    code TEXT,
    number_likes INT,
    post_creation_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS postscomments
(
    comment_id INT AUTO_INCREMENT PRIMARY KEY, 
    user_id INT,
    post_id INT,
    comment_text TEXT,
    comment_likes INT,
    comment_creation_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(post_id) REFERENCES posts(post_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS postlikes
(
    post_id INT, 
    user_id INT,
    post_like_date DATETIME,
    PRIMARY KEY(post_id,user_id),
    FOREIGN KEY(post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS commentlikes
(
    comment_id INT, 
    user_id INT,
    comment_like_date DATETIME,
    PRIMARY KEY(comment_id,user_id),
    FOREIGN KEY(comment_id) REFERENCES postscomments(comment_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

--@block
USE DevCommunityTest;
INSERT INTO users (user_name) VALUES
("salim"),
("hakim"),
("faycal")
;

INSERT INTO posts (user_id,type,description,number_likes,post_creation_date) VALUES
(1,"post","despcription 1",20,NOW()),
(2,"post","despcription 2",3,NOW()),
(3,"post","despcription 2",5,NOW())
;

INSERT INTO postscomments (user_id, post_id, comment_text,comment_likes,comment_creation_date) VALUES
(1,1,"comment 1",5,NOW()),
(2,1,"comment 2",2,NOW()),
(3,2,"comment 3",1,NOW());

INSERT INTO postlikes (user_id, post_id, post_like_date) VALUES
(1,1,NOW()),
(1,2,NOW()),
(2,3,NOW())

--@block
SELECT * FROM users;

--@block
SELECT * FROM posts;

--@block
SELECT * FROM postscomments;

--@block
SELECT * FROM postlikes;
--@block
select 
        c.post_id,
        c.post_creation_date,
        u.user_id,
        u.user_name,
        c.description,
        c.number_likes,
        json_arrayagg( json_object
                                ( 
                                'comment_id', p.comment_id, 
                                'user_id', u.user_id,
                                'user_name', u.user_name,
                                'comment_text', p.comment_text,
                                'comment_likes', p.comment_likes
                                )  
                        ) AS 'comments'
        from posts c
        inner join postscomments p on p.post_id = c.post_id
        inner join users u ON u.user_id = c.user_id
        group by c.post_id
        ;