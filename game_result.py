from dataclasses import dataclass


@dataclass
class GameResult:
    question_passed: int
    mistakes_made: int
    win: bool
