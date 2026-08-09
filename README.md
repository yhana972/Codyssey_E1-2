# Python 터미널 퀴즈 게임

## 1. 프로젝트 소개

이 프로젝트는 Python 표준 라이브러리만 사용하여 만든 터미널 기반 퀴즈 게임이다. 사용자는 터미널 메뉴에서 퀴즈를 추가, 조회, 삭제하고, 등록된 퀴즈 중 일부를 랜덤으로 풀 수 있다.

게임 데이터는 `state.json` 파일에 저장되며, 프로그램을 다시 실행해도 퀴즈 목록과 점수 기록을 불러올 수 있도록 구현했다.

## 2. 프로젝트 목표

이 프로젝트는 Codyssey 과제 제출용으로, Python의 기본 문법과 객체 지향 구조를 사용해 작은 콘솔 프로그램을 완성하는 것을 목표로 한다.

- 클래스와 객체 사용
- 함수와 메서드 분리
- 리스트와 딕셔너리 활용
- 조건문과 반복문 활용
- 예외 처리
- JSON 파일 입출력
- 데이터 영속성 구현
- 역할별 클래스 분리
- Git 브랜치와 병합 실습

## 3. 실행 환경

저장소에서 확인한 실행 환경은 다음과 같다.

- Python 3.14.4에서 문법 검사 확인
- Python 표준 라이브러리만 사용
- WSL Ubuntu 환경에서 검증
- Git 사용

<!-- IMAGE: 개발 환경 설정 화면 (예: Python 버전, Git 설정, 터미널 또는 VSCode) -->

외부 패키지를 설치할 필요는 없다.

## 4. 프로젝트 구조

```text
.
├── main.py
├── quiz.py
├── quiz_game.py
├── console_ui.py
├── data_manager.py
├── state.json
├── docs/
│   └── images/
│       └── .gitkeep
├── src/
│   └── .gitkeep
├── .gitignore
└── README.md
```

현재 실제 소스 코드는 프로젝트 루트의 Python 파일들에 있다. `docs/images/`와 `src/` 폴더에는 `.gitkeep`만 존재한다.

<!-- IMAGE: 프로젝트 파일 구조 화면 -->

## 5. 클래스 구조와 역할

| 파일 | 클래스/함수 | 역할 |
| --- | --- | --- |
| `quiz.py` | `Quiz` | 퀴즈 한 문제의 데이터와 정답 판정을 담당 |
| `quiz_game.py` | `QuizGame` | 메뉴 실행, 퀴즈 추가/조회/삭제/풀이, 점수 기록 관리를 담당 |
| `console_ui.py` | `ConsoleUI` | 터미널 입력 검증과 화면 출력을 담당 |
| `data_manager.py` | `DataManager` | `state.json` 파일 저장과 불러오기를 담당 |
| `main.py` | `main()` | 객체를 생성하고 게임 실행과 종료 시 저장을 담당 |

### Quiz

`Quiz` 클래스는 퀴즈 한 문제를 표현한다.

- `question`: 문제 내용
- `choices`: 선택지 목록
- `answer`: 정답 번호
- `hint`: 힌트 문자열
- `is_correct()`: 사용자 답과 정답 비교
- `to_dict()`: JSON 저장 가능한 딕셔너리로 변환
- `from_dict()`: 딕셔너리 데이터를 `Quiz` 객체로 복원

### QuizGame

`QuizGame` 클래스는 게임 진행 로직을 담당한다.

- 메인 메뉴 반복 실행
- 퀴즈 추가
- 퀴즈 목록 출력
- 퀴즈 삭제
- 퀴즈 풀이
- 풀이할 문제 수 선택
- `random.sample()`을 사용한 랜덤 출제
- 힌트 사용 여부 처리
- 점수 계산
- 점수 기록 저장 및 조회

### ConsoleUI

`ConsoleUI` 클래스는 입력과 출력을 담당한다.

- 메인 메뉴 출력
- 퀴즈 문제와 선택지 출력
- 빈 문자열 입력 재입력
- 숫자가 아닌 값 재입력
- 허용 범위를 벗어난 숫자 재입력
- `y` 또는 `n` 입력 검증
- 점수 기록 출력

### DataManager

`DataManager` 클래스는 JSON 파일 입출력을 담당한다.

- `state.json` 존재 여부 확인
- 저장된 퀴즈 데이터를 `Quiz` 객체 목록으로 복원
- 점수 기록 불러오기
- UTF-8 JSON 저장
- `ensure_ascii=False`로 한글이 읽히는 형태로 저장
- `indent=2`로 JSON을 보기 좋게 저장
- `state.json.tmp` 임시 파일에 먼저 저장한 뒤 성공하면 원본 파일로 교체
- 파일 없음, JSON 손상, 잘못된 키 구조 처리

### main

`main.py`는 프로그램의 진입점이다.

- `DataManager("state.json")` 생성
- 저장 데이터 불러오기
- `ConsoleUI` 생성
- `QuizGame` 생성
- `game.run()` 실행
- `KeyboardInterrupt`, `EOFError` 발생 시 안전 종료
- 종료 시 `data_manager.save()`로 데이터 저장
- `SIGTSTP`가 있는 환경에서는 `Ctrl+Z` 정지 신호를 무시하도록 설정

