-- dockerが起動したら入る場所
use project_db;

-- ユーザ情報生成処理
CREATE TABLE IF NOT EXISTS user (
    email VARCHAR(255) PRIMARY KEY NOT NULL,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    comment VARCHAR(255),
)
-- CREATE TABLE IF NOT EXISTS user (
--     id INT(11) PRIMARY KEY AUTO_INCREMENT,
--     username VARCHAR(20) NOT NULL,
--     email VARCHAR(255) NOT NULL,
--     password VARCHAR(255) NOT NULL
-- )
