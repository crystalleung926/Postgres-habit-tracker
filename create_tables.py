import psycopg2


class CreateTables:
    """Database connection and table creation."""
    
    def __init__(self, host='127.0.0.1', port=5433, database='mydb', 
                 user='postgres', password='postgres'):
        self.conn_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        self.conn = None
    
    def connect(self):
        """Connect to PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            return True
        except psycopg2.Error as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create database tables."""
        schema_sql = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  age INT,
  target_goal VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS habits (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  category VARCHAR(50),
  description TEXT
);

CREATE TABLE IF NOT EXISTS habit_logs (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  habit_id INT NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
  log_date DATE NOT NULL,
  status BOOLEAN NOT NULL DEFAULT FALSE,
  note TEXT,
  UNIQUE(user_id, habit_id, log_date)
);

CREATE INDEX IF NOT EXISTS idx_habit_logs_user_id ON habit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_habit_logs_habit_id ON habit_logs(habit_id);
CREATE INDEX IF NOT EXISTS idx_habit_logs_date ON habit_logs(log_date);
"""
        queries = [q.strip() for q in schema_sql.split(';') if q.strip()]
        
        try:
            with self.conn.cursor() as cursor:
                for query in queries:
                    if query:
                        cursor.execute(query)
                self.conn.commit()
            print("Tables created successfully")
            return True
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error creating tables: {e}")
            return False


def main():
    """Create database tables."""
    db = CreateTables()
    if not db.connect():
        return
    
    try:
        db.create_tables()
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()

