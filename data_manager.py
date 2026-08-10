# data_manager.py

import json
from pathlib import Path
from quiz import Quiz


class DataManager:
    """
    게임 데이터를 파일에서 읽고 파일로 저장함.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(
        self,
    ) -> tuple[
        list[Quiz],
        list[dict],
        float,
        dict | None,
    ]:
        """
        퀴즈 목록, 점수 기록, 최고 점수, 최고 게임 기록을 불러온다.

        state.json 있음
        -> 읽기
        -> Quiz 객체 목록 생성
        -> 점수 기록 및 최고 기록 반환

        state.json 없음
        -> 기본 데이터 반환
        """

        if not self.file_path.exists():
            print(
                "저장된 퀴즈가 없어 기본 퀴즈로 시작합니다. "
                "퀴즈를 추가해주세요!"
            )
            return self.get_default_data()

        try:
            with self.file_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            # JSON의 퀴즈 딕셔너리를 Quiz 객체로 복원
            quizzes = [
                Quiz.from_dict(quiz_data)
                for quiz_data in data["quizzes"]
            ]

            # 전체 점수 기록 불러오기
            score_history = data["score_history"]

            # 추가:
            # 새 버전 state.json에 저장된 최고 점수와
            # 최고 게임 기록을 불러온다.
            #
            # 기존 state.json에는 해당 키가 없을 수 있으므로
            # [] 접근 대신 get()을 사용한다.
            saved_best_score = data.get(
                "best_score"
            )
            saved_best_game = data.get(
                "best_game"
            )

            # 추가:
            # best_score와 best_game이 정상적으로 저장되어 있다면
            # 저장된 값을 그대로 사용한다.
            if (
                isinstance(
                    saved_best_score,
                    (int, float),
                )
                and isinstance(
                    saved_best_game,
                    dict,
                )
            ):
                best_score = float(
                    saved_best_score
                )
                best_game = saved_best_game

            # 추가:
            # 예전 state.json처럼 best_score / best_game 필드가 없더라도
            # 기존 score_history가 있다면 그 안에서 최고 점수 기록을 찾는다.
            elif score_history:
                best_game = max(
                    score_history,
                    key=lambda record: record.get(
                        "score",
                        0,
                    ),
                )

                best_score = float(
                    best_game.get(
                        "score",
                        0.0,
                    )
                )

            # 게임을 한 번도 하지 않은 경우
            else:
                best_score = 0.0
                best_game = None

        except FileNotFoundError:
            print(
                "저장 파일이 존재하지 않습니다."
            )
            return self.get_default_data()

        except json.JSONDecodeError:
            print(
                "저장 파일이 비어 있거나 손상되어 "
                "기본 퀴즈로 시작합니다."
            )
            return self.get_default_data()

        except KeyError:
            print(
                "파일 내부 구조가 잘못 되어 "
                "기본 퀴즈로 시작합니다."
            )
            return self.get_default_data()

        return (
            quizzes,
            score_history,
            best_score,
            best_game,
        )

    def save(
        self,
        quizzes: list[Quiz],
        score_history: list[dict],
        best_score: float,
        best_game: dict | None,
    ) -> None:
        """
        퀴즈 목록, 점수 기록,
        최고 점수와 최고 게임 기록을 저장한다.
        """

        # Quiz 객체 목록을 딕셔너리 목록으로 변환
        quiz_data_list = [
            quiz.to_dict()
            for quiz in quizzes
        ]

        # 추가:
        # 기존 quizzes / score_history와 함께
        # 최고 점수와 최고 게임 기록도 별도 필드로 저장한다.
        #
        # 평가 항목에서 요구하는 최고점수 영속화를 위해
        # best_score를 state.json 최상위 필드로 저장한다.
        data = {
            "quizzes": quiz_data_list,
            "score_history": score_history,
            "best_score": best_score,
            "best_game": best_game,
        }

        # 저장 도중 문제가 생기는 상황에 대비하여
        # 실제 state.json에 바로 쓰지 않고 임시 파일에 먼저 저장한다.
        temp_path = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        try:
            # UTF-8 쓰기 모드로 임시 파일 열기
            with temp_path.open(
                mode="w",
                encoding="utf-8",
            ) as file:

                # 임시 파일에 JSON 저장
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2,
                )

            # 임시 파일 저장에 성공하면
            # 기존 state.json을 새 파일로 교체한다.
            temp_path.replace(
                self.file_path
            )

        except OSError as error:
            print(
                f"데이터를 저장하지 못했습니다. : {error}"
            )

            # 저장 실패 시 남아 있는 임시 파일 제거
            if temp_path.exists():
                temp_path.unlink()

    def get_default_data(
        self,
    ) -> tuple[
        list[Quiz],
        list[dict],
        float,
        dict | None,
    ]:
        """
        저장 파일이 없거나 손상되었을 때 사용할 기본 데이터를 반환한다.
        """

        # 기본 퀴즈 객체 목록
        default_quizzes = [
            Quiz(
                question=(
                    "다음 중 빅데이터 분석 방법론 중\n"
                    "서로 피드백을 주고 받을 수 있는 단계로\n"
                    "바르게 연결된 것은 무엇인가?"
                ),
                choices=[
                    "분석 기획 - 데이터 분석",
                    "데이터 준비 - 데이터 분석",
                    "데이터 분석 - 시스템 구현",
                    "시스템 구현 - 평가 및 전개",
                ],
                answer=2,
            ),
            Quiz(
                question=(
                    "다음 중 기업에 필요한 데이터, 인력, 조직, 분석업무 등이 "
                    "적용되지 않아\n"
                    "성숙된 분석 수준을 확보하기 위한 여러 방면에서\n"
                    "사전준비가 필요한 기업은 어느 유형인가?"
                ),
                choices=[
                    "확산형 기업",
                    "정착형 기업",
                    "도입형 기업",
                    "준비형 기업",
                ],
                answer=4,
            ),
            Quiz(
                question=(
                    "빅데이터 분석 방법론에서 예상되는 위험으로부터\n"
                    "대응하기 위한 방법이 아닌것은 무엇인가?"
                ),
                choices=[
                    "회피",
                    "수용",
                    "방관",
                    "완화",
                ],
                answer=3,
            ),
            Quiz(
                question=(
                    "다음 중에 데이터 거버넌스의 체계의 순서를\n"
                    "바르게 나열한 것은 무엇인가?"
                ),
                choices=[
                    (
                        "데이터 관리 체계 - 데이터 표준화 - "
                        "데이터 저장소 관리 - 표준화 활동"
                    ),
                    (
                        "데이터 표준화 - 데이터 관리 체계 - "
                        "데이터 저장소 관리 - 표준화 활동"
                    ),
                    (
                        "데이터 저장소 관리 - 데이터 표준화 - "
                        "표준화 활동 - 데이터 관리 체계"
                    ),
                    (
                        "표준화 활동 - 데이터 저장소 관리 - "
                        "데이터 관리 체계 - 데이터 표준화"
                    ),
                ],
                answer=2,
            ),
            Quiz(
                question=(
                    "다음 중 시계열 분석의 정상성 가정에 대한\n"
                    "설명으로 잘못된 것은 무엇인가?"
                ),
                choices=[
                    "모든 시점 t에 대해 일정한 평균을 갖는다.",
                    "모든 시점 t에 대해 일정한 분산을 갖는다.",
                    (
                        "공분산은 시점 t에 의존하고 "
                        "시차 l에 의존하지 않는다."
                    ),
                    (
                        "백색잡음은 정상성 가정을 만족하는 "
                        "대표적인 시계열 자료다."
                    ),
                ],
                answer=3,
            ),
            Quiz(
                question=(
                    "다음 중 이상값에 대한 설명으로 "
                    "잘못된 것은 무엇인가?"
                ),
                choices=[
                    (
                        "상자 그림과 IQR을 활용하여 "
                        "이상값을 판단할 수 있다."
                    ),
                    (
                        "ESD는 다중변수의 이상치를 "
                        "판단하는 데 유용하다."
                    ),
                    (
                        "이상값은 데이터 입력 과정에서 "
                        "발생할 수 있다."
                    ),
                    (
                        "IQR은 3분위수와 1분위수의 "
                        "차이를 의미한다."
                    ),
                ],
                answer=2,
            ),
        ]

        # 추가:
        # 기본 상태에서는 아직 플레이 기록이 없으므로
        # score_history = []
        # best_score = 0.0
        # best_game = None 으로 반환한다.
        return (
            default_quizzes,
            [],
            0.0,
            None,
        )