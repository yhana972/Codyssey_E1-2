class ConsoleUI:
    """터미널의 사용자 입력과 화면 출력을 담당"""

    def show_main_menu(self) -> None:
        pass

    def get_number(self, message: str, min_value: int, max_value: int) -> int:
        pass

    def show_message(self, message: str) -> None:
        print(message)
