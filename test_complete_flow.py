#!/usr/bin/env python3
"""
Simulation script to test the complete flow from typing to results display.
This mimics what happens when a user completes a typing test.
"""

import time
import logging
from engine import TypingEngine

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s %(name)s] %(message)s')


def simulate_typing_test():
    """Simulate a complete typing test session."""
    print("=" * 70)
    print("Simulating Complete Typing Test Session")
    print("=" * 70)
    
    # Initialize engine (same as what main.py does)
    target_text = "hello world this is a typing test"
    duration = 30
    
    print(f"\nTest Setup:")
    print(f"  Target text: '{target_text}'")
    print(f"  Duration: {duration}s")
    
    engine = TypingEngine(target_text, duration)
    
    # Simulate user typing (with some errors)
    print("\nSimulating user typing...")
    typing_sequence = [
        ('h', True),   # Correct
        ('e', True),   # Correct
        ('l', True),   # Correct
        ('l', True),   # Correct
        ('o', True),   # Correct
        (' ', True),   # Correct
        ('w', True),   # Correct
        ('o', True),   # Correct
        ('r', True),   # Correct
        ('l', True),   # Correct
        ('x', False),  # Incorrect (should be 'd')
        (' ', True),   # Correct
        ('t', True),   # Correct
        ('h', True),   # Correct
        ('i', True),   # Correct
        ('s', True),   # Correct
    ]
    
    for char, expected_correct in typing_sequence:
        is_correct, idx = engine.handle_keypress(char)
        if is_correct != expected_correct:
            print(f"  WARNING: Expected {expected_correct} for '{char}', got {is_correct}")
    
    print(f"  Typed: '{engine.input_text}'")
    print(f"  Progress: {engine.char_index}/{len(target_text)} characters")
    
    # Wait a bit to simulate time passing
    time.sleep(0.15)
    
    # Get metrics before finishing (what update_stats_loop does)
    print("\nMetrics during typing (from update_stats_loop):")
    wpm_during = engine.calculate_wpm()
    accuracy_during = engine.calculate_accuracy()
    print(f"  WPM: {wpm_during:.2f}")
    print(f"  Accuracy: {accuracy_during:.2f}%")
    
    # Simulate test completion (what happens when time runs out or user finishes)
    print("\n" + "=" * 70)
    print("Simulating finish_test() call from TypingScreen")
    print("=" * 70)
    
    # This mimics what TypingScreen.finish_test() does:
    print("\n[TypingScreen.finish_test] Step 1: Call engine.finish_test()")
    engine.finish_test()
    
    print("\n[TypingScreen.finish_test] Step 2: Get test results")
    results = engine.get_test_results()
    
    print("\n[TypingScreen.finish_test] Step 3: Results to pass to on_test_complete():")
    for key, value in results.items():
        print(f"    {key}: {value}")
    
    # Simulate ResultsScreen.display_results()
    print("\n" + "=" * 70)
    print("Simulating ResultsScreen.display_results()")
    print("=" * 70)
    
    wpm = results["wpm"]
    accuracy = results["accuracy"]
    
    print(f"\n[ResultsScreen.display_results] Displaying:")
    print(f"    WPM Display: {int(wpm)} WPM")
    print(f"    Accuracy Display: {accuracy:.1f}%")
    
    # Verify results are valid
    print("\n" + "=" * 70)
    print("Verification")
    print("=" * 70)
    
    success = True
    
    if wpm <= 0:
        print(f"  ✗ FAIL: WPM is {wpm}, should be > 0")
        success = False
    else:
        print(f"  ✓ PASS: WPM is {wpm:.2f} (> 0)")
    
    if accuracy <= 0:
        print(f"  ✗ FAIL: Accuracy is {accuracy}, should be > 0")
        success = False
    else:
        print(f"  ✓ PASS: Accuracy is {accuracy:.2f}% (> 0)")
    
    if results["elapsed_time"] <= 0:
        print(f"  ✗ FAIL: Elapsed time is {results['elapsed_time']}, should be > 0")
        success = False
    else:
        print(f"  ✓ PASS: Elapsed time is {results['elapsed_time']:.2f}s (> 0)")
    
    # Expected accuracy: 15 correct out of 16 = 93.75%
    expected_accuracy = (15 / 16) * 100
    if abs(accuracy - expected_accuracy) > 0.1:
        print(f"  ✗ FAIL: Accuracy should be {expected_accuracy:.2f}%, got {accuracy:.2f}%")
        success = False
    else:
        print(f"  ✓ PASS: Accuracy is correct ({expected_accuracy:.2f}%)")
    
    print("\n" + "=" * 70)
    if success:
        print("SUCCESS: All metrics are calculated and displayed correctly!")
    else:
        print("FAILURE: Some metrics are incorrect!")
    print("=" * 70)
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(simulate_typing_test())
