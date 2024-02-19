CREATE TABLE users (
  id INT PRIMARY KEY,
  FirstName VARCHAR(15) NOT NULL,
  LastName VARCHAR(15) NOT NULL, 
  Email VARCHAR(30) NOT NULL
  Code VARCHAR(6)
);

CREATE TABLE referals (
  id INT REFERENCES users(id),
  refer INT REFERENCES users(id)
);
