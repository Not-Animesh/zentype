"""
ZenType - Minimalist Desktop Typing Speed Tester
Main application file with UI and event handling.
Uses customtkinter for modern UI and tkinter.Text for character-level typing control.
"""

import customtkinter as ctk
from tkinter import Canvas
import tkinter as tk
from words import WordProvider
from engine import TypingEngine
from database import DatabaseManager
from datetime import datetime
import math


class TypingDisplay(ctk.CTkFrame):
    """
    Custom frame for displaying typing text with character-level color control.
    Uses tkinter.Text widget with tags for precise visual feedback.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color="#2C2E31")

        # Configure text widget with monospaced font
        self.text_widget = tk.Text(
            self,
            font=("JetBrains Mono", 18),
            bg="#2C2E31",
            fg="#646669",
            height=8,
            width=80,
            wrap="word",
            borderwidth=0,
            highlightthickness=0,
            padx=20,
            pady=20,
            insertbackground="#E2B714",
            insertwidth=2,
        )
        self.text_widget.pack(fill="both", expand=True)

        # Configure text tags for different character states
        self.text_widget.tag_config("unwritten", foreground="#646669")
        self.text_widget.tag_config("correct", foreground="#D1D0C5")
        self.text_widget.tag_config("error", foreground="#CA4754")
        self.text_widget.tag_config("cursor", background="#E2B714")

        # Keep text widget in normal state but prevent default input handling
        # All input will be handled manually through our event bindings
        self.text_widget.config(state="normal")

    def display_text(self, text: str):
        """Set initial text in display widget."""
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", text)
        # Keep in normal state so key bindings work
        self.update_colors(text, "", 0)

    def update_colors(self, target_text: str, input_text: str, char_index: int):
        """
        Update character colors based on typing progress.
        Unwritten: #646669, Correct: #D1D0C5, Error: #CA4754

        Args:
            target_text: The text being typed
            input_text: User's input so far
            char_index: Current position in target text
        """
        # Remove all existing tags
        for tag in ["unwritten", "correct", "error", "cursor"]:
            self.text_widget.tag_remove(tag, "1.0", "end")

        # Apply color tags based on character status
        for i, char in enumerate(target_text):
            pos_start = f"1.0+{i}c"
            pos_end = f"1.0+{i+1}c"

            if i >= char_index:
                # Unwritten characters
                self.text_widget.tag_add("unwritten", pos_start, pos_end)
            elif i < len(input_text):
                # Compare with input
                if target_text[i] == input_text[i]:
                    self.text_widget.tag_add("correct", pos_start, pos_end)
                else:
                    self.text_widget.tag_add("error", pos_start, pos_end)
            else:
                self.text_widget.tag_add("unwritten", pos_start, pos_end)


class StatisticsPanel(ctk.CTkFrame):
    """Display real-time typing statistics (WPM, Accuracy)."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color="#2C2E31")

        # WPM Display
        self.wpm_label = ctk.CTkLabel(
            self,
            text="0",
            font=("JetBrains Mono", 48, "bold"),
            text_color="#E2B714",
        )
        self.wpm_label.pack(side="left", padx=40)

        self.wpm_unit = ctk.CTkLabel(
            self,
            text="WPM",
            font=("JetBrains Mono", 14),
            text_color="#646669",
        )
        self.wpm_unit.pack(side="left", padx=(0, 40))

        # Accuracy Display
        self.accuracy_label = ctk.CTkLabel(
            self,
            text="0%",
            font=("JetBrains Mono", 48, "bold"),
            text_color="#E2B714",
        )
        self.accuracy_label.pack(side="left", padx=40)

        self.accuracy_unit = ctk.CTkLabel(
            self,
            text="Accuracy",
            font=("JetBrains Mono", 14),
            text_color="#646669",
        )
        self.accuracy_unit.pack(side="left", padx=(0, 40))

    def update_stats(self, wpm: float, accuracy: float):
        """Update displayed statistics."""
        self.wpm_label.configure(text=f"{int(wpm)}")
        self.accuracy_label.configure(text=f"{accuracy:.1f}%")


