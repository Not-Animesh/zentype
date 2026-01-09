"""
Database Manager for ZenType
Handles SQLite database operations for storing and retrieving typing test results.
"""

import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class DatabaseManager:
    """Manages SQLite database operations for typing test results."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager with SQLite connection.
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Create data directory in home folder
            data_dir = Path.home() / ".zentype" / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(data_dir / "zentype.db")
        
        self.db_path = db_path
        self.connection = None
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database and create tables if they don't exist."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
        cursor = self.connection.cursor()
        
        # Create typing_results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS typing_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                wpm REAL NOT NULL,
                accuracy REAL NOT NULL,
                duration INTEGER NOT NULL,
                elapsed_time REAL,
                correct_chars INTEGER,
                total_chars_typed INTEGER,
                total_chars_in_test INTEGER,
                char_index INTEGER
            )
        """)
        
        self.connection.commit()

    def add_result(self, test_result: Dict) -> None:
        """
        Add a new test result to the database.
        
        Args:
            test_result: Dictionary containing test metrics (wpm, accuracy, duration, etc.)
        """
        cursor = self.connection.cursor()
        
        # Add timestamp if not present
        if "timestamp" not in test_result:
            test_result["timestamp"] = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO typing_results 
            (timestamp, wpm, accuracy, duration, elapsed_time, correct_chars, 
             total_chars_typed, total_chars_in_test, char_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_result.get("timestamp"),
            test_result.get("wpm", 0),
            test_result.get("accuracy", 0),
            test_result.get("duration", 0),
            test_result.get("elapsed_time", 0),
            test_result.get("correct_chars", 0),
            test_result.get("total_chars_typed", 0),
            test_result.get("total_chars_in_test", 0),
            test_result.get("char_index", 0),
        ))
        
        self.connection.commit()

    def get_statistics(self) -> Dict:
        """
        Calculate overall statistics from all test results.
        
        Returns:
            Dictionary with personal best WPM, average WPM, average accuracy, etc.
        """
        cursor = self.connection.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_tests,
                MAX(wpm) as best_wpm,
                AVG(wpm) as average_wpm,
                AVG(accuracy) as average_accuracy,
                SUM(total_chars_typed) as total_chars_typed
            FROM typing_results
        """)
        
        row = cursor.fetchone()
        
        if row["total_tests"] == 0:
            return {
                "total_tests": 0,
                "best_wpm": 0,
                "average_wpm": 0,
                "average_accuracy": 0,
                "total_chars_typed": 0,
            }
        
        return {
            "total_tests": row["total_tests"],
            "best_wpm": row["best_wpm"] or 0,
            "average_wpm": row["average_wpm"] or 0,
            "average_accuracy": row["average_accuracy"] or 0,
            "total_chars_typed": row["total_chars_typed"] or 0,
        }

    def get_recent_results(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent test results.
        
        Args:
            limit: Maximum number of results to return
        
        Returns:
            List of recent results in reverse chronological order
        """
        cursor = self.connection.cursor()
        
        cursor.execute("""
            SELECT timestamp, wpm, accuracy, duration, elapsed_time, 
                   correct_chars, total_chars_typed, total_chars_in_test, char_index
            FROM typing_results
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append(dict(row))
        
        return results

    def get_results_by_duration(self, duration: int) -> List[Dict]:
        """
        Get all results for a specific test duration.
        
        Args:
            duration: Test duration in seconds (30, 60, or 90)
        
        Returns:
            List of results matching the duration
        """
        cursor = self.connection.cursor()
        
        cursor.execute("""
            SELECT timestamp, wpm, accuracy, duration, elapsed_time,
                   correct_chars, total_chars_typed, total_chars_in_test, char_index
            FROM typing_results
            WHERE duration = ?
            ORDER BY timestamp DESC
        """, (duration,))
        
        results = []
        for row in cursor.fetchall():
            results.append(dict(row))
        
        return results

    def clear_all_data(self) -> None:
        """Clear all stored test results (use with caution)."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM typing_results")
        self.connection.commit()

    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()

    def __del__(self):
        """Ensure database connection is closed on object deletion."""
        self.close()
