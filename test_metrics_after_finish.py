#!/usr/bin/env python3
"""
Test script to verify that metrics are calculated correctly after finish_test() is called.
This addresses the issue where metrics would return 0 after the test is marked as finished.
"""

import time
from engine import TypingEngine


def test_metrics_after_finish():
    """Test that WPM and accuracy are calculated correctly after finish_test()."""
    print("Testing metrics calculation after finish_test()...")
    
    # Create engine with a simple test
    engine = TypingEngine("hello world test", 30)
    
    # Type some characters correctly
    engine.handle_keypress('h')  # Correct
    engine.handle_keypress('e')  # Correct
    engine.handle_keypress('l')  # Correct
    engine.handle_keypress('l')  # Correct
    engine.handle_keypress('o')  # Correct
    
    # Sleep a tiny bit to ensure some time passes
    time.sleep(0.1)
    
    # Type a space and more characters
    engine.handle_keypress(' ')  # Correct
    engine.handle_keypress('w')  # Correct
    engine.handle_keypress('o')  # Correct
    engine.handle_keypress('x')  # Incorrect (should be 'r')
    engine.handle_keypress('l')  # Correct
    
    # Check metrics before finishing
    wpm_before = engine.calculate_wpm()
    accuracy_before = engine.calculate_accuracy()
    
    print(f"\n  Before finish_test():")
    print(f"    WPM: {wpm_before:.2f}")
    print(f"    Accuracy: {accuracy_before:.2f}%")
    print(f"    Correct chars: {engine.correct_chars}")
    print(f"    Total chars typed: {engine.total_chars_typed}")
    print(f"    is_active: {engine.is_active}")
    
    assert wpm_before > 0, f"WPM before finish should be > 0, got {wpm_before}"
    assert accuracy_before > 0, f"Accuracy before finish should be > 0, got {accuracy_before}"
    
    # Now finish the test
    print("\n  Calling finish_test()...")
    engine.finish_test()
    
    # Check metrics after finishing
    wpm_after = engine.calculate_wpm()
    accuracy_after = engine.calculate_accuracy()
    
    print(f"\n  After finish_test():")
    print(f"    WPM: {wpm_after:.2f}")
    print(f"    Accuracy: {accuracy_after:.2f}%")
    print(f"    Correct chars: {engine.correct_chars}")
    print(f"    Total chars typed: {engine.total_chars_typed}")
    print(f"    is_active: {engine.is_active}")
    
    # These should NOT be 0 after finish_test()
    assert wpm_after > 0, f"WPM after finish should be > 0, got {wpm_after}"
    assert accuracy_after > 0, f"Accuracy after finish should be > 0, got {accuracy_after}"
    
    # Calculate expected accuracy (9 correct out of 10 = 90%)
    expected_accuracy = (9 / 10) * 100
    assert abs(accuracy_after - expected_accuracy) < 0.1, \
        f"Accuracy should be {expected_accuracy}%, got {accuracy_after}%"
    
    print("\n  ✓ Metrics calculated correctly after finish_test()")
    return True


def test_get_test_results():
    """Test that get_test_results() returns correct values after finish_test()."""
    print("\n\nTesting get_test_results() after finish_test()...")
    
    # Create engine
    engine = TypingEngine("test text", 30)
    
    # Type some characters
    for char in "test tex":
        engine.handle_keypress(char)
    
    time.sleep(0.05)
    
    # Finish the test
    print("\n  Calling finish_test()...")
    engine.finish_test()
    
    # Get test results
    print("\n  Getting test results...")
    results = engine.get_test_results()
    
    print(f"\n  Results:")
    print(f"    WPM: {results['wpm']}")
    print(f"    Accuracy: {results['accuracy']}")
    print(f"    Duration: {results['duration']}s")
    print(f"    Elapsed time: {results['elapsed_time']}s")
    print(f"    Correct chars: {results['correct_chars']}")
    print(f"    Total chars typed: {results['total_chars_typed']}")
    
    # Verify results contain non-zero values
    assert results['wpm'] > 0, f"WPM in results should be > 0, got {results['wpm']}"
    assert results['accuracy'] > 0, f"Accuracy in results should be > 0, got {results['accuracy']}"
    assert results['elapsed_time'] > 0, f"Elapsed time should be > 0, got {results['elapsed_time']}"
    assert results['correct_chars'] == 8, f"Should have 8 correct chars, got {results['correct_chars']}"
    assert results['total_chars_typed'] == 8, f"Should have 8 total chars, got {results['total_chars_typed']}"
    assert results['accuracy'] == 100.0, f"Accuracy should be 100%, got {results['accuracy']}"
    
    print("\n  ✓ get_test_results() returns correct values after finish_test()")
    return True


def test_elapsed_time_after_finish():
    """Test that elapsed time is calculated correctly after finish_test()."""
    print("\n\nTesting elapsed time calculation after finish_test()...")
    
    # Create engine
    engine = TypingEngine("test", 30)
    
    # Start typing
    engine.handle_keypress('t')
    
    # Sleep to accumulate some time
    time.sleep(0.2)
    
    # Get elapsed time before finishing
    elapsed_before = engine.get_elapsed_time()
    print(f"\n  Elapsed time before finish: {elapsed_before:.3f}s")
    
    # Finish the test
    engine.finish_test()
    
    # Get elapsed time after finishing
    elapsed_after = engine.get_elapsed_time()
    print(f"  Elapsed time after finish: {elapsed_after:.3f}s")
    
    # Elapsed time should be approximately the same (within a small margin)
    # and should not be 0
    assert elapsed_after > 0, f"Elapsed time after finish should be > 0, got {elapsed_after}"
    assert abs(elapsed_after - elapsed_before) < 0.05, \
        f"Elapsed time should be similar before and after finish, got {elapsed_before:.3f}s vs {elapsed_after:.3f}s"
    
    print(f"\n  ✓ Elapsed time calculated correctly after finish_test()")
    return True


def main():
    """Run all tests."""
    print("=" * 70)
    print("Testing Metrics Calculation After finish_test()")
    print("=" * 70)
    
    tests = [
        ("Metrics After Finish", test_metrics_after_finish),
        ("get_test_results() After Finish", test_get_test_results),
        ("Elapsed Time After Finish", test_elapsed_time_after_finish),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except AssertionError as e:
            print(f"\n  ✗ Test failed: {e}")
            results.append((name, False))
        except Exception as e:
            print(f"\n  ✗ Unexpected error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("Test Results:")
    print("=" * 70)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("All tests passed! Metrics are calculated correctly after finish_test().")
        return 0
    else:
        print("Some tests failed.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
