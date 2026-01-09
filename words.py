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
        # Additional 500+ commonly used words
        "call", "try", "need", "feel", "become", "leave", "put", "hand", "keep", "child",
        "eye", "follow", "never", "stand", "group", "play", "such", "again", "move", "change",
        "live", "off", "face", "public", "already", "speak", "others", "read", "level", "allow",
        "add", "office", "spend", "door", "health", "person", "art", "sure", "war", "history",
        "party", "within", "grow", "result", "open", "morning", "walk", "reason", "low", "win",
        "research", "girl", "guy", "early", "food", "before", "moment", "himself", "air", "teacher",
        "force", "offer", "enough", "both", "across", "although", "remember", "foot", "second", "boy",
        "maybe", "toward", "able", "age", "policy", "everything", "love", "process", "music", "including",
        "consider", "appear", "actually", "buy", "probably", "human", "wait", "serve", "market", "die",
        "send", "expect", "home", "sense", "build", "stay", "fall", "nation", "plan", "cut",
        "college", "interest", "death", "course", "someone", "experience", "behind", "reach", "local", "kill",
        "six", "remain", "effect", "yeah", "suggest", "class", "control", "raise", "care", "perhaps",
        "little", "late", "hard", "field", "else", "pass", "former", "sell", "major", "sometimes",
        "require", "along", "development", "themselves", "report", "role", "better", "economic", "effort", "decide",
        "rate", "strong", "possible", "heart", "drug", "show", "leader", "light", "voice", "wife",
        "whole", "police", "mind", "finally", "pull", "return", "free", "military", "price", "report",
        "less", "according", "decision", "explain", "son", "hope", "even", "develop", "view", "relationship",
        "carry", "town", "road", "drive", "arm", "true", "federal", "break", "better", "difference",
        "thank", "receive", "value", "international", "building", "action", "full", "model", "join", "season",
        "society", "because", "tax", "director", "early", "position", "player", "agree", "especially", "record",
        "pick", "wear", "paper", "special", "space", "ground", "form", "support", "event", "official",
        "whose", "matter", "everyone", "center", "couple", "site", "end", "project", "hit", "base",
        "activity", "star", "table", "need", "court", "produce", "eat", "american", "teach", "oil",
        "half", "situation", "easy", "cost", "industry", "figure", "street", "image", "itself", "phone",
        "either", "data", "cover", "quite", "picture", "clear", "practice", "piece", "land", "recent",
        "describe", "product", "doctor", "wall", "patient", "worker", "news", "test", "movie", "certain",
        "north", "personal", "open", "support", "simply", "third", "technology", "catch", "step", "baby",
        "computer", "type", "attention", "draw", "film", "republican", "tree", "source", "red", "nearly",
        "organization", "choose", "cause", "hair", "look", "point", "century", "evidence", "window", "difficult",
        "listen", "soon", "culture", "billion", "chance", "brother", "energy", "period", "course", "summer",
        "less", "realize", "hundred", "available", "plant", "likely", "opportunity", "term", "short", "letter",
        "condition", "choice", "place", "single", "rule", "daughter", "administration", "south", "husband", "congress",
        "floor", "campaign", "material", "population", "well", "call", "economy", "medical", "hospital", "church",
        "close", "thousand", "risk", "current", "fire", "future", "wrong", "involve", "defense", "anyone",
        "increase", "security", "bank", "myself", "certainly", "west", "sport", "board", "seek", "per",
        "subject", "officer", "private", "rest", "behavior", "deal", "performance", "fight", "throw", "top",
        "quickly", "past", "goal", "bed", "order", "author", "fill", "represent", "focus", "foreign",
        "drop", "plan", "blood", "upon", "agency", "push", "nature", "color", "store", "reduce",
        "sound", "note", "fine", "before", "near", "movement", "page", "enter", "share", "than",
        "common", "poor", "natural", "race", "concern", "series", "significant", "similar", "hot", "language",
        "each", "usually", "response", "dead", "rise", "animal", "factor", "decade", "article", "shoot",
        "east", "save", "seven", "artist", "away", "scene", "stock", "career", "despite", "central",
        "eight", "thus", "treatment", "beyond", "happy", "exactly", "protect", "approach", "lie", "size",
        "dog", "fund", "serious", "occur", "media", "ready", "sign", "thought", "list", "individual",
        "simple", "quality", "pressure", "accept", "answer", "resource", "identify", "left", "meeting", "determine",
        "prepare", "disease", "whatever", "success", "argue", "cup", "particularly", "amount", "ability", "staff",
        "recognize", "indicate", "character", "growth", "loss", "degree", "wonder", "attack", "herself", "region",
        "television", "box", "training", "pretty", "trade", "deal", "election", "everybody", "physical", "lay",
        "general", "feeling", "standard", "bill", "message", "fail", "outside", "arrive", "analysis", "benefit",
        "name", "sex", "forward", "lawyer", "present", "section", "environmental", "glass", "answer", "skill",
        "sister", "rules", "matter", "eat", "inside", "critical", "pattern", "weapon", "peace", "edge",
        "purpose", "strategy", "clearly", "discuss", "indeed", "force", "truth", "song", "example", "democratic",
        "check", "environment", "leg", "dark", "various", "rather", "laugh", "guess", "executive", "prove",
        "hang", "entire", "rock", "design", "enough", "forget", "since", "claim", "note", "remove",
        "manager", "enjoy", "network", "legal", "religious", "cold", "form", "final", "main", "science",
        "green", "memory", "card", "above", "seat", "cell", "establish", "nice", "trial", "expert",
        "that", "spring", "firm", "democrat", "radio", "visit", "management", "care", "avoid", "imagine",
        "tonight", "huge", "ball", "finish", "yourself", "theory", "impact", "respond", "statement", "maintain",
        "charge", "popular", "traditional", "onto", "reveal", "direction", "weapon", "employee", "cultural", "contain",
        "peace", "head", "control", "base", "pain", "apply", "play", "measure", "wide", "shake",
        "fly", "interview", "manage", "chair", "fish", "particular", "camera", "structure", "politics", "perform",
        "bit", "weight", "suddenly", "discover", "candidate", "top", "production", "treat", "trip", "evening",
        "affect", "inside", "conference", "unit", "best", "style", "adult", "worry", "range", "mention",
        "rather", "far", "deep", "front", "edge", "individual", "specific", "writer", "trouble", "necessary",
        "throughout", "challenge", "fear", "shoulder", "institution", "middle", "sea", "dream", "bar", "beautiful",
        "property", "instead", "improve", "stuff", "claim",
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
