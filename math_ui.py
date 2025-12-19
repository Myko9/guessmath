# math_ui.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from game_engine import GameEngine

# Set window size (for testing on desktop)
Window.size = (650, 480)

class MathGuessUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=10, **kwargs)
        self.engine = None
        self.timer_event = None
        self.themes = {
            "easy": {"bg": (232/255, 245/255, 233/255, 1), "accent": (46/255, 125/255, 50/255, 1)},
            "medium": {"bg": (255/255, 243/255, 224/255, 1), "accent": (239/255, 108/255, 0, 1)},
            "hard": {"bg": (251/255, 233/255, 231/255, 1), "accent": (198/255, 40/255, 40/255, 1)},
        }

        # Dark text color
        self.text_color = (0, 0, 0, 1)

        # Title
        self.title_label = Label(text="Math Guessing Game", font_size=24, size_hint=(1, 0.1), color=self.text_color)
        self.add_widget(self.title_label)

        # Difficulty buttons
        self.diff_layout = GridLayout(cols=3, spacing=10, size_hint=(1, 0.1))
        self.easy_btn = Button(text="Easy", on_release=lambda x: self.start_game("easy"), color=self.text_color)
        self.medium_btn = Button(text="Medium", on_release=lambda x: self.start_game("medium"), color=self.text_color)
        self.hard_btn = Button(text="Hard", on_release=lambda x: self.start_game("hard"), color=self.text_color)
        self.diff_layout.add_widget(self.easy_btn)
        self.diff_layout.add_widget(self.medium_btn)
        self.diff_layout.add_widget(self.hard_btn)
        self.add_widget(self.diff_layout)

        # Equation label
        self.equation_label = Label(text="Select a difficulty to start", font_size=20, size_hint=(1, 0.15), color=self.text_color)
        self.add_widget(self.equation_label)

        # Progress and timer
        self.progress_label = Label(text="Question: 0 / 0", size_hint=(1, 0.05), color=self.text_color)
        self.timer_label = Label(text="Time Left: -", size_hint=(1, 0.05), color=self.text_color)
        self.add_widget(self.progress_label)
        self.add_widget(self.timer_label)

        # Input for guess
        self.input_layout = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, 0.1))
        self.guess_input = TextInput(multiline=False, font_size=18, foreground_color=self.text_color)
        self.submit_btn = Button(text="Submit Guess", on_release=lambda x: self.submit_guess(), color=self.text_color)
        self.input_layout.add_widget(Label(text="Your Guess:", size_hint=(0.3, 1), color=self.text_color))
        self.input_layout.add_widget(self.guess_input)
        self.input_layout.add_widget(self.submit_btn)
        self.add_widget(self.input_layout)

        # Feedback
        self.feedback_label = Label(text="", font_size=16, size_hint=(1, 0.1), color=self.text_color)
        self.add_widget(self.feedback_label)

        # Score and attempts
        self.status_layout = GridLayout(cols=2, size_hint=(1, 0.05))
        self.attempts_label = Label(text="Attempts Left: -", color=self.text_color)
        self.score_label = Label(text="Score: 0", color=self.text_color)
        self.status_layout.add_widget(self.attempts_label)
        self.status_layout.add_widget(self.score_label)
        self.add_widget(self.status_layout)

        # New Game button
        self.new_game_btn = Button(text="New Game", size_hint=(1, 0.1), on_release=lambda x: self.reset_game(), color=self.text_color)
        self.add_widget(self.new_game_btn)

        # Final score
        self.final_label = Label(text="", font_size=18, color=(0, 1, 0, 1), size_hint=(1, 0.1))
        self.add_widget(self.final_label)

    # ================= GAME CONTROL =================
    def start_game(self, difficulty):
        self.engine = GameEngine(difficulty)
        self.apply_theme(difficulty)
        self.final_label.text = ""
        self.score_label.text = "Score: 0"
        self.load_new_equation()

    def apply_theme(self, difficulty):
        theme = self.themes[difficulty]
        Window.clearcolor = theme["bg"]

    def load_new_equation(self, *args):
        if self.timer_event:
            self.timer_event.cancel()
        equation = self.engine.next_equation()
        if equation is None:
            self.end_game()
            return
        self.equation_label.text = equation
        self.progress_label.text = f"Question: {self.engine.current_question_number} / {self.engine.total_questions}"
        self.attempts_label.text = f"Attempts Left: {self.engine.attempts_left}"
        self.feedback_label.text = ""
        self.guess_input.text = ""
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def submit_guess(self):
        if not self.engine or self.engine.game_over:
            return
        try:
            guess = int(self.guess_input.text)
        except ValueError:
            self.feedback_label.text = "Please enter a number."
            return
        self.guess_input.text = ""
        correct = self.engine.check_guess(guess)
        self.score_label.text = f"Score: {self.engine.score}"
        if correct:
            self.feedback_label.text = "Correct! 🎉"
            Clock.schedule_once(lambda dt: self.load_new_equation(), 0.5)
        else:
            if self.engine.game_over:
                self.end_game()
            else:
                self.feedback_label.text = "Wrong! ❌"
                self.attempts_label.text = f"Attempts Left: {self.engine.attempts_left}"

    def update_timer(self, dt):
        if not self.engine or self.engine.game_over:
            return
        remaining = self.engine.time_remaining()
        accent = self.themes[self.engine.difficulty]["accent"]
        self.timer_label.color = accent if remaining > 5 else (1, 0, 0, 1)
        self.timer_label.text = f"Time Left: {remaining}s"
        if remaining <= 0:
            self.end_game()

    def end_game(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.engine.game_over = True
        self.final_label.text = f"Your Final Score: {self.engine.score}"

    def reset_game(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.engine = None
        self.guess_input.text = ""
        self.equation_label.text = "Select a difficulty to start"
        self.progress_label.text = "Question: 0 / 0"
        self.timer_label.text = "Time Left: -"
        self.attempts_label.text = "Attempts Left: -"
        self.score_label.text = "Score: 0"
        self.feedback_label.text = ""
        self.final_label.text = ""

class MathApp(App):
    def build(self):
        return MathGuessUI()
