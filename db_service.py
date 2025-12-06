import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date, timedelta
from typing import List, Dict, Optional


class DatabaseService:
    """Database service layer for habit tracker operations."""
    
    def __init__(self, host='127.0.0.1', port=5433, database='mydb', 
                 user='postgres', password='postgres'):
        self.conn_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
    
    def _execute(self, query: str, params: tuple = None, fetch: bool = False):
        """Execute SQL query with automatic connection management."""
        conn = None
        try:
            conn = psycopg2.connect(**self.conn_params)
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                    conn.commit()
                    return result
                conn.commit()
                return True
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Error: {e}")
            return None
        finally:
            if conn:
                conn.close()
    
    # User operations
    def add_user(self, name: str, age: Optional[int] = None, 
                 target_goal: Optional[str] = None) -> Optional[int]:
        """Add a new user."""
        query = "INSERT INTO users (name, age, target_goal) VALUES (%s, %s, %s) RETURNING id"
        result = self._execute(query, (name, age, target_goal), fetch=True)
        return result[0]['id'] if result else None
    
    def get_users(self) -> List[Dict]:
        """Get all users."""
        return self._execute("SELECT * FROM users ORDER BY id", fetch=True) or []
    
    # Habit operations
    def add_habit(self, title: str, category: Optional[str] = None,
                  description: Optional[str] = None) -> Optional[int]:
        """Add a new habit."""
        query = "INSERT INTO habits (title, category, description) VALUES (%s, %s, %s) RETURNING id"
        result = self._execute(query, (title, category, description), fetch=True)
        return result[0]['id'] if result else None
    
    def get_habits(self) -> List[Dict]:
        """Get all habits."""
        return self._execute("SELECT * FROM habits ORDER BY id", fetch=True) or []
    
    # Habit log operations
    def log_habit(self, user_id: int, habit_id: int, log_date: date = None,
                  status: bool = True, note: Optional[str] = None) -> bool:
        """Log a habit completion."""
        if log_date is None:
            log_date = date.today()
        query = """
            INSERT INTO habit_logs (user_id, habit_id, log_date, status, note)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id, habit_id, log_date)
            DO UPDATE SET status = EXCLUDED.status, note = EXCLUDED.note
        """
        return self._execute(query, (user_id, habit_id, log_date, status, note)) is True
    
    def get_user_logs(self, user_id: int, days: int = 30) -> List[Dict]:
        """Get habit logs for a user within the last N days."""
        start_date = date.today() - timedelta(days=days)
        query = """
            SELECT 
                hl.id,
                hl.log_date,
                hl.status,
                hl.note,
                h.title as habit_title,
                h.category as habit_category,
                h.description as habit_description
            FROM habit_logs hl
            JOIN habits h ON hl.habit_id = h.id
            WHERE hl.user_id = %s 
            AND hl.log_date >= %s
            ORDER BY hl.log_date DESC, h.title
        """
        return self._execute(query, (user_id, start_date), fetch=True) or []
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get statistics for a user's habit completion."""
        query = """
            SELECT 
                COUNT(*) as total_logs,
                SUM(CASE WHEN status = TRUE THEN 1 ELSE 0 END) as completed_count,
                SUM(CASE WHEN status = FALSE THEN 1 ELSE 0 END) as missed_count,
                ROUND(
                    100.0 * SUM(CASE WHEN status = TRUE THEN 1 ELSE 0 END) / 
                    NULLIF(COUNT(*), 0),
                    2
                ) as completion_rate
            FROM habit_logs
            WHERE user_id = %s
        """
        result = self._execute(query, (user_id,), fetch=True)
        return result[0] if result else {}

