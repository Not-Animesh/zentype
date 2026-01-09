# ZenType - Minimalist Desktop Typing Speed Tester

A pure Python typing speed tester inspired by Monkeytype with a dark minimalist terminal aesthetic. Track your typing speed, accuracy, and progress with local data persistence.

## Features

- **Real-Time Statistics**: Live WPM (Words Per Minute) and accuracy tracking
- **Character-Level Feedback**: Visual indication of correct/incorrect characters as you type
- **Multiple Test Durations**: Choose between 30, 60, or 90-second tests
- **Smart Backspace**: Backspace only works within the current word (no cross-word corrections)
- **Performance Charting**: Speed-over-time visualization using canvas-based charting
- **Complete History**: All test results saved locally with comprehensive statistics
- **Local Data Storage**: 100% local persistence - no external database or cloud required
- **Dark Minimalist UI**: Terminal-inspired aesthetic with focus on typing experience

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

This installs:
- **customtkinter** - Modern UI framework
- **pillow** - Image processing (for UI assets)

## Running ZenType

Start the application:
```bash
python main.py
```

The application window will open and you're ready to start typing tests.

## How to Use

1. **Select Duration**: Click 30s, 60s, or 90s button to choose test length
2. **Focus the Text Area**: Click on the text display area
3. **Start Typing**: Begin typing when ready - timer auto-starts on first keypress
4. **Review Results**: After time expires, see your final WPM and accuracy
5. **View History**: Click "History" button to see all past test results and statistics

## Keyboard Shortcuts

- **Tab** - Reset current test and start over
- **Backspace** - Correct mistakes (only within current word)
- **Esc** - Exit application

## Data Storage

All typing test results are stored locally in:
```
~/.zentype/data/typing_results.json
```

This JSON file contains all test metrics and timestamps. No internet connection required.

## File Structure

```
ZenType/
├── main.py              # Main application and UI components
├── engine.py            # Typing logic, WPM/accuracy calculations
├── words.py             # Word list and text generation
├── data_manager.py      # Local JSON data persistence
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── SYSTEM_ARCHITECTURE.md  # Technical documentation
└── USER_GUIDE.md       # Detailed usage guide
```

## Color Scheme

- **Background**: `#2C2E31` - Dark charcoal
- **Unwritten Text**: `#646669` - Gray
- **Correct Text**: `#D1D0C5` - Light tan
- **Error Text**: `#CA4754` - Red
- **Accent/UI**: `#E2B714` - Gold

## Typography

Uses monospaced fonts (in priority order):
1. JetBrains Mono (primary)
2. Roboto Mono (fallback)
3. Consolas (system fallback)

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Run `pip install -r requirements.txt` to install dependencies
- Check that customtkinter is properly installed

### No font is rendering
- JetBrains Mono is preferred but not required
- Application falls back to system monospaced fonts automatically

### Data not saving
- Ensure `~/.zentype/data/` directory exists and is writable
- Check file permissions on `typing_results.json`

## Performance Tips

- Use a keyboard without input lag for best results
- Ensure typing display area is clearly visible
- Test durations from 30-90 seconds recommended for balanced difficulty

## Future Enhancements

- Theme customization options
- Sound effects for typing feedback
- Leaderboard integration
- Advanced statistics (percentile rankings, difficulty levels)
- Export to CSV functionality

## License

This is an educational project created for learning purposes.

---

Built with Python, customtkinter, and tkinter for pure desktop performance.
