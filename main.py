# main.py

from data_manager import DataManager
from quiz_game import QuizGame
from console_ui import ConsoleUI
import signal


def main():
    # Ctrl+Z가 발생시킨 정지 신호를 무시한다.
    if hasattr(signal, "SIGTSTP"):
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)

    # 게임 데이터 관리 객체 생성 ("state.json" 파일을 사용)
    data_manager = DataManager("state.json")

    # 게임 데이터 불러오기
    # 추가: 기존 퀴즈/점수 기록뿐 아니라 최고 점수와 최고 게임 기록도 불러온다.
    quizzes, score_history, best_score, best_game = data_manager.load()

    # 콘솔 UI 객체 생성
    ui = ConsoleUI()

    # 게임 객체 생성
    # 추가: 최고 점수와 최고 게임 기록도 QuizGame에 전달한다.
    game = QuizGame(
        quizzes,
        score_history,
        best_score,
        best_game,
        ui,
    )

    try:
        # 게임 진행
        game.run()

    # KeyboardInterrupt : 사용자가 Ctrl+C를 눌러 프로그램을 강제 종료할 때 발생하는 예외
    # EOFError : 사용자가 Ctrl+D를 눌러 입력을 종료할 때 발생하는 예외
    except (KeyboardInterrupt, EOFError):
        print(
            "\n\n프로그램이 사용자에 의해 중단 되었습니다. 안전하게 게임을 종료합니다."
        )

    finally:
        # 게임 종료 시점에 데이터 저장
        # 추가: 최고 점수와 최고 게임 기록도 state.json에 함께 저장한다.
        data_manager.save(
            quizzes=game.quizzes,
            score_history=game.score_history,
            best_score=game.best_score,
            best_game=game.best_game,
        )

        print("게임 데이터를 저장하고 종료합니다. 다음에 또 만나요!")


if __name__ == "__main__":
    main()


# 파이썬 표준 라이브러리

# 파이썬에서 파일이나 폴더의 경로(path)를 다루기 위해 제공되는 모듈

# 기존 파이썬에선 파일 경로를 다룰 때 문자열로 다루었음,
# pathlib은 경로 자체를 하나의 객체로 다룸.

# 장점 : 기존은 윈도우(\)와 맥/리눅스(/) 경로 구분자가 달라 오류가 날 수 있었음.
# pathlib을 쓰면 파이썬이 실행환경에 맞게 경로를 올바르게 처리함.

# __name__ 변수(str) :
# 파일 실행 시 __name__ 이라는 내장 특수 변수를 자동으로 생성.

# 1. 파일 직접 실행 시 : __name__ = "__main__"
# 조건문이 참이 되어 main() 함수 실행됨.

# 2. 다른 파일에서 import 시 : __name__ = "파일명"
# 조건문이 거짓이 되어 main() 함수 실행되지 않음.

# 왜 이렇게 사용?
# 1. 코드의 재사용성(모듈화)
# 파일 하나를 독립 실행 프로그램으로도 사용하고,
# 다른 파일에서 모듈로도 활용하기 위함.

# 2. 테스트 용이성
# 개발 중 해당 파일이 제대로 작동하는지 자체 테스트하는 코드(main())를 넣어두고
# 나중에 다른 파일에서 가져다 쓸 때는 테스트 코드가 동작하지 않도록 함.

# 내장 특수 변수 :
# 개발자가 직접 만들지 않아도 파이썬 인터프리터가 자동으로 생성하는 전역 변수.
# 변수 이름 앞뒤로 __가 붙음.
# 더블 언더스코어, 매직변수, 던더변수라 불림.

# __init__() :
# 생성자 메서드.
# 클래스로부터 새로운 객체(인스턴스)를 만들 때 자동으로 호출되는 초기화 메서드.

# self :
# 객체 자신을 가리키는 파이썬의 매개변수.
# 클래스를 사용해 객체를 만들 때 그 객체를 가리키는 참조값이 self가 됨.

# @classmethod :
# 클래스 메서드 장식자.
# 클래스에 직접 작동하는 기능임을 알려줌.
# 객체를 만들기 전에도 클래스 이름으로 호출할 수 있음.

# cls :
# 현재 클래스 자신을 의미함.

# JSON :
# 데이터 저장 및 주고받을 때 사용하는 대표적인 텍스트 기반 데이터 형식.
# 키-값 구조이며 여러 프로그래밍 언어에서 사용할 수 있음.

# 프로그램 실행 중 메모리에 있는 Quiz 객체를 JSON에 그대로 저장할 수 없으므로
# Quiz.to_dict()를 사용해 딕셔너리로 변환한 뒤 저장한다.

# 프로그램 시작 시에는 JSON 딕셔너리를 Quiz.from_dict()를 통해
# 다시 Quiz 객체로 복원한다.