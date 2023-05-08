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


