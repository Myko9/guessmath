# settings.py
# Central configuration for Math Guessing Game

DIFFICULTY_SETTINGS = {
    "easy": {
        "number_range": (1, 10),
        "operations": ["+", "-"],
        "attempts": 7,
        "score_multiplier": 10,
        "single_op_ratio": 0.7,
        "equation_count": 100,
        "time_limit": 35  # seconds per question
    },
    "medium": {
        "number_range": (1, 50),
        "operations": ["+", "-", "*"],
        "attempts": 5,
        "score_multiplier": 20,
        "single_op_ratio": 0.5,
        "equation_count": 100,
        "time_limit": 25
    },
    "hard": {
        "number_range": (1, 100),
        "operations": ["+", "-", "*", "/"],
        "attempts": 3,
        "score_multiplier": 30,
        "single_op_ratio": 0.3,
        "equation_count": 100,
        "time_limit": 15
    }
}
