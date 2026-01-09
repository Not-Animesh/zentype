"""
Word Generation System for ZenType
Handles word list management and random text generation for typing tests.
"""

import random


class WordProvider:
    """Manages word list and generates random text blocks for typing tests."""

    # Curated list of common English words for typing tests
    WORDS = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
        "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
        "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
        "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
        "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
        "is", "was", "are", "been", "being", "have", "has", "had", "having", "do",
        "does", "did", "doing", "go", "goes", "went", "gone", "going", "make", "makes",
        "made", "making", "get", "gets", "got", "getting", "know", "knows", "knew", "knowing",
        "think", "thinks", "thought", "thinking", "see", "sees", "saw", "seeing", "come", "comes",
        "came", "coming", "could", "would", "should", "may", "might", "must", "can", "will",
        "shall", "want", "wants", "wanted", "wanting", "need", "needs", "needed", "needing", "try",
        "tries", "tried", "trying", "use", "uses", "used", "using", "find", "finds", "found",
        "finding", "give", "gives", "gave", "giving", "tell", "tells", "told", "telling", "ask",
        "asks", "asked", "asking", "work", "works", "worked", "working", "seem", "seems", "seemed",
        "seeming", "help", "helps", "helped", "helping", "talk", "talks", "talked", "talking", "turn",
        "turns", "turned", "turning", "start", "starts", "started", "starting", "show", "shows", "showed",
        "showing", "hear", "hears", "heard", "hearing", "let", "lets", "letting", "mean", "means",
        "meant", "meaning", "set", "sets", "setting", "meet", "meets", "meeting", "run", "runs",
        "ran", "running", "pay", "pays", "paid", "paying", "sit", "sits", "sat", "sitting",
    ]

    @staticmethod
    def generate_text(word_count: int) -> str:
        """
        Generate random text block from word list.

        Args:
            word_count: Number of words to generate

        Returns:
            String of space-separated random words
        """
        selected_words = random.choices(WordProvider.WORDS, k=word_count)
        return " ".join(selected_words)

    @staticmethod
    def get_word_count_for_duration(duration_seconds: int) -> int:
        """
        Calculate appropriate word count for given duration.
        Assumes average typing speed of ~40 WPM for balanced difficulty.

        Args:
            duration_seconds: Test duration in seconds

        Returns:
            Recommended number of words
        """
        # 40 WPM = 200 characters per minute = ~3.3 chars/second
        # Average word is ~5 chars, so ~0.66 words per second
        # Add buffer for slower typists
        words_per_second = 0.6
        return max(30, int(duration_seconds * words_per_second))
