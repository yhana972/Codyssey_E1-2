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
                self.show_quizzes()

            elif menu == 3:
                self.delete_quiz()

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

    def show_quizzes(self) -> None:
        """등록된 퀴즈 목록을 출력한다."""

        # 퀴즈가 없는 경우 처리(퀴즈 전부 삭제 시에 나올 메세지)
        if not self.quizzes:
            self.ui.show_message("등록된 퀴즈가 없습니다.")
            return
        # 퀴즈 목록 순회
        self.ui.show_message("=== 퀴즈 목록 ===")
        for index, quiz in enumerate(self.quizzes, start=1):
            # UI를 통해 각 퀴즈 출력
            self.ui.show_quiz(quiz=quiz, number=index)
            print(f"\n")
        self.ui.show_message("================")

    def delete_quiz(self) -> None:
        """등록된 퀴즈를 삭제한다."""

        # 1. 퀴즈가 없는지 확인
        if not self.quizzes:
            self.ui.show_message("등록된 퀴즈가 없습니다.")
            return
        # 2. 퀴즈 목록 출력
        self.show_quizzes()
        # 3. 삭제할 번호 입력
        delete_number = self.ui.get_number("삭제할 퀴즈 번호:", 1, len(self.quizzes))
        # 4. 사용자 번호 → 리스트 인덱스로 변환
        delete_index = delete_number - 1
        # 5. 삭제 대상 출력
        selected_quiz = self.quizzes[delete_index]
        self.ui.show_quiz(
            selected_quiz, number=delete_number
        )  # delete_number는 사용자가 입력한 값임.
        # 6. 삭제 여부 확인
        confirmed = self.ui.get_yes_no("정말 삭제하시겠습니까? (y/n) : ")
        # 7. 삭제
        if not confirmed:
            self.ui.show_message("삭제를 취소 하셨습니다.")
            return
        # 8. 결과 메시지
        delete_quiz = self.quizzes.pop(delete_index)
        self.ui.show_message(f"'{delete_quiz.question}' 퀴즈를 삭제했습니다.")
