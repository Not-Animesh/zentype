#!/usr/bin/env python3
"""
ZenType Installation Test Script
Verifies all components are working correctly.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        from database import DatabaseManager
        from words import WordProvider
        from engine import TypingEngine
        print("  ✓ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False

def test_database():
    """Test database functionality."""
    print("\nTesting database...")
    try:
        from database import DatabaseManager
        
        db = DatabaseManager()
        
        # Add test result
        test_result = {
            "wpm": 50.0,
            "accuracy": 95.0,
            "duration": 30,
            "elapsed_time": 30.0,
            "correct_chars": 100,
            "total_chars_typed": 105,
            "total_chars_in_test": 150,
            "char_index": 100
        }
        db.add_result(test_result)
        
        # Get statistics
        stats = db.get_statistics()
        
        db.close()
        print("  ✓ Database operations successful")
        return True
    except Exception as e:
        print(f"  ✗ Database error: {e}")
        return False

def test_word_provider():
    """Test word provider."""
    print("\nTesting word provider...")
    try:
        from words import WordProvider
        
        wp = WordProvider()
        if len(wp.WORDS) < 500:
            print(f"  ✗ Word list too small: {len(wp.WORDS)} words")
            return False
        
        text = wp.generate_text(10)
        if len(text.split()) != 10:
            print(f"  ✗ Text generation failed")
            return False
        
        print(f"  ✓ Word provider working ({len(wp.WORDS)} words available)")
        return True
    except Exception as e:
        print(f"  ✗ Word provider error: {e}")
        return False

def test_typing_engine():
    """Test typing engine."""
    print("\nTesting typing engine...")
    try:
        from engine import TypingEngine
        
        engine = TypingEngine("test text", 30)
        
        # Test auto-start
        if engine.is_active:
            print("  ✗ Engine should not be active initially")
            return False
        
        engine.handle_keypress('t')
        if not engine.is_active:
            print("  ✗ Engine should be active after first keypress")
            return False
        
        # Test backspace
        engine.handle_keypress('e')
        engine.handle_keypress('s')
        engine.handle_keypress('t')
        engine.handle_keypress(' ')
        engine.handle_keypress('t')
        
        idx_before = engine.char_index
        engine.handle_backspace()
        if engine.char_index != idx_before - 1:
            print("  ✗ Backspace not working correctly")
            return False
        
        print("  ✓ Typing engine working correctly")
        return True
    except Exception as e:
        print(f"  ✗ Typing engine error: {e}")
        return False

def test_configuration():
    """Test configuration files."""
    print("\nTesting configuration...")
    
    if not os.path.exists('.env'):
        print("  ⚠ .env file not found (optional)")
    else:
        print("  ✓ .env file exists")
    
    if not os.path.exists('.gitignore'):
        print("  ⚠ .gitignore not found")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
        if '*.db' not in content:
            print("  ⚠ Database files not excluded from git")
            return False
    
    print("  ✓ Configuration files OK")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("ZenType Installation Test")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Database", test_database()))
    results.append(("Word Provider", test_word_provider()))
    results.append(("Typing Engine", test_typing_engine()))
    results.append(("Configuration", test_configuration()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("All tests passed! ZenType is ready to use.")
        print("\nRun 'python main.py' to start the application.")
        return 0
    else:
        print("Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
