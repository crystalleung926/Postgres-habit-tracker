# PostgreSQL Habit Tracker

A beginner-friendly PostgreSQL example demonstrating database operations with Python. This project uses a **habit tracking system** with three interconnected tables.

## 📋 Database Schema

The example includes 3 meaningful, reusable tables:

### 1. `users` - User Profiles
- `id` - Primary key (auto-incrementing)
- `name` - User's name
- `age` - User's age
- `target_goal` - User's personal goal

### 2. `habits` - Habit Library
- `id` - Primary key (auto-incrementing)
- `title` - Habit name
- `category` - Habit category (e.g., "Fitness", "Mindfulness")
- `description` - Detailed description

### 3. `habit_logs` - Daily Habit Tracking
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

This will start a PostgreSQL 18 container on port 5433.

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Create Database Tables

```bash
python create_tables.py
```

### Step 4: (Optional) Import Sample Data

```bash
python import_data.py
```

This will import sample users, habits, and habit logs from CSV files in the `data/` directory.

### Step 5: Run the Interactive UI

```bash
python interactive_ui.py
```

## 📁 Project Structure

```
postgres_tut/
├── postgres/
│   ├── docker-compose.yml    # Docker Compose configuration
│   └── Dockerfile            # PostgreSQL container setup
├── data/
│   ├── users.csv             # Sample user data
│   ├── habits.csv            # Sample habit data
│   └── habit_logs.csv        # Sample habit log data
├── create_tables.py          # Create database tables
├── db_service.py             # Database service layer
├── interactive_ui.py          # Interactive menu-based UI
├── import_data.py             # Import CSV data into database
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Database Connection

Default connection parameters:
- **Host**: localhost (or 127.0.0.1)
- **Port**: 5433 (changed from 5432 to avoid conflicts with local PostgreSQL)
- **Database**: mydb
- **User**: postgres
- **Password**: postgres

**Note**: Port 5433 is used instead of the default 5432 to avoid conflicts if you have a local PostgreSQL service running.

## 📚 Features

- ✅ Create database tables programmatically
- ✅ Add users and habits
- ✅ Log habit completions
- ✅ View user statistics and habit logs
- ✅ Interactive menu-based UI
- ✅ Import data from CSV files
- ✅ Demonstrates JOIN queries and foreign key relationships

## 🛠️ Usage Examples

### Using the Interactive UI

Run `python interactive_ui.py` and select from the menu:
1. Add User - Create a new user
2. Add Habit - Create a new habit
3. Log Habit - Log a habit completion
4. List All - View all users and habits
5. View User Habits - Select a user and see their habit logs and statistics
6. Exit - Quit the application

### Using the Database Service Directly

```python
from db_service import DatabaseService

service = DatabaseService()

# Add a user
user_id = service.add_user("John", 30, "Get fit")

# Add a habit
habit_id = service.add_habit("Morning Run", "Fitness", "Run 5km every morning")

# Log a habit
service.log_habit(user_id, habit_id, status=True, note="Felt great!")

# Get user logs
logs = service.get_user_logs(user_id, days=7)

# Get user statistics
stats = service.get_user_stats(user_id)
```

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

## 📝 Notes

- The schema uses `ON DELETE CASCADE` for foreign keys, meaning deleting a user or habit will automatically delete related logs
- The `habit_logs` table has a unique constraint to prevent duplicate entries for the same user/habit/date combination
- Indexes are created on foreign keys and dates for better query performance

---

**Happy Learning! 🎉**
