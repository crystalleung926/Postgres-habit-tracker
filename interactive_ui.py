"""
Habit Tracker Interactive UI
Interactive menu-based interface for managing users, habits, and habit logs.
"""

from datetime import date, datetime
from db_service import DatabaseService


def parse_date(date_str: str) -> date:
    """Parse date string in YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None


def parse_bool(value: str) -> bool:
    """Parse boolean string."""
    return value.lower() in ('true', 't', 'yes', 'y', '1')


def show_menu():
    """Display main menu."""
    print("\n" + "=" * 50)
    print("HABIT TRACKER")
    print("=" * 50)
    print("1. Add User")
    print("2. Add Habit")
    print("3. Log Habit")
    print("4. List All")
    print("5. View User Habits")
    print("6. Exit")
    print("=" * 50)


def add_user_interactive(service):
    """Interactive add user."""
    print("\n--- Add New User ---")
    name = input("Name: ").strip()
    if not name:
        print("Name is required!")
        return
    
    age_input = input("Age (optional): ").strip()
    age = int(age_input) if age_input else None
    
    goal = input("Target goal (optional): ").strip() or None
    
    user_id = service.add_user(name, age, goal)
    if user_id:
        print(f"\n✅ User created successfully! ID: {user_id}")
    else:
        print("\n❌ Failed to create user")


def add_habit_interactive(service):
    """Interactive add habit."""
    print("\n--- Add New Habit ---")
    title = input("Title: ").strip()
    if not title:
        print("Title is required!")
        return
    
    category = input("Category (optional): ").strip() or None
    description = input("Description (optional): ").strip() or None
    
    habit_id = service.add_habit(title, category, description)
    if habit_id:
        print(f"\n✅ Habit created successfully! ID: {habit_id}")
    else:
        print("\n❌ Failed to create habit")


def log_habit_interactive(service):
    """Interactive log habit."""
    print("\n--- Log Habit Completion ---")
    
    # Show users
    users = service.get_users()
    if not users:
        print("No users found. Please add a user first.")
        return
    print("\nUsers:")
    for user in users:
        print(f"  [{user['id']}] {user['name']}")
    
    user_id_input = input("\nUser ID: ").strip()
    try:
        user_id = int(user_id_input)
    except ValueError:
        print("Invalid user ID!")
        return
    
    # Show habits
    habits = service.get_habits()
    if not habits:
        print("No habits found. Please add a habit first.")
        return
    print("\nHabits:")
    for habit in habits:
        print(f"  [{habit['id']}] {habit['title']}")
    
    habit_id_input = input("\nHabit ID: ").strip()
    try:
        habit_id = int(habit_id_input)
    except ValueError:
        print("Invalid habit ID!")
        return
    
    date_input = input("Date (YYYY-MM-DD, or press Enter for today): ").strip()
    log_date = parse_date(date_input) if date_input else date.today()
    if log_date is None:
        print("Invalid date format!")
        return
    
    status_input = input("Completed? (y/n, default: y): ").strip()
    status = parse_bool(status_input) if status_input else True
    
    note = input("Note (optional): ").strip() or None
    
    if service.log_habit(user_id, habit_id, log_date, status, note):
        print(f"\n✅ Habit logged successfully!")
    else:
        print("\n❌ Failed to log habit")


def list_all_interactive(service):
    """Interactive list all."""
    print("\n--- All Users and Habits ---")
    
    users = service.get_users()
    habits = service.get_habits()
    
    print("\n👥 Users:")
    if users:
        for user in users:
            print(f"  [{user['id']}] {user['name']}", end="")
            if user.get('age'):
                print(f" (Age: {user['age']})", end="")
            if user.get('target_goal'):
                print(f" - Goal: {user['target_goal']}", end="")
            print()
    else:
        print("  No users found")
    
    print("\n🏃 Habits:")
    if habits:
        for habit in habits:
            print(f"  [{habit['id']}] {habit['title']}", end="")
            if habit.get('category'):
                print(f" ({habit['category']})", end="")
            if habit.get('description'):
                print(f" - {habit['description']}", end="")
            print()
    else:
        print("  No habits found")


def view_user_habits_interactive(service):
    """Interactive view user habits."""
    print("\n--- View User Habits ---")
    
    # Show users
    users = service.get_users()
    if not users:
        print("No users found. Please add a user first.")
        return
    
    print("\nUsers:")
    for user in users:
        print(f"  [{user['id']}] {user['name']}")
    
    user_id_input = input("\nSelect User ID: ").strip()
    try:
        user_id = int(user_id_input)
    except ValueError:
        print("Invalid user ID!")
        return
    
    # Find selected user
    selected_user = None
    for user in users:
        if user['id'] == user_id:
            selected_user = user
            break
    
    if not selected_user:
        print("User not found!")
        return
    
    # Show user info
    print(f"\n{'=' * 50}")
    print(f"User: {selected_user['name']}")
    if selected_user.get('age'):
        print(f"Age: {selected_user['age']}")
    if selected_user.get('target_goal'):
        print(f"Goal: {selected_user['target_goal']}")
    print(f"{'=' * 50}")
    
    # Get user statistics
    stats = service.get_user_stats(user_id)
    if stats.get('total_logs', 0) > 0:
        print(f"\n📊 Statistics:")
        print(f"  Total logs: {stats.get('total_logs', 0)}")
        print(f"  Completed: {stats.get('completed_count', 0)}")
        print(f"  Missed: {stats.get('missed_count', 0)}")
        print(f"  Completion rate: {stats.get('completion_rate', 0)}%")
    
    # Get user habit logs
    logs = service.get_user_logs(user_id, days=30)
    
    if logs:
        print(f"\n📋 Habit Logs (Last 30 days):")
        print("-" * 50)
        for log in logs:
            status_icon = "✅" if log['status'] else "❌"
            print(f"\n  {status_icon} {log['log_date']}")
            print(f"     Habit: {log['habit_title']} ({log.get('habit_category', 'N/A')})")
            if log.get('note'):
                print(f"     Note: {log['note']}")
    else:
        print("\n📋 No habit logs found for this user.")


def main():
    """Main interactive UI entry point."""
    service = DatabaseService()
    
    print("Welcome to Habit Tracker!")
    print("Make sure the database tables are created (run: python create_tables.py)")
    
    while True:
        show_menu()
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            add_user_interactive(service)
        elif choice == '2':
            add_habit_interactive(service)
        elif choice == '3':
            log_habit_interactive(service)
        elif choice == '4':
            list_all_interactive(service)
        elif choice == '5':
            view_user_habits_interactive(service)
        elif choice == '6':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid option. Please select 1-6.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    main()

