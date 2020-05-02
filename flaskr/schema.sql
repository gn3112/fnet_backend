CREATE TABLE IF NOT EXISTS store (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  image BLOB
);

CREATE TABLE IF NOT EXISTS camera1 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  image_capture INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_name TEXT,
  product_image_loc TEXT
);

INSERT OR IGNORE INTO store (id, image) VALUES (1, '');
INSERT OR IGNORE INTO store (id, image) VALUES (2, '');

INSERT OR IGNORE INTO camera1 (id, image_capture) VALUES (1,0);

INSERT INTO products (product_name, product_image_loc) VALUES ("Beurre president", "lemon.jpg");