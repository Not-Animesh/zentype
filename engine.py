"""
Core Typing Engine for ZenType
Handles character validation, WPM calculation, accuracy tracking, and test state management.
"""

import time
import logging
from typing import List, Tuple

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TypingEngine:
    """
    Core engine managing typing test logic, statistics, and validation.
    Character-level control for precise feedback on typing accuracy.
    """

    def __init__(self, target_text: str, duration_seconds: int):
        """
        Initialize typing engine with target text and duration.

        Args:
            target_text: The text that user must type
            duration_seconds: Test duration (30, 60, or 90 seconds)
        """
        self.target_text = target_text
        self.duration_seconds = duration_seconds

        # Typing state variables
        self.input_text = ""
        self.char_index = 0
        self.is_active = False
        self.start_time = None
        self.end_time = None

        # Statistics tracking
        self.correct_chars = 0
        self.total_chars_typed = 0
        self.keystrokes = []  # List of (char, is_correct, timestamp)

        # Current word tracking for backspace restriction
        self.current_word_start = 0  # Character index where current word begins

    def calculate_current_word_start(self) -> int:
        """
        Find the starting index of the current word (last space + 1).

        Returns:
            Index of current word start
        """
        # Search backwards from char_index to find the last space
        for i in range(self.char_index - 1, -1, -1):
            if self.target_text[i] == " ":
                return i + 1
        return 0  # Beginning of text if no space found

    def handle_keypress(self, char: str) -> Tuple[bool, int]:
        """
        Process a keypress and validate against target text.
        Returns whether character is correct and current character index.

        Args:
            char: The character pressed by user

        Returns:
            Tuple of (is_correct: bool, char_index: int)
        """
        if not self.is_active:
            # Auto-start timer on first keypress
            self.start_timer()

        if self.char_index >= len(self.target_text):
            # Already completed
            return False, self.char_index

        target_char = self.target_text[self.char_index]
        is_correct = char == target_char

        if is_correct:
            self.correct_chars += 1

        self.input_text += char
        self.total_chars_typed += 1
        self.char_index += 1
        self.keystrokes.append((char, is_correct, time.time()))

        return is_correct, self.char_index

    def handle_backspace(self) -> int:
        """
        Handle backspace with restriction: only allow within current word.
        Cannot backspace across word boundaries.

        Returns:
            Updated character index
        """
        if self.char_index <= 0:
            return self.char_index

        # Calculate where current word starts
        current_word_start = self.calculate_current_word_start()

        # Only allow backspace if not at word boundary
        if self.char_index > current_word_start:
            self.char_index -= 1
            self.input_text = self.input_text[:-1]
            self.total_chars_typed += 1  # Backspace counts as a keystroke
            self.keystrokes.append(("BACKSPACE", False, time.time()))

            return self.char_index
        else:
            # Cannot backspace - at word boundary
            return self.char_index

    def start_timer(self) -> None:
        """Start the test timer on first keypress."""
        if not self.is_active:
            self.is_active = True
            self.start_time = time.time()
            logger.debug(f"Timer started. start_time={self.start_time}")

    def get_elapsed_time(self) -> float:
        """
        Get elapsed time in seconds.

        Returns:
            Seconds elapsed since test started, or 0 if not started
        """
        if self.start_time is None:
            return 0
        
        # If test is finished, use end_time; otherwise use current time
        if self.end_time is not None:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    def is_time_exceeded(self) -> bool:
        """
        Check if time limit has been exceeded.

        Returns:
            True if elapsed time >= duration_seconds
        """
        return self.get_elapsed_time() >= self.duration_seconds

    def is_completed(self) -> bool:
        """
        Check if test is completed (time limit reached).

        Returns:
            True if time limit exceeded or all text typed
        """
        return self.is_time_exceeded() or self.char_index >= len(self.target_text)

    def calculate_wpm(self) -> float:
        """
        Calculate Words Per Minute using standard formula.
        Formula: (Correct Characters / 5) / (Time in Minutes)
        5 is the standard characters-per-word assumption.

        Returns:
            WPM as float, or 0 if test not started
        """
        elapsed_time = self.get_elapsed_time()
        
        # Debug output
        logger.debug(f"calculate_wpm: elapsed_time={elapsed_time:.2f}s, correct_chars={self.correct_chars}, is_active={self.is_active}")
        
        if elapsed_time == 0:
            return 0.0

        elapsed_minutes = elapsed_time / 60.0
        words = self.correct_chars / 5.0  # Standard CPM to WPM conversion
        wpm = words / elapsed_minutes if elapsed_minutes > 0 else 0.0
        
        logger.debug(f"calculate_wpm: calculated WPM={wpm:.2f}")
        
        return wpm

    def calculate_accuracy(self) -> float:
        """
        Calculate accuracy percentage.
        Formula: (Correct Keystrokes / Total Keystrokes) * 100

        Returns:
            Accuracy as percentage (0-100), or 0 if no keystrokes
        """
        # Debug output
        logger.debug(f"calculate_accuracy: correct_chars={self.correct_chars}, total_chars_typed={self.total_chars_typed}")
        
        if self.total_chars_typed == 0:
            return 0.0

        accuracy = (self.correct_chars / self.total_chars_typed) * 100.0
        
        logger.debug(f"calculate_accuracy: calculated accuracy={accuracy:.2f}%")
        
        return accuracy

    def get_character_status(self, index: int) -> str:
        """
        Get status of character at given index.
        Used for determining text coloring.

        Args:
            index: Character position in target text

        Returns:
            Status: "unwritten", "correct", or "error"
        """
        if index >= self.char_index:
            return "unwritten"
        elif index < len(self.input_text):
            # Check if this character matches
            is_correct = self.target_text[index] == self.input_text[index]
            return "correct" if is_correct else "error"
        else:
            return "unwritten"

    def finish_test(self) -> None:
        """Mark test as finished and record end time."""
        logger.debug(f"finish_test: Called. is_active={self.is_active}, start_time={self.start_time}")
        
        self.is_active = False
        self.end_time = time.time()
        
        # Calculate final metrics immediately
        final_wpm = self.calculate_wpm()
        final_accuracy = self.calculate_accuracy()
        
        logger.debug(f"finish_test: Test finished. end_time={self.end_time}, final WPM={final_wpm:.2f}, final accuracy={final_accuracy:.2f}%")

    def get_test_results(self) -> dict:
        """
        Compile all test statistics into results dictionary.

        Returns:
            Dictionary with all test metrics
        """
        elapsed_time = self.get_elapsed_time()
        return {
            "wpm": round(self.calculate_wpm(), 2),
            "accuracy": round(self.calculate_accuracy(), 2),
            "duration": self.duration_seconds,
            "elapsed_time": round(elapsed_time, 2),
            "correct_chars": self.correct_chars,
            "total_chars_typed": self.total_chars_typed,
            "total_chars_in_test": len(self.target_text),
            "char_index": self.char_index,
        }

    def get_wpm_history(self, interval: float = 1.0) -> List[float]:
        """
        Get WPM progression over time at specified intervals.
        Used for charting WPM over time.

        Args:
            interval: Time interval in seconds between data points (default: 1.0)

        Returns:
            List of WPM values at each interval
        """
        wpm_history = []
        elapsed = self.get_elapsed_time()

        # Generate data points at regular intervals
        for t in [i * interval for i in range(int(elapsed / interval) + 1)]:
            if t == 0:
                wpm_history.append(0)
            else:
                # Count correct chars up to time t
                correct_at_time = sum(
                    1 for char, is_correct, ts in self.keystrokes
                    if ts - self.start_time <= t and is_correct
                )
                words = correct_at_time / 5.0
                wpm = words / (t / 60.0)
                wpm_history.append(max(0, wpm))

        return wpm_history

    def reset(self) -> None:
        """Reset all test state variables for new test."""
        self.input_text = ""
        self.char_index = 0
        self.is_active = False
        self.start_time = None
        self.end_time = None
        self.correct_chars = 0
        self.total_chars_typed = 0
        self.keystrokes = []
        self.current_word_start = 0