class TypingScreen(ctk.CTkFrame):
    """Main typing test screen with text display and real-time feedback."""

    def __init__(self, parent, on_test_complete, on_show_history, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color="#2C2E31")

        self.on_test_complete = on_test_complete
        self.on_show_history = on_show_history
        self.engine: TypingEngine | None = None
        self.selected_duration = 30
        self.text_provider = WordProvider()
        self.data_manager = DatabaseManager()

        # Header with title
        header = ctk.CTkLabel(
            self,
            text="ZenType",
            font=("JetBrains Mono", 28, "bold"),
            text_color="#E2B714",
        )
        header.pack(pady=20)

        # Duration selector
        duration_frame = ctk.CTkFrame(self, fg_color="#2C2E31")
        duration_frame.pack(pady=10)

        ctk.CTkLabel(
            duration_frame,
            text="Duration:",
            font=("JetBrains Mono", 12),
            text_color="#646669",
        ).pack(side="left", padx=5)

        for duration in [30, 60, 90]:
            btn = ctk.CTkButton(
                duration_frame,
                text=f"{duration}s",
                font=("JetBrains Mono", 12),
                width=60,
                height=30,
                fg_color="#3C3E42" if duration != 30 else "#E2B714",
                text_color="#2C2E31" if duration == 30 else "#D1D0C5",
                command=lambda d=duration: self.set_duration(d),
            )
            btn.pack(side="left", padx=5)
            setattr(self, f"btn_{duration}", btn)

        # Statistics panel
        self.stats_panel = StatisticsPanel(self)
        self.stats_panel.pack(pady=20)

        # Text display
        self.typing_display = TypingDisplay(self, height=200)
        self.typing_display.pack(pady=20, padx=20, fill="both", expand=True)

        # Bottom controls
        control_frame = ctk.CTkFrame(self, fg_color="#2C2E31")
        control_frame.pack(pady=20)

        # Start Button
        self.start_button = ctk.CTkButton(
            control_frame,
            text="Start",
            font=("JetBrains Mono", 12),
            fg_color="#3C3E42",
            command=self.start_test,
        )
        self.start_button.pack(side="left", padx=5)

        ctk.CTkButton(
            control_frame,
            text="Reset (Tab)",
            font=("JetBrains Mono", 12),
            fg_color="#3C3E42",
            command=self.reset_test,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            control_frame,
            text="History",
            font=("JetBrains Mono", 12),
            fg_color="#3C3E42",
            command=self.on_show_history,
        ).pack(side="left", padx=5)

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Click to focus and start typing",
            font=("JetBrains Mono", 10),
            text_color="#646669",
        )
        self.status_label.pack(pady=10)

        # Focus overlay
        self.focus_overlay = ctk.CTkLabel(
            self.typing_display.text_widget,
            text="Click to Focus",
            font=("JetBrains Mono", 20),
            text_color="#E2B714",
            bg_color="#2C2E31",
        )

        self.init_test()

    def set_duration(self, duration: int):
        """Set test duration and update UI."""
        self.selected_duration = duration
        # Update button colors
        for d in [30, 60, 90]:
            btn = getattr(self, f"btn_{d}")
            if d == duration:
                btn.configure(fg_color="#E2B714", text_color="#2C2E31")
            else:
                btn.configure(fg_color="#3C3E42", text_color="#D1D0C5")

        self.reset_test()

    def init_test(self):
        """Initialize a new typing test."""
        word_count = self.text_provider.get_word_count_for_duration(
            self.selected_duration
        )
        target_text = self.text_provider.generate_text(word_count)

        self.engine = TypingEngine(target_text, self.selected_duration)
        self.typing_display.display_text(target_text)
        self.stats_panel.update_stats(0, 0)
        self.status_label.configure(text="Press Start to begin typing...")

        # Bind keyboard events to the text widget itself for better control
        # Unbind any previous bindings (use try-except to handle first call)
        for event in ["<Key>", "<BackSpace>", "<Tab>", "<Button-1>"]:
            try:
                self.typing_display.text_widget.unbind(event)
            except:
                pass  # Binding didn't exist, which is fine
        
        self.typing_display.text_widget.bind("<Key>", self.on_key)
        self.typing_display.text_widget.bind("<BackSpace>", self.on_backspace)
        self.typing_display.text_widget.bind("<Tab>", self.on_tab)
        
        # Prevent mouse clicks from moving cursor or selecting text
        self.typing_display.text_widget.bind("<Button-1>", lambda e: "break")
        self.typing_display.text_widget.bind("<B1-Motion>", lambda e: "break")
        self.typing_display.text_widget.bind("<Double-Button-1>", lambda e: "break")
        self.typing_display.text_widget.bind("<Triple-Button-1>", lambda e: "break")
        
        # Bind focus events to the main window
        self.master.bind("<FocusIn>", self.on_focus_in)
        self.master.bind("<FocusOut>", self.on_focus_out)

        # Start the update loop
        self.update_stats_loop()

    def start_test(self):
        """Start the typing test and allow user input."""
        # Ensure engine is initialized (defensive check)
        if self.engine is None:
            self.init_test()
        
        # Set focus to the text widget
        self.typing_display.text_widget.focus_set()
        
        # Start the test timer (safe to call multiple times - has guard)
        self.engine.start_timer()
        
        # Update status
        self.status_label.configure(text="Test started! Type away!")
        
        # Disable start button during test
        self.start_button.configure(state="disabled")

    def reset_test(self):
        """Reset the typing test to its initial state."""
        self.init_test()  # Properly reset the typing test
        # Re-enable start button
        self.start_button.configure(state="normal")

    def on_focus_in(self, event):
        """Handle when the window regains focus."""
        if hasattr(self, "focus_overlay"):
            self.focus_overlay.place_forget()  # Remove the focus overlay

    def on_focus_out(self, event):
        """Handle when the window loses focus."""
        if self.engine and self.engine.is_active:
            self.focus_overlay.place(relx=0.5, rely=0.5, anchor="center")  # Show the overlay

    def on_key(self, event):
        """Handle regular keypress events."""
        if self.engine is None:
            return "break"

        # Prevent typing before test starts
        if not self.engine.is_active:
            return "break"

        if self.engine.is_completed():
            self.finish_test()
            return "break"

        char = event.char
        if char and ord(char) >= 32:  # Printable characters only
            is_correct, idx = self.engine.handle_keypress(char)
            self.update_display()

        return "break"

    def on_backspace(self, event):
        """Handle backspace with word boundary restriction."""
        if self.engine and not self.engine.is_completed() and self.engine.is_active:
            self.engine.handle_backspace()
            self.update_display()
        return "break"
    
    def on_tab(self, event):
        """Handle Tab key to reset the test."""
        self.reset_test()
        return "break"

    def update_display(self):
        """Update text colors and statistics."""
        if self.engine is not None:
            self.typing_display.update_colors(
                self.engine.target_text, 
                self.engine.input_text, 
                self.engine.char_index
            )

    def update_stats_loop(self):
        """Update statistics every 500ms."""
        if self.engine and self.engine.is_active and not self.engine.is_completed():
            wpm = self.engine.calculate_wpm()
            accuracy = self.engine.calculate_accuracy()
            self.stats_panel.update_stats(wpm, accuracy)

        if self.engine and not self.engine.is_completed():
            self.after(500, self.update_stats_loop)
        elif self.engine and self.engine.is_completed():
            self.finish_test()

    def finish_test(self):
        """Complete test and show results."""
        if self.engine is not None:
            self.engine.finish_test()
            results = self.engine.get_test_results()
            self.data_manager.add_result(results)
            # Re-enable start button
            self.start_button.configure(state="normal")
            self.on_test_complete(results)


