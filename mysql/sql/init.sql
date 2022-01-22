-- dockerが起動したら入る場所
use project_db;

-- ユーザ情報
CREATE TABLE IF NOT EXISTS user (
    id INT(11) PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    comment VARCHAR(255),
    auth_id INT(1) NOT NULL DEFAULT 1,
    is_delete INT(1) NOT NULL DEFAULT 0,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ユーザ認証情報
CREATE TABLE IF NOT EXISTS user_authority (
    id INT(1) PRIMARY KEY,
    comment VARCHAR(50),
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 利用者、管理者
INSERT INTO user_authority(id, comment) VALUES(1, "利用者");
INSERT INTO user_authority(id, comment) VALUES(2, "管理者");
INSERT INTO user_authority(id, comment) VALUES(3, "スタッフ");

-- 投稿項目
CREATE TABLE IF NOT EXISTS post_info (
    id INT(11) PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    comment VARCHAR(255) NOT NULL,
    post_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 投稿ライク機能
CREATE TABLE IF NOT EXISTS post_like (
    email VARCHAR(255) NOT NULL,
    post_id INT(11) NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(email, post_id)
);

-- ユーザブロック機能
CREATE TABLE IF NOT EXISTS user_block (
    user_id INT(11) NOT NULL,
    target_id INT(11) NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(user_id, target_id)
);