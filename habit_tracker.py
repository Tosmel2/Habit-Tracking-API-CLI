import sqlite3
from datetime import datetime, timedelta
from functools import reduce

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            periodicity TEXT,
            creation_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS completions (
            habit_name TEXT,
            completion_date TEXT,
            FOREIGN KEY(habit_name) REFERENCES habits(name)
        )
    ''')
    conn.commit()
    return conn

# --- OOP: HABIT CLASS ---
class Habit:
    def __init__(self, name, periodicity, creation_date=None):
        self.name = name
        self.periodicity = periodicity
        self.creation_date = creation_date or datetime.now().strftime("%Y-%m-%d")

    def store(self, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO habits VALUES (?, ?, ?)", 
                       (self.name, self.periodicity, self.creation_date))
        conn.commit()

    def complete(self, conn, date_str=None):
        cursor = conn.cursor()
        date_str = date_str or datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO completions VALUES (?, ?)", (self.name, date_str))
        conn.commit()

# --- FUNCTIONAL ANALYTICS MODULE ---
def get_all_habits(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name, periodicity, creation_date FROM habits")
    return list(map(lambda row: Habit(row[0], row[1], row[2]), cursor.fetchall()))

def filter_by_periodicity(habits, periodicity):
    return list(filter(lambda h: h.periodicity == periodicity, habits))

def calculate_streak(dates, periodicity):
    if not dates: return 0
    # Functional approach to sort and calculate consecutive days/weeks
    sorted_dates = sorted(list(map(lambda d: datetime.strptime(d, "%Y-%m-%d"), dates)))
    
    def streak_reducer(acc, current_date):
        current_streak, max_streak, last_date = acc
        if not last_date:
            return (1, 1, current_date)
        
        diff = (current_date - last_date).days
        valid_gap = 1 if periodicity == "daily" else 7
        
        if diff <= valid_gap and diff > 0:
            return (current_streak + 1, max(max_streak, current_streak + 1), current_date)
        elif diff > valid_gap:
            return (1, max_streak, current_date)
        return acc

    _, final_max, _ = reduce(streak_reducer, sorted_dates, (0, 0, None))
    return final_max

def get_habit_completions(conn, habit_name):
    cursor = conn.cursor()
    cursor.execute("SELECT completion_date FROM completions WHERE habit_name = ?", (habit_name,))
    return list(map(lambda row: row[0], cursor.fetchall()))

def max_streak_for_habit(conn, habit_name, periodicity):
    dates = get_habit_completions(conn, habit_name)
    return calculate_streak(dates, periodicity)

def max_streak_all_habits(conn):
    habits = get_all_habits(conn)
    streaks = list(map(lambda h: max_streak_for_habit(conn, h.name, h.periodicity), habits))
    return max(streaks) if streaks else 0

# --- SEED FIXTURES (4 WEEKS DATA) ---
def seed_data(conn):
    habits = [
        Habit("Drink Water", "daily", "2026-09-01"),
        Habit("Read 10 Pages", "daily", "2026-09-01"),
        Habit("Run 5k", "weekly", "2026-09-01"),
        Habit("Call Parents", "weekly", "2026-09-01"),
        Habit("Meditate", "daily", "2026-09-01")
    ]
    for h in habits:
        h.store(conn)
        # Generate 4 weeks of mock data
        if h.periodicity == "daily":
            for i in range(28):
                h.complete(conn, (datetime(2026, 9, 1) + timedelta(days=i)).strftime("%Y-%m-%d"))
        else:
            for i in range(4):
                h.complete(conn, (datetime(2026, 9, 1) + timedelta(weeks=i)).strftime("%Y-%m-%d"))

# --- CLI ---
def cli():
    conn = init_db()
    seed_data(conn)
    print("Welcome to Habit Tracker! (Pre-seeded with 4 weeks of data)")
    while True:
        print("\n1. List all habits\n2. Create habit\n3. Check-off habit\n4. Analytics Dashboard\n5. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            for h in get_all_habits(conn): print(f"- {h.name} ({h.periodicity})")
        elif choice == '2':
            name = input("Habit name: ")
            period = input("Period (daily/weekly): ")
            Habit(name, period).store(conn)
            print("Habit created.")
        elif choice == '3':
            name = input("Habit name: ")
            Habit(name, "daily").complete(conn)
            print("Task completed!")
        elif choice == '4':
            print(f"Longest Streak All Habits: {max_streak_all_habits(conn)}")
        elif choice == '5':
            break

if __name__ == "__main__":
    cli()