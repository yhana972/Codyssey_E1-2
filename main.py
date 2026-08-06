import json
from pathlib import Path

class Quiz:
    """
    Quiz 클래스는 퀴즈 한 문제의 데이터와 정답 판정을 담당.
    문제 내용, 선택지 목록, 정답 번호, 사용자 답안 판정 
    """
    def __init__(self, question:str, choices: list[str], answer : int):
        self.question = question
        self.choices = choices
        self.answer = answer

    
    def is_correct(self, user_answer: int) -> bool:
        """사용자 입력 값과 정답을 비교하여 bool 타입으로 반환."""
        if self.answer == user_answer :
            return True
        else:
            return False


    def to_dict(self) -> dict:
        """Quiz 객체를 JSON 저장이 가능한 딕셔너리로 변환."""
        return {
            "question" : self.question,
            "choices" : self.choices,
            "answer" : self.answer
        }

    @classmethod
    def from_dict(cls, data:dict) -> "Quiz":
        """
        딕셔너리 데이터를 Quiz 객체로 반환. 
        cls : 현재 클래스 자체
        """
        return cls(
            question=data['question'],
            choices=data['choices'],
            answer=data['answer']
        )


class DataManager:
    """
    게임 데이터를 파일에서 읽고 파일로 저장함.
    """
    def __init__(self, file_path:str):
        self.file_path = Path(file_path)

    def load(self):
        """
        퀴즈 목록/ 점수 기록을 불러오기
        state.json 있음 -> 읽기 -> Quiz 객체 목록 생성 -> 퀴즈 목록과 점수 기록 반환
        state.json 없음 -> 기본 데이터 반환 (get_default_data)
        """

        if not self.file_path.exists(): #False
            print("저장된 퀴즈가 없어 기본 퀴즈로 시작합니다. 퀴즈를 추가해주세요!")
            return self.get_default_data()

        try:
            with self.file_path.open(mode="r", encoding="utf-8") as file:
                    data= json.load(file) #json 내용이 딕셔너리로 변환됨. 
        except json.JSONDecodeError:
            print("저장파일이 비어 있거나 손상되어 기본 퀴즈로 시작합니다.")
            return self.get_default_data()
        
        quizzes = [ Quiz.from_dict(quiz_data) for quiz_data in data["quizzes"] ]
        # 아래 코드와 같음.
        # for quiz_data in data["quizzes"]: 
        #   quizzes.add(Quiz.from_dict(quiz_data))
                
        score_history = data["score_history"]    
            
        return quizzes, score_history # 퀴즈 목록, 점수 히스토리

    def save(self, quizzes, score_history):
        """퀴즈 목록/ 점수 기록을 저장"""
        pass

    def get_default_data(self)->tuple[list[Quiz], list[dict]]:
        """저장 파일이 없을 때 사용할 기본 데이터 반환."""
        #기본 퀴즈 객체 목록 만들기
        default_quizzes = [
            Quiz(
                question="다음 중 빅데이터 분석 방법론 중\n 서로 피드백을 주고 받을 수 있는 단계로\n 바르게 연결된 것은 무엇인가?",
                choices=[
                    "분석 기획 - 데이터 분석",
                    "데이터 준비 - 데이터 분석",
                    "데이터 분석 - 시스템 구현",
                    "시스템 구현 - 평가 및 전개"
                ],
                answer=2
            ),
        ]
        #빈 점수 기록 목록과 함께 반환
        return default_quizzes, []


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


#파이썬 표준 라이브러리
# 파이썬에서 파일이나 폴더의 경로(path)를 다루기 위해 제공되는 모듈
# 기존 파이썬에선 파일 경로를 다룰 때 문자열로 다루었음, pathlib은 경로 자체를 하나의 객체로 다룸. 
# 장점 : 기존은 윈도우(\)와 맥/리눅스(/) 경로 구분자가 달라 오류가 났음. pathlib 쓰면 파이썬이 알아서
# 실행환경에 맞게 경로를 올바르게 처리함. 

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

# @classmethod :  클래스 메서드 장식자. 클래스에 직접 작동하는 기능임을 알려줌. classmethod는 객체 만들기 전에도 클래스 이름으로 바로 호출해서 사용 가능한 기능. 
# 일반 메서드: 이미 만들어진 quiz 객체가 호출
#quiz = Quiz(...)
#quiz.show_answer() 
# 클래스 메서드: 객체 생성 없이 Quiz 클래스가 직접 호출
#new_quiz = Quiz.from_dict(data)

# cls : 자기 자신 클래스 의미. 클래스 자신을 가리키기 위함. 
# 왜 클래스명으로 직접 안쓰고 cls로 쓰는가? 상속때문. 
# 만약 Quiz를 상속받은 MultipleChoiceQuiz(객관식 퀴즈)라는 자식 클래스가 있다고 가정. 
# Quiz 대신 cls를 쓰면, 상속받은 자식 클래스에서 이 메서드를 실행했을 때 자동으로 자식 클래스의 객체를 생성해주므로 코드의 재사용성이 훨씬 높아짐.

# -> "Quiz" : Quiz 객체가 결과로 나온다는 표시. 
# -> "Quiz" vs -> Quiz 차이는? 이썬이 코드를 읽는 순서(타임라인) 때문에 발생.
# -> Quiz (에러 발생 가능): def from_dict(...)를 정의하는 시점에는 아직 Quiz라는 클래스의 정의가 완전히 끝나지 않은 상태. 따라서 파이썬은 "Quiz 뭐임?"라며 NameError를 발생시킬 수 있음.
#-> "Quiz" (안전함): 따옴표를 붙여 문자열(Type Hint String)로 적어두면, 파이썬에게 "지금은 문자로 써두지만, 나중에 이 클래스 정의 끝나면 Quiz 타입으로 해석해 줘"라고 알려주는 것. (이를 Forward Reference/선행 참조라 부름.)
# 파이썬 3.7 이상에서 코드 맨 위에 from __future__ import annotations를 추가하면 따옴표 없이 -> Quiz라고 적어도 에러가 나지 않음.

# return cls {...} : 클래스 객체를 생성해서 반환. 
# Json 파일은 딕셔너리 형태로 데이터를 넘겨줌. 그럼 Quiz 객체에 딕셔너리 키 값을 직접 지정해서 생성해도 되지 않나? 가능은 함.
# 딕셔너리 형태에서 객체 형태로 변환해주는 메서드는 직관적으로 변환해주어 사용할뿐.
# 도우미 함수(from_dict)를 만드는 이유 (안 쓸 때와의 차이) : 가장 큰 차이는 '코드의 중복 제거'와 '유지보수성'
# 도우미 함수 안 쓸때 : 코드 곳곳에 d1['딕셔너리키 명']으로 사용하여 객체를 여러개 반복해서 써야함. 딕셔너리 키 명이 변경될때 그 코드들 일일히 다 바꿔줘야함.
# 도우미 함수 쓸때 : 코드 가독성이 좋아짐.(반복 작성X), 딕셔너리 구조가 변경되도 함수에서 수정하면 나머지 전체 수정 안해도 됨. 

# .open(mode="r", encoding="utf-8") as file:
# mode="r" : 파일 읽기 모드, encoding="utf-8" : 한글이 깨지지 않도록 utf-8 사용. with : 작업이 끝난 후 파일 자동 닫기.

# except json.JSONDecodeError: 아래 상황에서 오류를 처리함. 
# 파일이 비어있음, Json 문법이 잘못됨, 쉼표가 빠짐, 큰 따옴표가 잘못됨, 중괄호가 닫히지 않음. 