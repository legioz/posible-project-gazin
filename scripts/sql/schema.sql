USE db;

CREATE TABLE user (
  id INTEGER NOT NULL AUTO_INCREMENT,
  username VARCHAR(30) UNIQUE NOT NULL,
  password VARCHAR(70) NOT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  inserted_on DATETIME DEFAULT NOW(),
  PRIMARY KEY(id)
);

CREATE TABLE developer (
  id INTEGER NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  sex CHAR(1) NOT NULL,
  hobby VARCHAR(150) NOT NULL,
  birthdate DATETIME NOT NULL,
  is_deleted TINYINT NOT NULL DEFAULT 0,
  inserted_on DATETIME NOT NULL DEFAULT NOW(),
  updated_on DATETIME,
  PRIMARY KEY(id),
  CHECK(sex IN ('M', 'F'))
);


INSERT INTO
  user (username, password)
VALUES
  (
    'admin',
    '$2b$12$e.L97G95MrCQpta7SBTEkeyRAqPeUMdTkTp3pugkseTy9Q7Fqy6XS'
  );
