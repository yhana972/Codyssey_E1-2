# quiz_game.py

from quiz import Quiz
from console_ui import ConsoleUI
import random
from datetime import datetime


class QuizGame:
    """
    게임의 전반적인 진행 담당.
    """

    def __init__(
        self,
        quizzes,
        score_history,
        best_score,
        best_game,
        ui: ConsoleUI,
    ):
        self.quizzes = quizzes
        self.score_history = score_history

        # 추가:
        # 현재까지의 역대 최고 점수를 보관한다.
        self.best_score = best_score

        # 추가:
        # 역대 최고 점수를 달성한 게임의 상세 기록을 보관한다.
        # 아직 게임 기록이 없다면 None이다.
        self.best_game = best_game

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
            choice = self.ui.get_text(f"선택지 {number}: ")
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
        quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )

        # self.quizzes에 추가
        self.quizzes.append(quiz)

        # 완료 메시지
        self.ui.show_message("=== 퀴즈 추가 완료 ===")

    def show_quizzes(self) -> None:
        """등록된 퀴즈 목록을 출력한다."""

        # 퀴즈가 없는 경우 처리
        if not self.quizzes:
            self.ui.show_message("등록된 퀴즈가 없습니다.")
            return

        # 퀴즈 목록 순회
        self.ui.show_message("=== 퀴즈 목록 ===")

        for index, quiz in enumerate(self.quizzes, start=1):
            self.ui.show_quiz(
                quiz=quiz,
                number=index,
            )
            print()

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
        delete_number = self.ui.get_number(
            "삭제할 퀴즈 번호: ",
            1,
            len(self.quizzes),
        )

        # 4. 사용자 번호 → 리스트 인덱스로 변환
        delete_index = delete_number - 1

        # 5. 삭제 대상 출력
        selected_quiz = self.quizzes[delete_index]

        self.ui.show_quiz(
            selected_quiz,
            number=delete_number,
        )

        # 6. 삭제 여부 확인
        confirmed = self.ui.get_yes_no(
            "정말 삭제하시겠습니까? (y/n) : "
        )

        # 7. 삭제 취소
        if not confirmed:
            self.ui.show_message("삭제를 취소 하셨습니다.")
            return

        # 8. 실제 삭제
        deleted_quiz = self.quizzes.pop(delete_index)

        # 9. 결과 메시지
        self.ui.show_message(
            f"'{deleted_quiz.question}' 퀴즈를 삭제했습니다."
        )

    def play_quiz(self) -> None:
        """등록된 퀴즈를 랜덤으로 풀고 점수를 계산한다."""

        # 1. 퀴즈가 없는지 확인
        if not self.quizzes:
            self.ui.show_message(
                "등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요."
            )
            return

        # 몇 개의 퀴즈를 풀지 선택
        quiz_count = self.ui.get_number(
            f"{len(self.quizzes)} 문제 중 몇 문제를 푸실건가요? : ",
            1,
            len(self.quizzes),
        )

        # 전체 퀴즈에서 선택한 개수만큼 중복 없이 랜덤 추출
        random_quizzes = random.sample(
            self.quizzes,
            quiz_count,
        )

        # 한 문제당 배점 계산
        one_score = 100 / quiz_count

        # 점수 관련 변수 초기화
        correct_count = 0
        earned_score = 0.0
        hint_count = 0

        self.ui.show_message("=== 퀴즈 풀기 ===")

        # 퀴즈 순회
        for number, quiz in enumerate(
            random_quizzes,
            start=1,
        ):
            # 문제마다 힌트 사용 여부를 새로 초기화
            used_hint = False

            # 문제 출력
            self.ui.show_quiz(
                quiz=quiz,
                number=number,
            )

            # 문제에 힌트가 있다면 힌트 보기 여부 물어보기
            if quiz.hint:
                used_hint = self.ui.get_yes_no(
                    "힌트를 보시겠습니까? (y/n): "
                )

                if used_hint:
                    self.ui.show_message(
                        f"힌트 : {quiz.hint}"
                    )
                    hint_count += 1

            # 사용자 답 입력
            user_answer = self.ui.get_number(
                "정답 : ",
                1,
                len(quiz.choices),
            )

            # 정답 판정
            if quiz.is_correct(user_answer):
                correct_count += 1

                # 힌트를 사용하고 정답을 맞힌 경우
                # 해당 문제 점수의 50%만 획득
                if used_hint:
                    earned_score += one_score * 0.5

                    self.ui.show_message(
                        f"[정답] +{one_score * 0.5:.1f}점 획득"
                    )

                # 힌트를 사용하지 않고 정답을 맞힌 경우
                # 해당 문제 배점을 모두 획득
                else:
                    earned_score += one_score

                    self.ui.show_message(
                        f"[정답] +{one_score:.1f}점 획득"
                    )

            else:
                self.ui.show_message(
                    f"[오답] 정답은 "
                    f"{quiz.choices[quiz.answer - 1]}입니다!"
                )

            self.ui.show_message("-" * 30)

        # 최종 점수를 소수점 첫째 자리까지 저장
        final_score = round(earned_score, 1)

        # 최종 결과 출력
        self.ui.show_message("=== 최종 결과 ===")
        self.ui.show_message(
            f"정답 수 / 총 문제 수 : "
            f"{correct_count} / {quiz_count}"
        )
        self.ui.show_message(
            f"힌트 사용 : {hint_count}회"
        )
        self.ui.show_message(
            f"총 점수 : {final_score:.1f} / 100"
        )

        # 게임 종료 시간 생성
        game_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # 이번 게임의 전체 기록 생성
        game_record = {
            "played_at": game_time,
            "question_count": quiz_count,
            "correct_count": correct_count,
            "hint_count": hint_count,
            "score": final_score,
        }

        # 전체 점수 기록에 이번 게임 추가
        self.score_history.append(game_record)

        # 추가:
        # 아직 최고 기록이 없거나
        # 이번 점수가 기존 최고 점수보다 높은 경우
        # 최고 점수와 최고 게임 기록을 함께 갱신한다.
        #
        # > 를 사용하므로 동일한 최고 점수가 다시 나온 경우에는
        # 먼저 최고 점수를 달성했던 기록을 유지한다.
        if (
            self.best_game is None
            or final_score > self.best_score
        ):
            self.best_score = final_score
            self.best_game = game_record

            self.ui.show_message(
                f"새로운 최고 기록입니다! "
                f"{self.best_score:.1f}점"
            )

    def show_score_history(self) -> None:
        """저장된 게임 점수 기록을 출력한다."""

        # 기록 없음 검사
        if not self.score_history:
            self.ui.show_message(
                "아직 저장된 점수 기록이 없습니다."
            )
            return

        # 추가:
        # 최고 게임 기록이 있다면 전체 기록보다 먼저 출력한다.
        if self.best_game is not None:
            self.ui.show_best_record(
                self.best_game
            )

        # 전체 게임 기록 출력
        for number, record in enumerate(
            self.score_history,
            start=1,
        ):
            self.ui.show_score_record(
                record=record,
                number=number,
            )