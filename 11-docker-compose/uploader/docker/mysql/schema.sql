CREATE TABLE IF NOT EXISTS photo (
  id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
  lookup VARCHAR(50) UNIQUE NOT NULL,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
