# ZenType - User Guide

Complete guide to using ZenType typing speed tester.

## Getting Started

### Installation

1. Ensure Python 3.8+ is installed on your system
2. Download or clone the ZenType project
3. Open terminal/command prompt in the project directory
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

In the project directory, run:
```bash
python main.py
```

The ZenType window will open, ready to use.

---

## Main Typing Screen

### Layout Overview

```
         ZenType
     [Minimalist Header]

    30s  60s  90s
  [Duration Selector]

   #### WPM  ##.#% Accuracy
  [Real-Time Statistics]

  ╔════════════════════════════════════╗
  ║ type text appears here as you type ║
  ║ characters turn gold when correct  ║
  ║ characters turn red when wrong     ║
  ╚════════════════════════════════════╝

[Reset (Tab)]  [History]
```

### Step-by-Step: Taking a Typing Test

#### 1. Select Test Duration

Click one of the duration buttons:
- **30s** - Quick test (good for warm-up)
- **60s** - Standard test (recommended)
- **90s** - Extended test (challenging)

The selected duration button will turn gold.

#### 2. Focus the Typing Area

Click anywhere in the text display box to focus it. You'll see the cursor ready in the text field.

#### 3. Start Typing

Begin typing the displayed text. Your typing will:
- Auto-start the 60-second timer on your first keystroke
- Display in real-time with color feedback:
  - **Gold/Tan**: Correct character ✓
  - **Red**: Wrong character ✗
  - **Gray**: Not yet typed

#### 4. Watch Your Stats

Real-time statistics update every 500 milliseconds:
- **WPM**: Words per minute (large gold number on left)
- **Accuracy**: Percentage of correct keystrokes (large gold number on right)

#### 5. Complete the Test

The test automatically ends when:
- Time limit expires (30/60/90 seconds), OR
- You type all characters (if faster than time limit)

A results screen will appear automatically.

---

## During Typing: Keyboard Controls

### Regular Keys

Simply type the displayed text. Each character appears in the text box:
- **Correct match**: Turns light tan/gold color
- **Wrong character**: Turns red color

### Backspace

**Correct the current word only** by pressing backspace:
- You can backspace to the beginning of the **current word**
- You **cannot** backspace to the previous word
- This prevents "cheating" by fixing entire sentences

**Example:**
```
Target text: "the quick brown fox"
You typed:   "the quikc"

Cursor is here: ↓
                "the quikc"

Press backspace 2 times:
- First backspace: "the quik" (can go back)
- Second backspace: "the qui" (still in word)
- At word boundary: Cannot backspace further
```

### Tab Key

Press **Tab** to instantly **reset the current test**:
- Clears all typed input
- Resets timer to 0
- Clears statistics
- Keeps same duration and text

Perfect for warm-ups or false starts.

### Window Focus

If you click another window or lose focus:
- Typing test **pauses**
- "Click to Focus" message appears on screen
- Click back in the text area to **resume**

---

## Results Screen

After test completion, you'll see:

### Final Statistics

```
         Test Complete!

   ### WPM        ##.#% Accuracy
```

Large gold numbers showing:
- Your final words-per-minute score
- Your accuracy percentage

### Performance Chart

A line graph showing your typing speed over time:
- **X-axis**: Time elapsed (0 to duration in seconds)
- **Y-axis**: WPM at that moment
- **Gold line**: Your speed progression
- **Yellow dots**: Data points (1-second intervals)

This visualizes:
- If you started slow and improved
- If you maintained consistent speed
- If you fatigued toward the end

### Action Buttons

#### Retry (Same Duration)
```
[Retry (Same Duration)]
```
Start a new test immediately with the same duration (30/60/90s).
- Timer resets
- New random text generated
- Statistics cleared

#### Change Duration
```
[Change Duration]
```
Go back to duration selection screen to:
- Choose different test length
- Start a new test with new duration

#### View History
```
[View History]
```
Jump to the history screen to see:
- All past test results
- Personal statistics
- Performance trends

---

## History and Statistics Screen

Access by clicking **History** button from any screen.

### Overall Statistics Summary

Displays aggregate data from all your tests:

```
Total Tests: 27
Best WPM: 92
Average WPM: 78.5
Average Accuracy: 96.8%
```

**Metrics Explained:**
- **Total Tests**: How many typing tests you've completed
- **Best WPM**: Your highest WPM score across all tests
- **Average WPM**: Mean WPM across all tests
- **Average Accuracy**: Mean accuracy across all tests

### Recent Tests List

Scrollable table showing your last 10 typing tests:

```
92 WPM | 98.2% | 60s | 2024-01-09
89 WPM | 97.5% | 60s | 2024-01-09
85 WPM | 96.1% | 30s | 2024-01-08
...
```

Each row shows:
- **WPM Score**: Speed for that test
- **Accuracy**: Percentage correct keystrokes
- **Duration**: Test length (30/60/90s)
- **Date**: When test was taken (YYYY-MM-DD format)

The list shows most recent tests first (newest at top).

### Navigation

**Back to Typing** button returns to typing screen to take new tests.

---

## Understanding Your Statistics

### WPM (Words Per Minute)

**What it measures**: How fast you type

**Formula**: `(Correct Characters ÷ 5) ÷ Time in Minutes`

**Why 5 chars?** Industry standard - average English word is ~5 characters