class ResultsScreen(ctk.CTkFrame):
    """Display test results and performance chart."""

    def __init__(self, parent, on_retry, on_new_duration, on_show_history, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color="#2C2E31")

        self.on_retry = on_retry
        self.on_new_duration = on_new_duration
        self.on_show_history = on_show_history

        # Title
        title = ctk.CTkLabel(
            self,
            text="Test Complete!",
            font=("JetBrains Mono", 28, "bold"),
            text_color="#E2B714",
        )
        title.pack(pady=20)

        # Results display frame
        results_frame = ctk.CTkFrame(self, fg_color="#2C2E31")
        results_frame.pack(pady=20)

        self.wpm_display = ctk.CTkLabel(
            results_frame,
            text="0 WPM",
            font=("JetBrains Mono", 48, "bold"),
            text_color="#E2B714",
        )
        self.wpm_display.pack(side="left", padx=40)

        self.accuracy_display = ctk.CTkLabel(
            results_frame,
            text="0%",
            font=("JetBrains Mono", 48, "bold"),
            text_color="#E2B714",
        )
        self.accuracy_display.pack(side="left", padx=40)

        # Chart canvas
        self.chart_canvas = Canvas(
            self,
            width=600,
            height=200,
            bg="#2C2E31",
            highlightthickness=0,
            borderwidth=0,
        )
        self.chart_canvas.pack(pady=20)

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="#2C2E31")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Retry (Same Duration)",
            font=("JetBrains Mono", 12),
            fg_color="#3C3E42",
            command=self.on_retry,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Change Duration",
            font=("JetBrains Mono", 12),
            fg_color="#3C3E42",
            command=self.on_new_duration,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="View History",
            font=("JetBrains Mono", 12),
            fg_color="#3C3E42",
            command=self.on_show_history,
        ).pack(side="left", padx=5)

    def display_results(self, results: dict, engine):
        """Display test results and chart."""
        wpm = results["wpm"]
        accuracy = results["accuracy"]

        self.wpm_display.configure(text=f"{int(wpm)} WPM")
        self.accuracy_display.configure(text=f"{accuracy:.1f}%")

        # Draw chart
        self.draw_chart(engine)

    def draw_chart(self, engine):
        """Draw WPM progression chart on canvas."""
        self.chart_canvas.delete("all")

        # Get WPM history
        wpm_history = engine.get_wpm_history(interval=1.0)

        if not wpm_history or len(wpm_history) < 2:
            return

        # Canvas dimensions
        canvas_width = 600
        canvas_height = 200
        margin = 40

        # Data ranges
        max_wpm = max(wpm_history) if wpm_history else 1
        max_time = len(wpm_history) - 1

        # Draw axes
        self.chart_canvas.create_line(
            margin, canvas_height - margin, canvas_width - margin, canvas_height - margin,
            fill="#646669", width=2
        )
        self.chart_canvas.create_line(
            margin, margin, margin, canvas_height - margin,
            fill="#646669", width=2
        )

        # Draw grid lines and labels
        for i in range(0, max(int(max_time) + 1, 2), max(1, int(max_time / 4))):
            x = margin + (i / max_time) * (canvas_width - 2 * margin) if max_time > 0 else margin
            self.chart_canvas.create_text(
                x, canvas_height - margin + 20,
                text=f"{i}s", fill="#646669", font=("JetBrains Mono", 10)
            )

        # Draw WPM history line
        for i in range(len(wpm_history) - 1):
            x1 = margin + (i / max_time) * (canvas_width - 2 * margin) if max_time > 0 else margin
            y1 = canvas_height - margin - (wpm_history[i] / max_wpm) * (canvas_height - 2 * margin) if max_wpm > 0 else canvas_height - margin

            x2 = margin + ((i + 1) / max_time) * (canvas_width - 2 * margin) if max_time > 0 else margin
            y2 = canvas_height - margin - (wpm_history[i + 1] / max_wpm) * (canvas_height - 2 * margin) if max_wpm > 0 else canvas_height - margin

            self.chart_canvas.create_line(x1, y1, x2, y2, fill="#E2B714", width=2)
            self.chart_canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="#E2B714")


