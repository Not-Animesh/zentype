"""
Local Data Persistence Manager for ZenType
Handles JSON file operations for storing and retrieving typing test results.
All data stored locally - no external database required.
"""

import json
import os
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class DataManager:
    """Manages local JSON-based data persistence for typing test results."""

    def __init__(self):
        """Initialize data manager with local data directory."""
        # Create data directory in home folder
        self.data_dir = Path.home() / ".zentype" / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.results_file = self.data_dir / "typing_results.json"

        # Initialize results file if it doesn't exist
        if not self.results_file.exists():
            self._init_results_file()

    def _init_results_file(self) -> None:
        """Initialize empty results file with proper structure."""
        self.save_results([])

    def save_results(self, results: List[Dict]) -> None:
        """
        Save typing results to JSON file.

        Args:
            results: List of test result dictionaries
        """
        try:
            with open(self.results_file, "w") as f:
                json.dump(results, f, indent=2)
        except Exception as e:
            print(f"Error saving results: {e}")

    def load_results(self) -> List[Dict]:
        """
        Load all typing results from JSON file.

        Returns:
            List of test result dictionaries
        """
        try:
            if self.results_file.exists():
                with open(self.results_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading results: {e}")
        return []

    def add_result(self, test_result: Dict) -> None:
        """
        Add a new test result to the results file.

        Args:
            test_result: Dictionary containing test metrics (wpm, accuracy, duration, etc.)
        """
        results = self.load_results()

        # Add timestamp if not present
        if "timestamp" not in test_result:
            test_result["timestamp"] = datetime.now().isoformat()

        results.append(test_result)
        self.save_results(results)

    def get_statistics(self) -> Dict:
        """
        Calculate overall statistics from all test results.

        Returns:
            Dictionary with personal best WPM, average WPM, average accuracy, etc.
        """
        results = self.load_results()

        if not results:
            return {
                "total_tests": 0,
                "best_wpm": 0,
                "average_wpm": 0,
                "average_accuracy": 0,
                "total_chars_typed": 0,
            }

        wpm_values = [r.get("wpm", 0) for r in results]
        accuracy_values = [r.get("accuracy", 0) for r in results]
        total_chars = sum(r.get("total_chars_typed", 0) for r in results)

        return {
            "total_tests": len(results),
            "best_wpm": max(wpm_values) if wpm_values else 0,
            "average_wpm": sum(wpm_values) / len(wpm_values) if wpm_values else 0,
            "average_accuracy": sum(accuracy_values) / len(accuracy_values) if accuracy_values else 0,
            "total_chars_typed": total_chars,
        }

    def get_results_by_duration(self, duration: int) -> List[Dict]:
        """
        Get all results for a specific test duration.

        Args:
            duration: Test duration in seconds (30, 60, or 90)

        Returns:
            List of results matching the duration
        """
        results = self.load_results()
        return [r for r in results if r.get("duration") == duration]

    def get_recent_results(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent test results.

        Args:
            limit: Maximum number of results to return

        Returns:
            List of recent results in reverse chronological order
        """
        results = self.load_results()
        # Sort by timestamp in reverse (newest first)
        sorted_results = sorted(
            results, key=lambda x: x.get("timestamp", ""), reverse=True
        )
        return sorted_results[:limit]

    def export_to_csv(self, filepath: str) -> bool:
        """
        Export all test results to CSV file.

        Args:
            filepath: Path where CSV file should be saved

        Returns:
            True if export successful, False otherwise
        """
        try:
            import csv
            results = self.load_results()

            if not results:
                return False

            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "timestamp",
                        "wpm",
                        "accuracy",
                        "duration",
                        "correct_chars",
                        "total_chars_typed",
                    ],
                )
                writer.writeheader()
                writer.writerows(results)

            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False

    def clear_all_data(self) -> None:
        """Clear all stored test results (use with caution)."""
        self.save_results([])
