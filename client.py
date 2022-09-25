from GAME_STATUS import GameStatus
from game import Game
from game_result import GameResult


def end_of_game_handler(result: GameResult):
    print(f'Question asked {result.question_passed}. Mistakes made {result.mistakes_made}.')
    print('You won!' if result.win else 'You lost!')


game = Game('question.csv', end_of_game_handler, allowed_mistake=2)


while game.game_status == GameStatus.IN_PROGRESS:

    q = game.get_next_question()
    print('Do you believe in the next statement or question? Enter "y" or "n": ')
    print(q.text)

    answer = input() == 'y'

    if q.is_true == answer:
        print('Good job! You are right!')
    else:
        print('Oops, actually you are mistaken. Here is the explanation:')
        print(q.explanation)

    game.give_answer(answer)