class HistoryScreen(ctk.CTkFrame):
    """Display typing test history and statistics."""

    def __init__(self, parent, on_back_to_typing, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(fg_color="#2C2E31")

        self.on_back_to_typing = on_back_to_typing
        self.data_manager = DatabaseManager()

        # Back button at top-left
        back_button_frame = ctk.CTkFrame(self, fg_color="#2C2E31")
        back_button_frame.pack(anchor="nw", padx=20, pady=10)
        
        ctk.CTkButton(
            back_button_frame,
            text="← Back",
            font=("JetBrains Mono", 12),
            fg_color="#3C3E42",
            command=self.on_back_to_typing,
            width=100,
        ).pack()

        # Title
        title = ctk.CTkLabel(
            self,
            text="Statistics & History",
            font=("JetBrains Mono", 28, "bold"),
            text_color="#E2B714",
        )
        title.pack(pady=(0, 20))

        # Overall statistics
        stats = self.data_manager.get_statistics()
        
        # Check if there's any history
        if stats['total_tests'] == 0:
            # Show "No history" message
            no_history_frame = ctk.CTkFrame(self, fg_color="#2C2E31")
            no_history_frame.pack(pady=50, expand=True)
            
            ctk.CTkLabel(
                no_history_frame,
                text="No History Yet",
                font=("JetBrains Mono", 24, "bold"),
                text_color="#646669",
            ).pack(pady=20)
            
            ctk.CTkLabel(
                no_history_frame,
                text="Complete a typing test to see your results here",
                font=("JetBrains Mono", 12),
                text_color="#646669",
            ).pack(pady=10)
        else:
            # Show statistics and history
            stats_frame = ctk.CTkFrame(self, fg_color="#2C2E31")
            stats_frame.pack(pady=20)

            ctk.CTkLabel(
                stats_frame,
                text=f"Total Tests: {stats['total_tests']}",
                font=("JetBrains Mono", 12),
                text_color="#D1D0C5",
            ).pack(anchor="w", padx=20, pady=5)

            ctk.CTkLabel(
                stats_frame,
                text=f"Best WPM: {int(stats['best_wpm'])}",
                font=("JetBrains Mono", 12),
                text_color="#D1D0C5",
            ).pack(anchor="w", padx=20, pady=5)

            ctk.CTkLabel(
                stats_frame,
                text=f"Average WPM: {stats['average_wpm']:.1f}",
                font=("JetBrains Mono", 12),
                text_color="#D1D0C5",
            ).pack(anchor="w", padx=20, pady=5)

            ctk.CTkLabel(
                stats_frame,
                text=f"Average Accuracy: {stats['average_accuracy']:.1f}%",
                font=("JetBrains Mono", 12),
                text_color="#D1D0C5",
            ).pack(anchor="w", padx=20, pady=5)

            # Recent results
            ctk.CTkLabel(
                self,
                text="Recent Tests",
                font=("JetBrains Mono", 14, "bold"),
                text_color="#E2B714",
            ).pack(pady=(20, 10))

            # Results list frame with scrolling
            list_frame = ctk.CTkScrollableFrame(self, fg_color="#3C3E42", height=250)
            list_frame.pack(pady=10, padx=20, fill="both", expand=True)

            recent = self.data_manager.get_recent_results(10)
            for result in recent:
                result_text = f"{result.get('wpm', 0):.0f} WPM | {result.get('accuracy', 0):.1f}% | {result.get('duration', 0)}s | {result.get('timestamp', 'N/A').split('T')[0]}"
                ctk.CTkLabel(
                    list_frame,
                    text=result_text,
                    font=("JetBrains Mono", 11),
                    text_color="#D1D0C5",
                ).pack(anchor="w", padx=10, pady=5)


class ZenTypeApp(ctk.CTk):
    """Main application window for ZenType."""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("ZenType - Typing Speed Tester")
        self.geometry("1000x600")
        self.configure(fg_color="#2C2E31")

        # Center window on screen
        self.update_idletasks()
        width = 1000
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="#2C2E31")
        self.main_frame.pack(fill="both", expand=True)

        # Initialize screens
        self.typing_screen = TypingScreen(
            self.main_frame,
            on_test_complete=self.show_results,
            on_show_history=self.show_history,
        )

        self.results_screen = ResultsScreen(
            self.main_frame,
            on_retry=self.retry_test,
            on_new_duration=self.show_typing,
            on_show_history=self.show_history,
        )

        self.history_screen = HistoryScreen(
            self.main_frame,
            on_back_to_typing=self.show_typing,
        )

        self.show_typing()

    def show_typing(self):
        """Show typing screen."""
        self.results_screen.pack_forget()
        self.history_screen.pack_forget()
        self.typing_screen.pack(fill="both", expand=True)
        self.typing_screen.typing_display.text_widget.focus_set()

    def show_results(self, results: dict):
        """Show results screen."""
        self.typing_screen.pack_forget()
        self.history_screen.pack_forget()
        self.results_screen.pack(fill="both", expand=True)
        self.results_screen.display_results(results, self.typing_screen.engine)

    def show_history(self):
        """Show history screen."""
        self.typing_screen.pack_forget()
        self.results_screen.pack_forget()
        # Destroy old history screen and create fresh one
        self.history_screen.destroy()
        self.history_screen = HistoryScreen(
            self.main_frame,
            on_back_to_typing=self.show_typing,
        )
        self.history_screen.pack(fill="both", expand=True)

    def retry_test(self):
        """Retry test with same duration."""
        self.typing_screen.reset_test()
        self.show_typing()


if __name__ == "__main__":
    app = ZenTypeApp()
    app.mainloop()
