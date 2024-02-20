CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(15) NOT NULL,
  last_name VARCHAR(15) NOT NULL, 
  email VARCHAR(30) NOT NULL,
  code VARCHAR(6),
  password VARCHAR(100) NOT NULL
);

CREATE TABLE referals (
  id INT REFERENCES users(id),
  refer INT REFERENCES users(id)
);
