#!/usr/bin/env python3
"""
Test script to verify key binding logic in ZenType.
Tests the TypingEngine functionality which underlies the key bindings.
"""

from engine import TypingEngine


def test_basic_typing():
    """Test basic character typing."""
    print("Testing basic typing...")
    engine = TypingEngine("hello world", 30)
    
    # Auto-start on first keypress
    assert not engine.is_active, "Engine should not be active initially"
    
    is_correct, idx = engine.handle_keypress('h')
    assert engine.is_active, "Engine should auto-start on first keypress"
    assert is_correct, "First character should be correct"
    assert idx == 1, "Index should be 1 after first character"
    
    # Type rest of "hello"
    engine.handle_keypress('e')
    engine.handle_keypress('l')
    engine.handle_keypress('l')
    engine.handle_keypress('o')
    
    assert engine.char_index == 5, f"Should be at index 5, got {engine.char_index}"
    assert engine.input_text == "hello", f"Input text should be 'hello', got '{engine.input_text}'"
    
    print("  ✓ Basic typing works correctly")
    return True


def test_incorrect_typing():
    """Test incorrect character handling."""
    print("\nTesting incorrect typing...")
    engine = TypingEngine("test", 30)
    
    # Type 't' correctly
    is_correct, _ = engine.handle_keypress('t')
    assert is_correct, "First character should be correct"
    
    # Type 'x' incorrectly (should be 'e')
    is_correct, _ = engine.handle_keypress('x')
    assert not is_correct, "Second character should be incorrect"
    assert engine.correct_chars == 1, f"Should have 1 correct char, got {engine.correct_chars}"
    assert engine.total_chars_typed == 2, f"Should have 2 total chars, got {engine.total_chars_typed}"
    
    print("  ✓ Incorrect typing tracked correctly")
    return True


def test_backspace_within_word():
    """Test backspace functionality within a word."""
    print("\nTesting backspace within word...")
    engine = TypingEngine("hello world", 30)
    
    # Type "hello"
    for char in "hello":
        engine.handle_keypress(char)
    
    # Type space to move to next word
    engine.handle_keypress(' ')
    
    # Type "wor"
    engine.handle_keypress('w')
    engine.handle_keypress('o')
    engine.handle_keypress('r')
    
    assert engine.char_index == 9, f"Should be at index 9, got {engine.char_index}"
    
    # Backspace should work within the word
    idx = engine.handle_backspace()
    assert idx == 8, f"After backspace, should be at index 8, got {idx}"
    assert engine.input_text == "hello wo", f"Input should be 'hello wo', got '{engine.input_text}'"
    
    # Another backspace
    idx = engine.handle_backspace()
    assert idx == 7, f"After second backspace, should be at index 7, got {idx}"
    
    print("  ✓ Backspace works within word")
    return True


def test_backspace_at_word_boundary():
    """Test that backspace stops at word boundaries."""
    print("\nTesting backspace at word boundary...")
    engine = TypingEngine("hello world", 30)
    
    # Type "hello "
    for char in "hello ":
        engine.handle_keypress(char)
    
    assert engine.char_index == 6, f"Should be at index 6, got {engine.char_index}"
    
    # Now we're at the start of "world"
    # Backspace should NOT go back past the space (word boundary)
    idx = engine.handle_backspace()
    assert idx == 6, f"Should stay at index 6 (word boundary), got {idx}"
    assert engine.input_text == "hello ", f"Input should still be 'hello ', got '{engine.input_text}'"
    
    print("  ✓ Backspace correctly stops at word boundary")
    return True


def test_wpm_calculation():
    """Test WPM calculation."""
    print("\nTesting WPM calculation...")
    engine = TypingEngine("hello world", 30)
    
    # Type 10 characters correctly
    for char in "hello worl":
        engine.handle_keypress(char)
    
    # WPM should be calculated
    wpm = engine.calculate_wpm()
    assert wpm >= 0, f"WPM should be >= 0, got {wpm}"
    
    print(f"  ✓ WPM calculation works (WPM: {wpm:.2f})")
    return True


def test_accuracy_calculation():
    """Test accuracy calculation."""
    print("\nTesting accuracy calculation...")
    engine = TypingEngine("test", 30)
    
    # Type 3 correct, 1 incorrect
    engine.handle_keypress('t')  # Correct
    engine.handle_keypress('e')  # Correct
    engine.handle_keypress('x')  # Incorrect (should be 's')
    engine.handle_keypress('t')  # Correct
    
    accuracy = engine.calculate_accuracy()
    expected = (3 / 4) * 100  # 75%
    assert abs(accuracy - expected) < 0.1, f"Accuracy should be {expected}%, got {accuracy}%"
    
    print(f"  ✓ Accuracy calculation works (Accuracy: {accuracy:.1f}%)")
    return True


def test_completion_detection():
    """Test completion detection."""
    print("\nTesting completion detection...")
    engine = TypingEngine("hi", 30)
    
    assert not engine.is_completed(), "Should not be completed initially"
    
    engine.handle_keypress('h')
    assert not engine.is_completed(), "Should not be completed after 1 char"
    
    engine.handle_keypress('i')
    assert engine.is_completed(), "Should be completed after all chars typed"
    
    print("  ✓ Completion detection works")
    return True


def main():
    """Run all key binding tests."""
    print("=" * 60)
    print("ZenType Key Binding Logic Test")
    print("=" * 60)
    
    tests = [
        ("Basic Typing", test_basic_typing),
        ("Incorrect Typing", test_incorrect_typing),
        ("Backspace Within Word", test_backspace_within_word),
        ("Backspace at Boundary", test_backspace_at_word_boundary),
        ("WPM Calculation", test_wpm_calculation),
        ("Accuracy Calculation", test_accuracy_calculation),
        ("Completion Detection", test_completion_detection),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            results.append((name, False))
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
            results.append((name, False))
    
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
        print("All tests passed! Key binding logic is working correctly.")
        return 0
    else:
        print("Some tests failed.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
