# game_engine.py
import random
import time
from settings import DIFFICULTY_SETTINGS


class Equation:
    def __init__(self, display, answer):
        self.display = display
        self.answer = answer


class GameEngine:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.config = DIFFICULTY_SETTINGS[difficulty]

        self.score = 0
        self.game_over = False

        self.equations = self._generate_equations()
        random.shuffle(self.equations)
        self.total_questions = len(self.equations)
        self.current_question_number = 0

        self.current_equation = None
        self.attempts_left = 0
        self.start_time = None

    # ==========================
    # PUBLIC METHODS
    # ==========================

    def next_equation(self):
        if not self.equations:
            self.game_over = True
            return None

        self.current_question_number += 1
        self.current_equation = self.equations.pop()

        # Reset attempts and timer per question
        self.attempts_left = self.config["attempts"]
        self.start_time = time.time()

        return self.current_equation.display

    def check_guess(self, user_guess):
        if self.game_over:
            return False

        if user_guess == self.current_equation.answer:
            self._add_score()
            # Do NOT increase attempts; attempts stay the same
            return True

        # Wrong guess reduces attempts
        self.attempts_left -= 1
        if self.attempts_left <= 0:
            self.game_over = True

        return False

    def time_remaining(self):
        if not self.start_time:
            return self.config["time_limit"]
        elapsed = int(time.time() - self.start_time)
        remaining = self.config["time_limit"] - elapsed
        if remaining <= 0:
            # Game over if timer expires
            self.game_over = True
            return 0
        return remaining

    # ==========================
    # INTERNAL METHODS
    # ==========================

    def _add_score(self):
        self.score += self.config["score_multiplier"]

    def _generate_equations(self):
        equations = []
        total = self.config["equation_count"]
        single_op_limit = int(total * self.config["single_op_ratio"])

        while len(equations) < total:
            if len(equations) < single_op_limit:
                eq = self._single_operation()
            else:
                eq = self._two_operations()

            if eq:
                equations.append(eq)

        return equations

    def _single_operation(self):
        a, b = self._random_numbers(2)
        op = random.choice(self.config["operations"])

        if op == "/":
            b = random.randint(1, a)
            a = b * random.randint(1, 10)

        result = self._eval(a, b, op)
        hidden = random.choice(["a", "b"])

        if hidden == "a":
            return Equation(f"? {op} {b} = {result}", a)
        return Equation(f"{a} {op} ? = {result}", b)

    def _two_operations(self):
        a, b, c = self._random_numbers(3)
        op1, op2 = random.sample(self.config["operations"], 2)

        try:
            if op1 == "/":
                b = random.randint(1, a)
                a = b * random.randint(1, 10)

            temp = self._eval(a, b, op1)

            if op2 == "/":
                # Ensure temp >= 1 to avoid empty range
                temp = max(1, temp)
                c = random.randint(1, temp)
                temp = c * random.randint(1, 10)

            result = self._eval(temp, c, op2)
        except ZeroDivisionError:
            return None
        except ValueError:
            return None  # catches empty range errors

        hidden = random.choice(["a", "b", "c"])

        if hidden == "a":
            return Equation(f"? {op1} {b} {op2} {c} = {result}", a)
        if hidden == "b":
            return Equation(f"{a} {op1} ? {op2} {c} = {result}", b)
        return Equation(f"{a} {op1} {b} {op2} ? = {result}", c)

    def _eval(self, x, y, op):
        if op == "+":
            return x + y
        if op == "-":
            return x - y
        if op == "*":
            return x * y
        if op == "/":
            return x // y

    def _random_numbers(self, count):
        low, high = self.config["number_range"]
        return [random.randint(low, high) for _ in range(count)]
