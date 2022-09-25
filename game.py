from typing import Callable
from GAME_STATUS import GameStatus
from create_question import Question
from game_result import GameResult


class Game:

    def __init__(self, file_path: str, end_of_game_event: Callable, allowed_mistake: int):
        if allowed_mistake > 5 or allowed_mistake < 1:
            raise ValueError(f'Allowed mistakes must be from 1 to 5. You inputted {allowed_mistake}.')
        self.__file_path = file_path
        self.__allowed_mistake = allowed_mistake
        self.__end_of_game_event = end_of_game_event
        self.__mistakes = 0
        self.__counter = 0
        self.__question: list[Question] = []
        self.__game_status = GameStatus.IN_PROGRESS

        self.__fill_in_question(file_path, self.__question)

    @property
    def game_status(self):
        return self.__game_status

    def get_next_question(self) -> Question:
        return self.__question[self.__counter]

    def is_last_question(self) -> bool:
        return self.__counter == len(self.__question) - 1

    def give_answer(self, answer: bool):

        def exceeded_allowed_mistakes():
            return self.__mistakes > self.__allowed_mistake

        if self.__question[self.__counter].is_true != answer:
            self.__mistakes += 1

        if self.is_last_question() or exceeded_allowed_mistakes():
            self.__game_status = GameStatus.IS_OVER

            result = GameResult(self.__counter + 1, self.__mistakes, self.__mistakes <= self.__allowed_mistake)
            self.__end_of_game_event(result)

        self.__counter += 1

    def __fill_in_question(self, file_path, questions):
        with open(file_path, encoding='utf8') as file:
            for line in file:
                q = self.__parse_line(line)
                questions.append(q)

    def __parse_line(self, line) -> Question:
        parts = line.split(sep=';')
        test = parts[0]
        is_correct = parts[1] == 'Yes'
        explanation = parts[2]

        return Question(test, is_correct, explanation)