## 6. 주요 기능

실제 코드 기준 구현 기능은 다음과 같다.

- [x] 메인 메뉴 출력
- [x] 퀴즈 추가
- [x] 퀴즈 목록 조회
- [x] 퀴즈 삭제
- [x] 퀴즈 풀이
- [x] 정답 판정
- [x] 오답 시 정답 선택지 표시
- [x] 풀이할 문제 수 선택
- [x] `random.sample()` 기반 랜덤 출제
- [x] 힌트 보기
- [x] 힌트 사용 시 점수 50% 감점
- [x] 100점 만점 점수 계산
- [x] 전체 게임 점수 기록
- [x] 플레이 날짜/시간 기록
- [x] JSON 데이터 저장
- [x] 프로그램 재실행 후 데이터 복원
- [x] `Ctrl+C`, `Ctrl+D` 안전 종료
- [x] `Ctrl+Z` 정지 신호 무시 처리

## 7. 게임 진행 방식

프로그램을 실행하면 다음 메뉴가 반복해서 출력된다.

```text
=== 메인 메뉴 ===
1. 퀴즈 추가
2. 퀴즈 목록
3. 퀴즈 삭제
4. 퀴즈 풀기
5. 점수 기록
0. 종료
================
```

<!-- IMAGE: 프로그램 실행 후 메인 메뉴 화면 -->

퀴즈 풀기를 선택하면 현재 등록된 전체 문제 수 안에서 몇 문제를 풀지 입력한다. 입력한 문제 수만큼 퀴즈가 랜덤으로 선택되어 출제된다.

<!-- IMAGE: 풀이할 문제 수 선택 및 랜덤 출제 화면 -->

문제에 힌트가 있으면 힌트를 볼지 선택할 수 있다. 힌트를 사용한 뒤 정답을 맞히면 해당 문제 배점의 절반만 획득한다.

<!-- IMAGE: 퀴즈 풀이 및 힌트 사용 화면 -->

## 8. 점수 계산 방식

점수는 전체 게임 기준 100점 만점으로 계산한다.

```text
문제당 배점 = 100 / 선택한 문제 수
```

| 결과 | 획득 점수 |
| --- | --- |
| 힌트 없이 정답 | 해당 문제 배점 100% |
| 힌트 사용 후 정답 | 해당 문제 배점 50% |
| 오답 | 0점 |

최종 점수는 소수점 첫째 자리까지 출력하고, 점수 기록에는 `round(earned_score, 1)` 값으로 저장한다.

<!-- IMAGE: 최종 점수 결과 화면 -->

## 9. 데이터 저장 구조

게임 데이터는 `state.json`에 저장된다. 실제 저장 구조는 다음과 같다.

```json
{
  "quizzes": [
    {
      "question": "문제 내용",
      "choices": [
        "선택지 1",
        "선택지 2",
        "선택지 3",
        "선택지 4"
      ],
      "answer": 2,
      "hint": ""
    }
  ],
  "score_history": [
    {
      "played_at": "2026-08-09 19:00:00",
      "question_count": 5,
      "correct_count": 4,
      "hint_count": 1,
      "score": 70.0
    }
  ]
}
```

현재 저장소의 `state.json`에는 기본 퀴즈 6개와 빈 점수 기록이 저장되어 있다.

<!-- IMAGE: state.json 저장 데이터 화면 -->

### 기본 데이터 정책

`DataManager.load()` 기준 기본 데이터 정책은 다음과 같다.

- `state.json` 파일이 없으면 기본 퀴즈 6개와 빈 점수 기록으로 시작
- `state.json`이 비어 있거나 JSON 문법이 손상되면 기본 퀴즈 6개와 빈 점수 기록으로 시작
- `state.json` 내부에 필요한 키가 없으면 기본 퀴즈 6개와 빈 점수 기록으로 시작
- 정상 JSON에서 `quizzes`가 빈 리스트라면, 사용자가 모든 퀴즈를 삭제한 정상 상태로 보고 빈 목록을 유지

## 10. 예외 처리 및 데이터 보호

입력 검증은 `ConsoleUI`에서 처리한다.

- 빈 문자열 입력 시 다시 입력 요청
- 숫자가 아닌 값 입력 시 다시 입력 요청
- 허용 범위를 벗어난 숫자 입력 시 다시 입력 요청
- `y`, `n`이 아닌 값 입력 시 다시 입력 요청

<!-- IMAGE: 잘못된 입력 처리 화면 -->

파일 처리 예외는 `DataManager`에서 처리한다.

- `FileNotFoundError`: 기본 데이터 사용
- `json.JSONDecodeError`: 기본 데이터 사용
- `KeyError`: 기본 데이터 사용
- 저장 중 `OSError`: 오류 메시지 출력 후 임시 파일 정리

프로그램 종료 예외는 `main.py`에서 처리한다.

