# console_ui.py

from quiz import Quiz


class ConsoleUI:
    """터미널의 사용자 입력과 화면 출력을 담당"""

    # 입력
    def get_number(
        self,
        message: str,
        min_value: int,
        max_value: int,
    ) -> int:
        while True:
            value = input(message).strip()

            # 1. 빈 입력 검사
            if not value:
                self.show_message("값을 입력해주세요.")
                continue

            # 2. 숫자인지 검사
            if not value.isdigit():
                self.show_message("숫자를 입력해주세요.")
                continue

            # 3. int로 변환
            number = int(value)

            # 4. min_value ~ max_value 범위 검사
            if not min_value <= number <= max_value:
                self.show_message(
                    f"{min_value}부터 {max_value} 사이의 숫자를 입력해주세요."
                )
                continue

            # 5. 정상 값 return
            return number

    def get_text(self, message: str) -> str:
        """빈 문자열이 아닌 값을 입력받는다."""

        while True:
            value = input(message).strip()

            # 빈 값이면 안내 후 다시 입력
            if not value:
                self.show_message("값을 입력해주세요.")
                continue

            # 정상 값이면 return
            return value

    def get_yes_no(self, message: str) -> bool:
        """y 또는 n을 입력받아 bool로 반환한다."""

        while True:
            value = input(message).strip().lower()

            # y → True
            if value == "y":
                return True

            # n → False
            elif value == "n":
                return False

            # 그 외 → 안내 후 재입력
            else:
                self.show_message(
                    "대문자 Y, N 또는 소문자 y, n으로 입력해주세요."
                )

    # 출력
    def show_message(self, message: str) -> None:
        print(message)

    def show_main_menu(self) -> None:
        print(
            """
=== 메인 메뉴 ===
1. 퀴즈 추가
2. 퀴즈 목록
3. 퀴즈 삭제
4. 퀴즈 풀기
5. 점수 기록
0. 종료
================
"""
        )

    def show_quiz(
        self,
        quiz: Quiz,
        number: int | None = None,
    ) -> None:
        """퀴즈 한 문제와 선택지를 출력한다."""

        # number가 있다면 문제 번호 출력
        if number is not None:
            print(f"[{number}번 문제]")

        print(quiz.question)

        for index, choice in enumerate(quiz.choices, start=1):
            print(f"{index}. {choice}")

    def show_best_record(self, record: dict) -> None:
        """
        추가:
        역대 최고 점수를 달성한 게임의 전체 기록을 출력한다.
        """
        print("=== 최고 기록 ===")
        print(f"날짜/시간 : {record['played_at']}")
        print(f"문제 수   : {record['question_count']}")
        print(f"정답 수   : {record['correct_count']}")
        print(f"힌트 사용 : {record['hint_count']}회")
        print(f"최고 점수 : {record['score']} / 100")
        print("=" * 30)

    def show_score_record(
        self,
        record: dict,
        number: int,
    ) -> None:
        """게임 한 판의 점수 기록을 출력한다."""

        print("=== 점수 기록 ===")
        print(f"[{number}번째 게임]")
        print(f"날짜/시간 : {record['played_at']}")
        print(f"문제 수   : {record['question_count']}")
        print(f"정답 수   : {record['correct_count']}")
        print(f"힌트 사용 : {record['hint_count']}회")
        print(f"점수      : {record['score']} / 100")
        print("-" * 30)