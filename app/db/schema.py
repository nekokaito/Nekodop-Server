from app.db.client import DB

db = DB()

# cat table
def create_tables():
  # cats
  db.run("""
  CREATE TABLE IF NOT EXISTS cats (
      id TEXT PRIMARY KEY,
      cat_owner_id TEXT REFERENCES users(id),
      cat_name TEXT NOT NULL,
      cat_image TEXT,
      cat_age REAL,
      cat_gender TEXT,
      cat_description TEXT,
      owner_name TEXT,
      owner_address TEXT,
      owner_phone TEXT,
      owner_email TEXT,
      adopted INTEGER DEFAULT 0,
      is_approved INTEGER DEFAULT 0,
      additional_information TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  """)
  # user
  db.run("""
    CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    profile_picture TEXT,
    user_role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  """)
