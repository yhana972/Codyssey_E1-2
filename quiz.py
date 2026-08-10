# quiz.py


class Quiz:
    """
    Quiz 클래스는 퀴즈 한 문제의 데이터와 정답 판정을 담당.
    문제 내용, 선택지 목록, 정답 번호, 힌트, 사용자 답안 판정
    """

    def __init__(
        self,
        question: str,
        choices: list[str],
        answer: int,
        hint: str = "",
    ):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def is_correct(self, user_answer: int) -> bool:
        """사용자 입력 값과 정답을 비교하여 bool 타입으로 반환."""
        if self.answer == user_answer:
            return True
        else:
            return False

    def to_dict(self) -> dict:
        """Quiz 객체를 JSON 저장이 가능한 딕셔너리로 변환."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """
        딕셔너리 데이터를 Quiz 객체로 반환.
        cls : 현재 클래스 자체
        """

        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            # 기존 state.json에 hint가 없는 경우에도 오류가 발생하지 않도록
            # 빈 문자열을 기본값으로 사용한다.
            hint=data.get("hint", ""),
        )