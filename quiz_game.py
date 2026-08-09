from quiz import Quiz
from console_ui import ConsoleUI
import random
from datetime import datetime


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
                self.play_quiz()

            elif menu == 5:
                self.show_score_history()

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
            self.ui.show_message("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
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

    def play_quiz(self) -> None:
        """등록된 퀴즈를 순서대로 풀고 점수를 계산한다."""

        # 1. 퀴즈가 없는지 확인
        if not self.quizzes:
            self.ui.show_message("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        # + 몇개의 퀴즈를 풀건지 선택 및 문제 랜덤으로 돌리기
        quiz_count = self.ui.get_number(
            f"{len(self.quizzes)} 문제 중 몇 문제를 푸실건가요? : ",
            1,
            len(self.quizzes),
        )
        random_quizzes = random.sample(self.quizzes, quiz_count)
        # 한문제 당 배점 계산
        one_score = 100 / quiz_count
        # 2. 점수 초기화
        correct_score = 0  # 맞힌 문제 개수
        earned_score = 0  # 실제 획득 점수
        hint_count = 0  # 힌트 사용 개수
        self.ui.show_message("=== 퀴즈 풀기 ===")
        # 3. 퀴즈 순회
        for number, quiz in enumerate(random_quizzes, start=1):
            used_hint = False  # 퀴즈 당 힌트 사용 여부 체크
            # 4. 문제 출력
            self.ui.show_quiz(quiz=quiz, number=number)
            # + 문제에 힌트가 있다면 힌트 보기 여부 물어보기
            if quiz.hint:
                used_hint = self.ui.get_yes_no("힌트를 보시겠습니까? (y/n): ")
                if used_hint:
                    self.ui.show_message(f"힌트 : {quiz.hint}")
                    hint_count += 1
            # 5. 사용자 답 입력
            user_answer = self.ui.get_number("정답 : ", 1, len(quiz.choices))
            # 6. 정답 판정
            if quiz.is_correct(user_answer):
                # 정답
                correct_score += 1
                if used_hint:  # 힌트 써서 맞췄다면 획득점수의 반만 점수가 오르게
                    earned_score += one_score * 0.5
                    self.ui.show_message(f"[정답] +{one_score * 0.5}점 획득")
                else:
                    earned_score += one_score
                    self.ui.show_message(f"[정답] +{one_score}점 획득")
            else:
                # 오답
                self.ui.show_message(
                    f"[오답] 정답은 {quiz.choices[quiz.answer-1]}입니다!"
                )
            self.ui.show_message("-" * 30)
        # 7. 최종 결과 출력

        self.ui.show_message("=== 최종 결과 ===")
        self.ui.show_message(f"맞은 갯수 / 총 문제 수 : {correct_score} / {quiz_count}")
        self.ui.show_message(f"힌트 사용 : {hint_count}회")
        self.ui.show_message(f"총 점수 : {earned_score:.1f} / 100")

        game_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        game_record = {
            "played_at": game_time,
            "question_count": quiz_count,
            "correct_count": correct_score,
            "hint_count": hint_count,
            "score": round(earned_score, 1),
        }
        self.score_history.append(game_record)  # 게임 히스토리 저장

    def show_score_history(self) -> None:
        """저장된 게임 점수 기록을 출력한다."""

        # 기록 없음 검사
        if not self.score_history:
            self.ui.show_message("아직 저장된 점수 기록이 없습니다.")
            return
        # 기록 반복
        for number, record in enumerate(self.score_history, start=1):
            # UI를 통해 출력
            self.ui.show_score_record(record=record, number=number)
