from quiz import Quiz


class ConsoleUI:
    """터미널의 사용자 입력과 화면 출력을 담당"""

    def show_main_menu(self) -> None:
        print("""
=== 메인 메뉴 ===
  1. 퀴즈 추가
  2. 퀴즈 목록
  3. 퀴즈 삭제
  4. 퀴즈 풀기
  5. 점수 기록
  0. 종료
================
            """)

    def show_quiz(
        self,
        quiz: Quiz,
        number: int | None = None,
    ) -> None:
        """퀴즈 한 문제와 선택지를 출력한다."""

        # number가 있다면 문제 번호 출력
        if number is not None:
            # quiz.question 출력
            print(f"[{number}번 문제]")
        print(quiz.question)
        for index, choice in enumerate(quiz.choices, start=1):
            # quiz.choices를 번호와 함께 출력
            print(f"{index}. {choice}")

    def get_number(self, message: str, min_value: int, max_value: int) -> int:
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

    def show_message(self, message: str) -> None:
        print(message)