- `KeyboardInterrupt`: `Ctrl+C` 입력 시 안전 종료
- `EOFError`: `Ctrl+D` 입력 시 안전 종료
- `SIGTSTP`: 지원되는 환경에서 `Ctrl+Z`로 프로그램이 정지되지 않도록 무시

<!-- IMAGE: Ctrl+C, Ctrl+D 또는 Ctrl+Z 안전 종료 처리 화면 -->

### 안전한 저장 방식

`DataManager.save()`는 데이터를 바로 `state.json`에 쓰지 않고, 먼저 `state.json.tmp`에 저장한다. 임시 파일 저장이 성공하면 `state.json`으로 교체한다.

이 방식은 저장 중 오류가 발생했을 때 기존 `state.json`이 중간에 깨지는 위험을 줄이기 위한 것이다. `.gitignore`에는 `state.json.tmp`가 포함되어 있어 임시 파일이 Git에 포함되지 않도록 했다.

## 11. 실행 방법

WSL 또는 Linux 계열 터미널에서 프로젝트 루트로 이동한 뒤 실행한다.

```bash
python3 main.py
```

Windows PowerShell에서는 `python3` 명령이 환경에 따라 다르게 동작할 수 있으므로, 이 저장소에서는 WSL Ubuntu에서 실행을 확인했다.

## 12. 테스트 및 검증 방법

문법 검사는 다음 명령으로 수행했다.

```bash
python3 -m py_compile main.py quiz.py quiz_game.py console_ui.py data_manager.py
```

검증 결과:

- WSL Ubuntu의 Python 3.14.4에서 `py_compile` 통과
- 현재 코드 기준 외부 패키지 설치 불필요
- `docs/images/`에는 실제 이미지 파일이 없어 README 이미지 링크는 추가하지 않음

<!-- IMAGE: 문법 검사 실행 결과 화면 -->

## 13. Git 브랜치 및 협업 실습

이 프로젝트는 Git 브랜치를 사용해 기능을 나누어 개발하고 `main`으로 병합한 기록이 있다.

확인된 브랜치:

- `main`
- `feature/game`
- `refactor`
- `origin/feature/data`
- `origin/feature/game`
- `origin/feature/quiz`
- `origin/refactor`
- `origin/main`

확인된 병합 기록:

- `Merge : 퀴즈 기능을 main에 반영`
- `Merge:코드 구조 정리를 main에 반영`

최근 Git 로그 기준으로 의미 있는 커밋은 10개 이상 확인된다. 주요 작업 흐름은 다음과 같다.

- 초기 프로젝트 구조 생성
- `main.py` 기본 구조 작성
- `Quiz` 모델 구현
- JSON 데이터 변환 기능 추가
- 기본 퀴즈와 데이터 불러오기 추가
- 데이터 저장 기능 추가
- 입력/출력, 게임 진행, 데이터 관리 파일 분리
- 퀴즈 추가/목록/삭제 기능 추가
- 퀴즈 풀이와 점수 계산 추가
- 랜덤 출제, 힌트, 점수 기록 기능 추가
- 전체 실행 테스트 이슈 수정
- `Ctrl+Z` 처리 추가

실습에 사용한 주요 Git 명령은 다음과 같다.

```bash
git init
git add
git commit
git push
git pull
git switch
git checkout
git merge
git clone
```

<!-- IMAGE: git log --oneline --graph 실행 결과 화면 -->

## 14. 실행 결과

`docs/images/` 폴더는 존재하지만 현재 실제 실행 화면 이미지 파일은 없다. 이미지가 추가되면 아래 항목에 연결할 수 있다.

<!-- IMAGE: 퀴즈 추가 실행 화면 -->
<!-- IMAGE: 퀴즈 목록 실행 화면 -->
<!-- IMAGE: 퀴즈 삭제 실행 화면 -->
<!-- IMAGE: 퀴즈 풀이 실행 화면 -->
<!-- IMAGE: 최종 점수 실행 화면 -->
<!-- IMAGE: 점수 기록 조회 화면 -->
<!-- IMAGE: 프로그램 재실행 후 데이터 복원 확인 화면 -->
<!-- IMAGE: state.json 저장 화면 -->
<!-- IMAGE: Git 로그 화면 -->

## 15. 프로젝트를 통해 학습한 내용

이 프로젝트를 통해 Python 콘솔 프로그램을 역할별 클래스로 나누어 구성하는 방법을 연습했다.

- `Quiz`는 한 문제의 데이터와 정답 판정을 담당하도록 분리했다.
- `QuizGame`은 전체 게임 흐름과 점수 계산을 담당하도록 분리했다.
- `ConsoleUI`는 입력 검증과 출력만 담당하도록 분리했다.
- `DataManager`는 JSON 저장과 불러오기를 담당하도록 분리했다.
- `main.py`는 객체를 연결하고 종료 시 데이터를 저장하는 진입점 역할만 담당하도록 구성했다.

또한 JSON 파일을 사용해 프로그램 종료 후에도 데이터를 유지하는 방법과, Git 브랜치를 사용해 기능 개발 후 병합하는 흐름을 실습했다.

