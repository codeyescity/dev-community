--@block
DROP DATABASE DevCommunityTest;

--@block
CREATE DATABASE DevCommunityTest;
USE DevCommunityTest;

--@block
CREATE TABLE IF NOT EXISTS users
(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name TEXT
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
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS postscomments
(
    comment_id INT AUTO_INCREMENT PRIMARY KEY, 
    user_id INT,
    post_id INT,
    comment_text TEXT,
    comment_likes INT,
    comment_creation_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(post_id) REFERENCES posts(post_id)
);

CREATE TABLE IF NOT EXISTS postlikes
(
    post_id INT, 
    user_id INT,
    post_like_date DATETIME,
    PRIMARY KEY(post_id,user_id),
    FOREIGN KEY(post_id) REFERENCES posts(post_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS commentlikes
(
    comment_id INT, 
    user_id INT,
    comment_like_date DATETIME,
    PRIMARY KEY(comment_id,user_id),
    FOREIGN KEY(comment_id) REFERENCES postscomments(comment_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

--@block
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

INSERT INTO postscomments (user_id, comment_text,comment_likes,comment_creation_date) VALUES
(1,"comment 1",5,NOW()),
(2,"comment 2",2,NOW()),
(3,"comment 3",1,NOW());

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