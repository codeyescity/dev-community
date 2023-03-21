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
    img_url VARCHAR(120) DEFAULT "http://127.0.0.1:3000/static/img/user.jpg",
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    about VARCHAR(500) DEFAULT "This user has no about section",
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


CREATE TABLE IF NOT EXISTS projects
(
    project_id INT AUTO_INCREMENT PRIMARY KEY, 
    project_owner_id INT,
    project_name TEXT,
    project_description TEXT,
    project_progress INT DEFAULT 0,
    project_creation_date DATETIME,
    FOREIGN KEY(project_owner_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS members
(
    member_id INT AUTO_INCREMENT PRIMARY KEY, 
    member_role VARCHAR(6) DEFAULT "member",
    user_id INT,
    project_id INT,
    member_join_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS invites
(
    invite_id INT AUTO_INCREMENT PRIMARY KEY, 
    user_id INT,
    project_id INT,
    invite_role VARCHAR(6),
    invite_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS teams
(
    team_id INT AUTO_INCREMENT PRIMARY KEY, 
    team_name VARCHAR(50),
    team_leader_id INT,
    project_id INT,
    FOREIGN KEY(team_leader_id) REFERENCES members(user_id) ON DELETE CASCADE,
    FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS team_members
(
    team_member_id INT AUTO_INCREMENT PRIMARY KEY, 
    team_id INT, 
    member_id INT,
    FOREIGN KEY(team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY(member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS technologies
(
    technology_id INT PRIMARY KEY,
    technology_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS users_technologies
(
    user_id INT ,
    technology_id INT, 
    technology_experience FLOAT DEFAULT 0.0,
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

CREATE TABLE IF NOT EXISTS chatlogs
(
    chatlogs_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    project_id INT,
    message VARCHAR(400),
    message_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tasks
(
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    member_id INT, 
    task_title VARCHAR(200),
    task_description TEXT,
    task_type VARCHAR(20),
    task_state VARCHAR(20),
    task_progress INT DEFAULT 0,
    task_start_date VARCHAR(200),
    task_end_date VARCHAR(200),
    task_needed_time INT,
    FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY(member_id) REFERENCES members(member_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tasks_technologies
(
    task_id INT ,
    technology_id INT, 
    technology_level FLOAT DEFAULT 0.0,
    PRIMARY KEY(task_id, technology_id),
    FOREIGN KEY(task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY(technology_id) REFERENCES technologies(technology_id) ON DELETE CASCADE
);



--@block
DELETE from users;
DELETE from technologies;
DELETE from users_technologies;

--@block
USE DevCommunityTest;
--@block
SELECT * FROM technologies;
--@block
SELECT * FROM users;
--@block 
SELECT * FROM users_technologies;
--@block
SELECT * from tasks_technologies;


--@block
INSERT INTO technologies (technology_id, technology_name) VALUES (1 ,"html"), (2 ,"css") , (3 ,"javascript"), (4 ,"c++"), (5 ,"java"), (6 ,"sql"), (7 ,"php"), (8 ,"python"), (9 ,"c"), (10 ,"c#"), (11 ,"go");
INSERT INTO users(username) VALUES ("user1"), ("user2"), ("user3");

--@block
INSERT INTO users_technologies (user_id, technology_id, technology_experience) VALUES 
(1, 1, 2), (1, 2, 2), (1, 3, 2),
(2, 1, 4), (2, 2, 3), (2, 3, 3),
(3, 1, 3), (3, 2, 3), (3, 3, 4);



--@block
USE DevCommunityTest;
--@block
SELECT * from chatlogs;








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
SELECT * FROM invites;
--@block
SELECT * FROM projects;

--@block
SELECT * FROM members;
--@block
SELECT * FROM teams;


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