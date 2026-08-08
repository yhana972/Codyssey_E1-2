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
        while True:
            self.ui.show_main_menu()

            menu = self.ui.get_number(
                "메뉴를 선택하세요: ",
                0,
                5,
            )
            # menu 값에 따라 분기
            if menu == 1:
                self.add_quiz()

            elif menu == 2:
                self.ui.show_message("퀴즈 목록 기능 준비 중입니다.")

            elif menu == 3:
                self.ui.show_message("퀴즈 삭제 기능 준비 중입니다.")

            elif menu == 4:
                self.ui.show_message("퀴즈 풀기 기능 준비 중입니다.")

            elif menu == 5:
                self.ui.show_message("점수 기록 기능 준비 중입니다.")

            elif menu == 0:
                self.ui.show_message("게임을 종료합니다.")
                break

    def add_quiz(self) -> None:
        """새로운 퀴즈를 추가한다."""

        self.ui.show_message("=== 퀴즈 추가 ===")
        # 문제 입력
        question = self.ui.get_text("문제를 입력하세요: ")
        # 선택지 4개 입력
        choices = []
        for number in range(1, 5):
            choice = self.ui.get_text(f"선택지 {number}:")
            choices.append(choice)
        # 정답 번호 입력
        answer = self.ui.get_number(
            "정답 : ",
            1,
            len(choices),
        )
        # 힌트 입력
        hint = self.ui.get_text("힌트 입력 : ")
        # Quiz 객체 생성
        quiz = Quiz(question=question, choices=choices, answer=answer, hint=hint)
        # self.quizzes에 추가
        self.quizzes.append(quiz)
        # 완료 메시지
        self.ui.show_message("=== 퀴즈 추가 완료 ===")
