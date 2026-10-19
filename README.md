# Habit Tracker API
A robust Python CLI backend for tracking daily and weekly habits.

## Installation
1. Ensure Python 3.7+ is installed.
2. Clone this repository.
3. Install testing dependencies: `pip install pytest`

## Usage
Run the application via the command line:
`python habit_tracker.py`

The application automatically seeds an SQLite database (`habits.db`) with 5 predefined habits and 4 weeks of historical tracking data on the first run.

## Testing
Run the unit test suite to validate streak logic and OOP models:<br>
`pytest test_habit_tracker.py` <br>
`python -m pytest -v test_habit_tracker.py`