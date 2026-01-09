# ZenType - System Architecture Documentation

Comprehensive technical breakdown of ZenType's architecture, suitable for academic presentation and technical viva.

## 1. Project Overview

ZenType is a pure Python typing speed tester built with:
- **UI Framework**: customtkinter + tkinter
- **Data Storage**: Local JSON files
- **Architecture**: Modular design with clear separation of concerns

```
┌─────────────────┐
│   main.py       │  UI Layer (5 screens)
├─────────────────┤
│   engine.py     │  Logic Layer (typing validation, stats)
├─────────────────┤
│   words.py      │  Content Layer (word generation)
├─────────────────┤
│ data_manager.py │  Persistence Layer (JSON storage)
└─────────────────┘
```

---

## 2. Logic Layer: Core Typing Engine

### 2.1 TypingEngine Class (engine.py)

The heart of ZenType's functionality. Handles all typing validation, statistics calculation, and test state management.

#### Character Validation System

**Problem**: How to validate character-by-character input while the user types?

**Solution**: Character-level state tracking with index-based comparison

```python
def handle_keypress(self, char: str) -> Tuple[bool, int]:
    """
    Compare each character against target text at current position.
    Returns (is_correct, updated_char_index)
    """
    target_char = self.target_text[self.char_index]
    is_correct = char == target_char
    self.char_index += 1  # Move cursor forward
    return is_correct, self.char_index
```

**Key Features**:
- Maintains `char_index`: Current position in target text
- Maintains `input_text`: All characters typed so far
- Tracks `correct_chars`: Count of correctly typed characters
- Stores keystroke history: `(char, is_correct, timestamp)` tuples

#### WPM Calculation (Words Per Minute)

**Formula**: `(Correct Characters ÷ 5) ÷ (Time in Minutes)`

```python
def calculate_wpm(self) -> float:
    elapsed_minutes = self.get_elapsed_time() / 60.0
    words = self.correct_chars / 5.0  # 5 chars = 1 word (standard)
    return words / elapsed_minutes
```

**Why 5 characters per word?**
- Industry standard assumption
- Accounts for spaces and variable word lengths
- Normalizes WPM across different texts

**Update Frequency**: Every 500ms for smooth real-time feedback

#### Accuracy Calculation

**Formula**: `(Correct Keystrokes ÷ Total Keystrokes) × 100`

```python
def calculate_accuracy(self) -> float:
    if self.total_chars_typed == 0:
        return 0.0
    return (self.correct_chars / self.total_chars_typed) * 100.0
```

**Counts**:
- `correct_chars`: Only characters that match target exactly
- `total_chars_typed`: All keystrokes including backspace
- Includes both correct and incorrect characters

#### Backspace Logic with Word Boundary Restriction

**Requirement**: Users can only backspace within the current word, not across word boundaries.

```python
def handle_backspace(self) -> int:
    """Only allow backspace if not crossing word boundary."""
    current_word_start = self.calculate_current_word_start()

    if self.char_index > current_word_start:
        self.char_index -= 1  # Safe to backspace
    # else: At word boundary, ignore backspace
```

**Current Word Detection**:
1. Search backwards from current position
2. Find the last space character
3. Word starts at position after that space
4. Backspace only allowed within that word

**Example**:
```
Target: "the quick brown fox"
         ^       ^
         0       4 (word starts at index 4)

If user is at index 9 (mid-word "quick"):
- Can backspace to index 4 (word start)
- Cannot backspace beyond index 4 (that's the word boundary)
```

#### Timer and Test Completion

**Auto-start Mechanism**:
```python
def handle_keypress(self, char: str):
    if not self.is_active:
        self.start_timer()  # First keypress triggers timer
```

**Test Completion Detection**:
```python
def is_completed(self) -> bool:
    return self.is_time_exceeded() or self.char_index >= len(self.target_text)
```

Completes when either:
1. Time limit exceeded (30s, 60s, or 90s)
2. User types entire text (before time runs out)

#### WPM History for Charting

```python
def get_wpm_history(self, interval: float = 1.0) -> List[float]:
    """Generate WPM datapoints at 1-second intervals for visualization."""
    wpm_history = []
    for t in range(int(elapsed_time)):
        correct_at_t = count_correct_chars_up_to(t)
        wpm = (correct_at_t / 5) / (t / 60)
        wpm_history.append(wpm)
    return wpm_history
```

---

### 2.2 WordProvider Class (words.py)

Generates random text blocks for typing tests.

#### Word List Management

Contains 200+ curated common English words:
```python
WORDS = ["the", "be", "to", "of", "and", "a", ...]
```

**Why curated?**
- Common, recognizable words reduce cognitive load
- Balanced word length distribution
- Mix of easy and slightly challenging words

#### Dynamic Text Generation

```python
def generate_text(word_count: int) -> str:
    selected_words = random.choices(WORDS, k=word_count)
    return " ".join(selected_words)
```

Uses `random.choices()` to allow word repetition (no finite word limit).

#### Word Count Calculation

Dynamically determines how many words to show based on test duration:

```python
def get_word_count_for_duration(duration_seconds: int) -> int:
    words_per_second = 0.6  # ~40 WPM average
    return int(duration_seconds * words_per_second)
```

**For 30 seconds**: ~18 words
**For 60 seconds**: ~36 words
**For 90 seconds**: ~54 words

---

### 2.3 DataManager Class (data_manager.py)

Handles persistent local storage without external databases.

#### Local File Storage Structure

```
~/.zentype/data/
└── typing_results.json
    [
        {
            "timestamp": "2024-01-09T14:30:45.123456",
            "wpm": 75.5,
            "accuracy": 98.2,
            "duration": 60,
            "correct_chars": 450,
            "total_chars_typed": 459,
            "char_index": 456
        },
        ...
    ]
```

#### Key Operations

1. **Save Results**: Append new test to results.json
2. **Load Results**: Parse JSON array from file
3. **Calculate Statistics**: Aggregate data across all tests
4. **Filter by Duration**: Get results for specific test length
5. **Recent Results**: Sort by timestamp for history view

---

## 3. UI Layer: Visual Architecture

### 3.1 Typing Screen (`TypingScreen` class)

Main interactive screen where users type.

#### TypingDisplay: Character-Level Text Widget

```python
class TypingDisplay(ctk.CTkFrame):
    """Custom frame using tkinter.Text for character-level control."""
```

**Why tkinter.Text instead of CTkEntry?**
- CTkEntry: Single-line, treats input as whole string
- tkinter.Text: Multi-line, supports character-level tags and formatting
- Tags: Apply different colors to individual characters dynamically

#### Text Tags System

Three color states defined as tkinter tags:

```python
self.text_widget.tag_config("unwritten", foreground="#646669")   # Gray
self.text_widget.tag_config("correct", foreground="#D1D0C5")     # Tan
self.text_widget.tag_config("error", foreground="#CA4754")       # Red
```

#### Character Coloring Algorithm

On each keystroke, update character colors:

```python
def update_colors(self, target_text, input_text, char_index):
    """Apply tags based on character status."""
    for i in range(len(target_text)):
        pos_start = f"1.0+{i}c"  # Position: line 1, character i
        pos_end = f"1.0+{i+1}c"

        if i >= char_index:
            tag = "unwritten"  # Not yet typed
        elif target_text[i] == input_text[i]:
            tag = "correct"
        else:
            tag = "error"

        self.text_widget.tag_add(tag, pos_start, pos_end)
```

**Performance**: Removes old tags, applies new ones every 500ms

#### Real-Time Statistics Panel

```python
class StatisticsPanel:
    """Displays WPM and Accuracy in large, easy-to-read format."""

    def update_stats(self, wpm: float, accuracy: float):
        self.wpm_label.configure(text=f"{int(wpm)}")
        self.accuracy_label.configure(text=f"{accuracy:.1f}%")
```

Updates triggered by 500ms loop:
```python
def update_stats_loop(self):
    if self.engine.is_active and not self.engine.is_completed():
        wpm = self.engine.calculate_wpm()
        accuracy = self.engine.calculate_accuracy()
        self.stats_panel.update_stats(wpm, accuracy)
        self.after(500, self.update_stats_loop)
```

#### Focus Management

Window blur overlay:
```python
def on_focus_out(self, event):
    """Show overlay when window loses focus."""
    if self.engine.is_active:
        self.focus_overlay.place(relx=0.5, rely=0.5, anchor="center")

def on_focus_in(self, event):
    """Hide overlay when window regains focus."""
    self.focus_overlay.place_forget()
```

---

### 3.2 Results Screen (`ResultsScreen` class)

Displays final statistics and performance chart.

#### Canvas-Based Chart Rendering

```python
def draw_chart(self, engine):
    """Draw speed-over-time chart using pure tkinter Canvas."""
    wpm_history = engine.get_wpm_history(interval=1.0)

    # Data range mapping
    max_wpm = max(wpm_history)
    max_time = len(wpm_history)

    # Draw axes and grid
    # Convert data coordinates to pixel coordinates
    # Plot line connecting data points
```

**Key Calculations**:
- **Pixel to Data Mapping**: Scale data values to canvas dimensions
- **Y-axis**: WPM values (0 to max observed)
- **X-axis**: Time in seconds (0 to test duration)
- **Grid Lines**: Every 1 second on X-axis

---

### 3.3 History Screen (`HistoryScreen` class)

Displays personal statistics and recent test results.

#### Statistics Aggregation

```python
def display_statistics(self):
    stats = self.data_manager.get_statistics()

    # Displays:
    # - Total tests completed
    # - Personal best WPM
    # - Average WPM across all tests
    # - Average accuracy
```

#### Scrollable Results List

Recent tests shown in reverse chronological order:
```
75 WPM | 98.2% | 60s | 2024-01-09
72 WPM | 97.1% | 60s | 2024-01-08
...
```

---

## 4. Event Handling System

### 4.1 Keyboard Event Binding

