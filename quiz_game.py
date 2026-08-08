from quiz import Quiz
from console_ui import ConsoleUI


class QuizGame:
    """
    게임의 전반적인 진행 담당.
    """

    # 객체 생성 시 퀴즈 목록, 점수 히스토리를 받아 내부 변수에 저장.
    # 각 메소드의
    def __init__(self, quizzes, score_history, ui: ConsoleUI):
        self.quizzes = quizzes
        self.score_history = score_history
        self.ui = ui

    def run(self):
        """게임 진행"""
        self.ui.show_main_menu()
        # menu = self.ui.get_number()
