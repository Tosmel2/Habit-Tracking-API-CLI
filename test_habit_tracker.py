import pytest
import sqlite3
from habit_tracker import Habit, calculate_streak

def test_habit_creation():
    h = Habit("Test Habit", "daily")
    assert h.name == "Test Habit"
    assert h.periodicity == "daily"

def test_calculate_streak_daily():
    # Consecutive days
    dates = ["2026-10-01", "2026-10-02", "2026-10-03"]
    assert calculate_streak(dates, "daily") == 3

    # Broken streak
    dates = ["2026-10-01", "2026-10-02", "2026-10-05"]
    assert calculate_streak(dates, "daily") == 2

def test_calculate_streak_weekly():
    # Consecutive weeks (7 days apart)
    dates = ["2026-10-01", "2026-10-08", "2026-10-15"]
    assert calculate_streak(dates, "weekly") == 3