```python
self.master.bind("<Key>", self.on_key)        # All keys
self.master.bind("<BackSpace>", self.on_backspace)  # Special handling
self.master.bind("<Tab>", lambda e: self.reset_test())  # Reset
self.master.bind("<FocusIn>", self.on_focus_in)  # Window focus
self.master.bind("<FocusOut>", self.on_focus_out)  # Window blur
```

### 4.2 Keypress Event Flow

```
Key Press Event
    ↓
on_key() handler
    ↓
Check if time exceeded → If yes, finish_test()
    ↓
Extract character from event
    ↓
engine.handle_keypress(char)
    ↓
Compare with target text
    ↓
Update char_index, input_text, correct_chars
    ↓
Return (is_correct, new_index)
    ↓
update_display()
    ↓
update_colors() with new char_index
    ↓
Text widget re-renders with updated colors
```

### 4.3 Backspace Event Flow

```
Backspace Key Press
    ↓
on_backspace() handler
    ↓
Calculate current_word_start
    ↓
Check if char_index > current_word_start
    ↓
If yes: Decrement char_index, remove from input_text
    ↓
If no: Ignore (word boundary)
    ↓
update_display()
```

### 4.4 Update Loop (500ms)

```python
def update_stats_loop(self):
    """Continuous update cycle for real-time feedback."""
    if self.engine.is_active and not self.engine.is_completed():
        # Calculate fresh statistics
        wpm = self.engine.calculate_wpm()
        accuracy = self.engine.calculate_accuracy()

        # Update UI
        self.stats_panel.update_stats(wpm, accuracy)

        # Schedule next update
        self.after(500, self.update_stats_loop)
```

---

## 5. Data Flow Diagram

```
User Types Character
    ↓
<Key> event → on_key()
    ↓
engine.handle_keypress()
    ↓
Compare char with target_text[char_index]
    ↓
Update: correct_chars, total_chars, char_index
    ↓
update_display()
    ↓
update_colors() → Apply text tags
    ↓
update_stats_loop() [Every 500ms]
    ↓
engine.calculate_wpm(), calculate_accuracy()
    ↓
stats_panel.update_stats()
    ↓
User sees live feedback
```

---

## 6. Performance Considerations

### 6.1 Character-Level Processing

- **Efficiency**: Single character comparison per keystroke
- **Memory**: Input text stored in string (minimal overhead)
- **Rendering**: Only tags updated, not entire widget

### 6.2 Update Frequency

- **500ms Loop**: Balances responsiveness with CPU usage
- **No Busy-Waiting**: Uses tkinter's `.after()` for non-blocking updates

### 6.3 Data Persistence

- **JSON Format**: Human-readable, standard Python support
- **Append-Only**: New results added to existing array
- **File I/O**: Minimal overhead, only on test completion

---

## 7. Color and Typography System

### 7.1 Color Palette

| Element | Color | Hex | Purpose |
|---------|-------|-----|---------|
| Background | Dark Charcoal | #2C2E31 | Low eye strain |
| Unwritten Text | Gray | #646669 | Indicates upcoming text |
| Correct Text | Light Tan | #D1D0C5 | Visual confirmation |
| Error Text | Red | #CA4754 | Immediate feedback |
| Accent/UI | Gold | #E2B714 | Interactive elements |

### 7.2 Font Selection

```python
font=("JetBrains Mono", 18)  # Primary monospace font
```

**Fallback Chain**:
1. JetBrains Mono (preferred)
2. Roboto Mono
3. Consolas (Windows default)

---

## 8. Design Patterns Used

### 8.1 Model-View-Controller (MVC)

- **Model**: `TypingEngine`, `DataManager` (logic & data)
- **View**: `TypingScreen`, `ResultsScreen`, `HistoryScreen` (UI components)
- **Controller**: Main application class `ZenTypeApp` (orchestration)

### 8.2 Observer Pattern

- Statistics update loop observes engine state
- UI updates when engine calculates new values

### 8.3 State Machine

Test states:
- IDLE → ACTIVE (first keypress) → COMPLETED (time/text finished)

---

## 9. Technical Limitations & Future Improvements

### Current Limitations

1. **Font Availability**: Relies on system fonts, may not have JetBrains Mono
2. **Single Window**: No multi-window support
3. **No Theme Switching**: Dark mode only
4. **No Difficulty Levels**: Uses uniform word list

### Potential Enhancements

1. **Custom Word Lists**: User-selectable difficulty
2. **Sound Effects**: Audio feedback for errors/milestones
3. **Advanced Charts**: More detailed performance visualization
4. **Multiplayer**: Network-based competitive typing
5. **Mobile Version**: Port to mobile platforms

---

## Conclusion

ZenType demonstrates a clean modular architecture separating logic, UI, and persistence layers. The character-level typing validation using tkinter.Text tags provides precise feedback, while the 500ms update loop balances responsiveness with performance. Local JSON storage ensures privacy and offline functionality without sacrificing data persistence.

The design prioritizes user experience through real-time statistics, clear visual feedback, and a focused minimalist interface inspired by professional typing applications.
