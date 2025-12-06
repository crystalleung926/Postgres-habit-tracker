"""
Import CSV data into PostgreSQL database.
"""

import csv
from datetime import datetime
from db_service import DatabaseService


def import_users(service, csv_file):
    """Import users from CSV."""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            age = int(row['age']) if row['age'] else None
            goal = row['target_goal'] if row['target_goal'] else None
            user_id = service.add_user(row['name'], age, goal)
            if user_id:
                count += 1
        print(f"✅ Imported {count} users")


def import_habits(service, csv_file):
    """Import habits from CSV."""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            category = row['category'] if row['category'] else None
            description = row['description'] if row['description'] else None
            habit_id = service.add_habit(row['title'], category, description)
            if habit_id:
                count += 1
        print(f"✅ Imported {count} habits")


def import_habit_logs(service, csv_file):
    """Import habit logs from CSV."""
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            user_id = int(row['user_id'])
            habit_id = int(row['habit_id'])
            log_date = datetime.strptime(row['log_date'], '%Y-%m-%d').date()
            status = row['status'].lower() == 'true'
            note = row['note'] if row['note'] else None
            
            if service.log_habit(user_id, habit_id, log_date, status, note):
                count += 1
        print(f"✅ Imported {count} habit logs")


def main():
    """Import all CSV data."""
    service = DatabaseService()
    
    print("Starting data import...")
    print("=" * 50)
    
    try:
        import_users(service, 'data/users.csv')
        import_habits(service, 'data/habits.csv')
        import_habit_logs(service, 'data/habit_logs.csv')
        
        print("\n" + "=" * 50)
        print("✅ All data imported successfully!")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure the CSV files are in the 'data' directory")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    main()