**Examples**:
- 40 WPM = Very beginner
- 60 WPM = Average typist
- 80 WPM = Good typist
- 100+ WPM = Advanced typist
- 150+ WPM = Professional level

**Improving WPM**:
- Practice regularly (30 minutes daily)
- Memorize key positions
- Focus on accuracy first, speed follows
- Avoid looking at keyboard

### Accuracy

**What it measures**: How many keystrokes were correct

**Formula**: `(Correct Keystrokes ÷ Total Keystrokes) × 100%`

**Interpretation**:
- 90% = Good (but room to improve)
- 95% = Very good
- 98%+ = Excellent
- 100% = Perfect (rare!)

**Why accuracy matters**:
- Speed without accuracy is useless
- Backspacing wastes time
- Build muscle memory through accuracy
- Professional work demands high accuracy

**Improving Accuracy**:
- Slow down - prioritize accuracy over speed
- Focus on proper finger positioning
- Practice problem keys repeatedly
- Take breaks to avoid fatigue

---

## Tips for Better Typing Performance

### Before You Start

1. **Posture**: Sit with back straight, feet flat
2. **Hand Position**: Wrists aligned with keyboard, fingers curved
3. **Lighting**: Adequate light on keyboard and text
4. **Comfort**: Remove distractions, silence notifications

### During Test

1. **Focus**: Don't glance at keyboard - trust your fingers
2. **Accuracy First**: Speed comes naturally with accuracy
3. **Rhythm**: Develop a steady, consistent typing pace
4. **Breathing**: Relax, don't hold your breath

### Between Tests

1. **Breaks**: Take 5 minutes after 20-minute sessions
2. **Stretching**: Stretch wrists and fingers between tests
3. **Hydration**: Drink water, stay hydrated
4. **Review**: Check history to identify problem keys

### Progressive Training

- **Week 1-2**: Focus on accuracy over speed
- **Week 3-4**: Increase speed gradually while maintaining accuracy
- **Week 5+**: Target specific weak keys with custom drills

---

## Data and Privacy

### Where Data is Stored

All your typing test results are saved locally:
```
~/.zentype/data/typing_results.json
```

This is in your home directory in a hidden `.zentype` folder.

### What Data is Saved

Each test record contains:
- Timestamp (when you took the test)
- WPM score
- Accuracy percentage
- Test duration (30/60/90s)
- Character counts
- Other metrics

### Privacy

- **100% Local**: All data stored on your computer
- **No Cloud**: Never sent to internet or external servers
- **Your Data**: You have complete control
- **Exportable**: Can backup or export results manually

### Accessing Raw Data

You can view your raw test data:

1. Open file explorer/finder
2. Navigate to home directory
3. Look for hidden folder: `.zentype`
4. Open `data` folder
5. Open `typing_results.json` in text editor

Format is standard JSON with one test per line.

---

## Troubleshooting

### Q: Font looks weird or different from screenshots

**A**: ZenType automatically falls back to system fonts:
1. JetBrains Mono (primary)
2. Roboto Mono (fallback)
3. Consolas (system default)

All are monospaced fonts and work equally well.

### Q: Text won't appear in the typing area

**A**:
- Click in the text box to focus it
- Ensure tkinter is properly installed
- Try restarting the application

### Q: Statistics aren't updating

**A**:
- Check that the text box is focused
- Ensure you've started typing (timer starts on first keypress)
- Wait for 500ms update cycle

### Q: History is empty or won't save

**A**:
- Ensure `~/.zentype/data/` directory exists
- Check file permissions (should be readable/writable)
- Try taking a fresh test and checking results immediately

### Q: Application crashes on startup

**A**:
- Verify Python 3.8+ installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Check system has tkinter: `python -m tkinter`

### Q: Can't backspace across words

**A**: This is by design! You can only correct the current word:
- Word boundary is last space character
- Prevents entire-sentence corrections
- Encourages accuracy focus

---

## Keyboard Shortcuts Reference

| Action | Key | Effect |
|--------|-----|--------|
| Type character | Any key | Appears in text, auto-starts timer |
| Fix current word | Backspace | Delete last character (within word) |
| Reset test | Tab | Clear all input, restart timer |
| Regain focus | Click text | Resume paused test |
| Exit focus | Click outside | Pause test, show overlay |

---

## Common Performance Benchmarks

These are typical scores for reference:

| Skill Level | WPM | Accuracy |
|-------------|-----|----------|
| Absolute beginner | 20-40 | 85-90% |
| Beginning typist | 40-60 | 90-94% |
| Intermediate | 60-80 | 94-97% |
| Advanced | 80-100 | 97-99% |
| Professional | 100+ | 99%+ |

Your goal should be **sustainable improvement** over time, not rapid gains.

---

## Next Steps

1. **Take your first test**: Start with 30 seconds to get comfortable
2. **Review results**: Check what keys trip you up
3. **Practice regularly**: 15-30 minutes daily is ideal
4. **Track progress**: Use History screen to monitor improvement
5. **Set goals**: Aim for 5 WPM improvement every week

---

## Getting Help

If you encounter issues not covered here:

1. Check SYSTEM_ARCHITECTURE.md for technical details
2. Review README.md for installation help
3. Examine your test data in `~/.zentype/data/typing_results.json`
4. Try restarting the application

---

Happy typing! 🎯

Remember: **Accuracy over speed, consistency over bursts, practice over perfection.**
