#파이썬 표준 라이브러리
# 파이썬에서 파일이나 폴더의 경로(path)를 다루기 위해 제공되는 모듈
# 기존 파이썬에선 파일 경로를 다룰 때 문자열로 다루었음, pathlib은 경로 자체를 하나의 객체로 다룸. 
# 장점 : 기존은 윈도우(\)와 맥/리눅스(/) 경로 구분자가 달라 오류가 났음. pathlib 쓰면 파이썬이 알아서
# 실행환경에 맞게 경로를 올바르게 처리함. 
from pathlib import Path

class Quiz:
    """
    Quiz 클래스는 퀴즈 한 문제의 데이터와 정답 판정을 담당.
    """
    pass

class DataManager:
    """
    게임 데이터를 파일에서 읽고 파일로 저장함.
    """
    def __init__(self, file_path:str):
        self.file_path = Path(file_path)

    def load(self):
        """퀴즈 목록/ 점수 기록을 불러오기"""
        return [], [] # 퀴즈 목록, 점수 히스토리

    def save(self, quizzes, score_history):
        """퀴즈 목록/ 점수 기록을 저장"""
        pass


class QuizGame:
    """ 
    게임의 전반적인 진행 담당.
    """
    # 객체 생성 시 퀴즈 목록, 점수 히스토리를 받아 내부 변수에 저장.
    # 각 메소드의 
    def __init__(self, quizzes, score_history):
        self.quizzes = quizzes
        self.score_history = score_history

    def run(self):
        """게임 진행"""
        pass

def main():
    # 게임 데이터 관리 객체 생성 ("state.json" 파일을 사용)
    data_manager = DataManager("state.json")

    # 게임 데이터 불러오기
    quizzes, score_history = data_manager.load()

    # 게임 객체 생성 (퀴즈 목록과 점수 기록을 전달)
    game = QuizGame(quizzes, score_history)


    try: #에러가 발생할 가능성이 있는 코드를 넣는곳
        # 게임 진행
        game.run()
    # keyboardInterrupt : 사용자가 Ctrl+C를 눌러 프로그램을 강제 종료할 때 발생하는 예외 
    # EOFError : 사용자가 Ctrl+D를 눌러 입력을 종료할 때 발생하는 예외
    except(KeyboardInterrupt, EOFError): #에러가 생겼을때 실행됨.
        print("\n\n프로그램이 사용자에 의해 중단 되었습니다. 안전하게 게임을 종료합니다.")
    finally: #에러가 나든 안나든 무조건 실행. 마무리/정리 작업 담당. 외부 자원 다룰때(파일 읽쓰. DB 연결, 네트워크 통신 등) 필수적으로 사용. 

        # 게임 종료 시점에 데이터 저장
        data_manager.save(quizzes=game.quizzes, score_history=game.score_history)
        print("게임 데이터를 저장하고 종료합니다. 다음에 또 만나요!")

if __name__ == "__main__":
    main()

#__name__ 변수(str) : 파일 실행 시 __name__ 이라는 내장 특수 변수를 자동으로 생성. 
#  현재 파일이 어떻게 실행되었는지에 따라 다른 값이 들어감. 
# 1. 파일 직접 실행 시 : __name__ = "__main__" 할당됨. 조건 문이 참이 되어 main() 함수 실행됨.
# 2. 다른 파일에서 import 시 : __name__ = "파일명" 할당됨. 조건 문이 거짓이 되어 main() 함수 실행되지 않음.
# 왜 이렇게 사용?
# 1. 코드의 재사용성(모듈화) : 파일 하나를 독립 실행 프로그램으로도 사용하고, 다른 파일에서 모듈로도 활용하기 위함.
# 2. 테스트 용이성 : 개발 중 해당 파일이 제대로 작동하는지 자체 테스트하는 코드(main()) 을 넣어두고 나중에 다른 파일에서 가져다 쓸때는 테스트 코드가 동작하지 않도록 함. 

# 내장 특수 변수 : 개발자가 직접 만들지 않아도 파이썬 인터프리터가 자동으로 생성 하는 전역 변수. 변수 이름 앞뒤로 __가 붙음. 더블 언더스코어, 매직변수, 던더변수라 불림. 
# 왜 사용? : 현재 모듈이나 객체의 정보를 알려주거나 프로그램 실행 환경의 상태를 전달하기 위함. 
# 내장 변수 자동 생성 이유 : 프로그램의 메타데이터(시스템 상태, 환경정보)를 일관되고 안전하게 제공하기 위함. 

# __init__() : 생성자 메서드, 클래스로 부터 새로운 객체(인스턴스)를 만들때 자동으로 호출되는 초기화 메서드.
# 객체가 처음 생성 될때 필요한 초기 변수들을 설정하기 위해 사용. 

# self : 객체 자신을 가리키는 파이썬의 매개변수. 클래스 사용해 객체 만들때 그 객체를 가리키는 참조값이 self가 됨. 
# ex ) QuizGame(quizzes, score_history) = self 