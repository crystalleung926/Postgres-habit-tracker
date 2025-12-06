# PostgreSQL Habit Tracker Tutorial

A beginner-friendly example demonstrating PostgreSQL database operations with Python. This project uses a **habit tracking system** with three interconnected tables to teach fundamental database concepts.

## 📋 Database Schema

The example includes 3 meaningful, reusable tables:

### 1. `users` - User Profiles
Stores basic user information:
- `id` - Primary key (auto-incrementing)
- `name` - User's name
- `age` - User's age
- `target_goal` - User's personal goal

### 2. `habits` - Habit Library
A catalog of healthy habits:
- `id` - Primary key (auto-incrementing)
- `title` - Habit name
- `category` - Habit category (e.g., "Fitness", "Mindfulness")
- `description` - Detailed description

### 3. `habit_logs` - Daily Habit Tracking
Records daily habit completion:
- `id` - Primary key (auto-incrementing)
- `user_id` - Foreign key to `users` table
- `habit_id` - Foreign key to `habits` table
- `log_date` - Date of the log entry
- `status` - Boolean indicating completion (TRUE/FALSE)
- `note` - Optional note about the entry
- Unique constraint on `(user_id, habit_id, log_date)` to prevent duplicates

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.7+ installed

### Step 1: Start PostgreSQL Database

```bash
cd postgres
docker-compose up -d
```

This will:
- Start a PostgreSQL 18 container
- Automatically create the database schema
- Load sample data for demonstration

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Example

```bash
python example.py
```

The example script demonstrates:
- ✅ Connecting to PostgreSQL
- ✅ Creating users and habits
- ✅ Logging habit completions
- ✅ Querying data with JOINs
- ✅ Calculating statistics
- ✅ Filtering and searching

## 📁 Project Structure

```
postgres_tut/
├── postgres/
│   ├── docker-compose.yml    # Docker Compose configuration
│   ├── Dockerfile            # PostgreSQL container setup
│   ├── schema.sql            # Database schema definition
│   └── init.sql              # Sample data initialization
├── example.py                # Python example demonstrating all operations
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Database Connection

Default connection parameters:
- **Host**: localhost (or 127.0.0.1)
- **Port**: 5433 (changed from 5432 to avoid conflicts with local PostgreSQL)
- **Database**: mydb
- **User**: postgres
- **Password**: postgres

**Note**: Port 5433 is used instead of the default 5432 to avoid conflicts if you have a local PostgreSQL service running.

You can modify these in `example.py` or `docker-compose.yml`.

## 📚 Example Queries

### Get all users
```python
users = db.get_all_users()
```

### Create a new habit
```python
habit_id = db.create_habit(
    title="Morning Run",
    category="Fitness",
    description="Run for 30 minutes every morning"
)
```

### Log a habit completion
```python
db.log_habit(
    user_id=1,
    habit_id=1,
    log_date=date.today(),
    status=True,
    note="Felt great!"
)
```

### Get user's habit logs
```python
logs = db.get_user_habit_logs(user_id=1, days=7)
```

### Get user statistics
```python
stats = db.get_user_stats(user_id=1)
```

## 🛠️ Customization

### Modify Schema
Edit `postgres/schema.sql` to add columns or tables.

### Add Sample Data
Edit `postgres/init.sql` to customize initial data.

### Extend Functionality
The `HabitTrackerDB` class in `example.py` can be extended with additional methods.

## 🧹 Cleanup

To stop and remove the database container:

```bash
cd postgres
docker-compose down
```

To also remove the database volume (deletes all data):

```bash
docker-compose down -v
```

## 📖 Learning Points

This example teaches:
- **Primary Keys**: Auto-incrementing IDs
- **Foreign Keys**: Relationships between tables
- **JOINs**: Combining data from multiple tables
- **Constraints**: Unique constraints and referential integrity
- **Indexes**: Performance optimization
- **Transactions**: Safe database operations
- **Best Practices**: Error handling, connection management

## 🎯 Use Cases

This schema can be adapted for:
- Personal habit tracking apps
- Fitness and wellness applications
- Goal tracking systems
- Daily routine management
- Learning management systems (with modifications)

## 📝 Notes

- The schema uses `ON DELETE CASCADE` for foreign keys, meaning deleting a user or habit will automatically delete related logs
- The `habit_logs` table has a unique constraint to prevent duplicate entries for the same user/habit/date combination
- Indexes are created on foreign keys and dates for better query performance

## 🤝 Contributing

Feel free to extend this example with:
- Additional tables (e.g., `reminders`, `achievements`)
- More complex queries (e.g., streaks, weekly summaries)
- User authentication
- API endpoints

---

**Happy Learning! 🎉**

