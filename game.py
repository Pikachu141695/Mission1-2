# -*- coding: utf-8 -*-
"""
[파일 용도 설명]
이 파일(game.py)은 퀴즈 게임의 전체 흐름을 관장하는 'QuizGame' 클래스를 정의합니다.
데이터 파일(state.json) 관리, 메뉴 표시, 사용자 입력 검증, 퀴즈 플레이, 퀴즈 추가,
목록 조회, 점수 확인 등 게임의 핵심 비즈니스 로직(Controller 역할)을 수행합니다.
"""

import json
import os
from quiz import Quiz
from default_data import get_default_quizzes

class QuizGame:
    """
    [클래스 역할]
    퀴즈 게임 전체의 상태(퀴즈 목록, 최고 점수)와 진행 로직을 담당하는 매니저 클래스입니다.
    """

    def __init__(self, state_file_path: str = "state.json"):
        """
        [생성자 메서드: __init__]
        - 왜 필요한가(Why): 게임을 시작할 때 데이터를 보관할 파일 경로를 지정하고, 
          기존에 저장된 퀴즈와 최고 점수를 불러와 준비하기 위함입니다.
        - 어떻게 동작하는가(How): state_file_path를 인자로 받아 저장하고, load_data()를 호출하여 초기 데이터를 채웁니다.
        """
        self.state_file_path = state_file_path
        self.quizzes: list[Quiz] = []
        self.best_score: int = 0
        
        # 게임 객체가 생성될 때 바로 저장된 파일에서 데이터를 불러옵니다.
        self.load_data()

    def load_data(self) -> None:
        """
        [메서드: load_data]
        - 왜 필요한가(Why): 프로그램 재시작 시 이전 데이터를 복원하기 위함입니다 (데이터 영속성).
        - 어떻게 동작하는가(How):
          1. state.json 파일이 없으면 기본 5개 퀴즈로 초기화하고 새 파일을 저장합니다.
          2. 파일이 존재하지만 내용이 깨졌거나(JSON 오류) 읽기 오류가 나면 try/except로 감지하여 기본 데이터로 자동 복구합니다.
          3. 파일이 정상적이면 JSON을 읽어 Quiz 객체 리스트와 최고 점수를 복원합니다.
        """
        # 1. 파일이 아예 존재하지 않는 첫 실행의 경우
        if not os.path.exists(self.state_file_path):
            print("📂 저장된 데이터 파일이 없어 기본 퀴즈 데이터로 시작합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            self.save_data()
            return

        # 2. 파일이 존재하는 경우 읽기 시도
        try:
            # UTF-8 인코딩으로 파일을 읽기 모드('r')로 안전하게 엽니다.
            with open(self.state_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # JSON에서 quizzes 리스트를 가져와 각 항목을 Quiz 객체로 변환합니다.
            raw_quizzes = data.get("quizzes", [])
            self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]
            self.best_score = data.get("best_score", 0)

            # 퀴즈 목록이 비어있다면 최소 5개의 기본 퀴즈를 보장합니다.
            if not self.quizzes:
                self.quizzes = get_default_quizzes()
                self.save_data()

            print(f"📂 저장된 데이터를 성공적으로 불러왔습니다. (등록된 퀴즈 {len(self.quizzes)}개, 최고 기록 {self.best_score}점)")

        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
            # 파일이 비정상적으로 깨졌거나 읽을 수 없는 경우 복구 로직
            print(f"⚠️ 경고: 데이터 파일({self.state_file_path})이 손상되었거나 올바르지 않습니다: {e}")
            print("🔄 안전을 위해 기본 퀴즈 데이터로 복구 및 초기화를 진행합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            self.save_data()

    def save_data(self) -> None:
        """
        [메서드: save_data]
        - 왜 필요한가(Why): 퀴즈가 추가되거나 최고 점수가 갱신되었을 때 변경사항을 영구 보존하기 위함입니다.
        - 어떻게 동작하는가(How):
          Quiz 객체들을 딕셔너리로 직렬화한 뒤, json.dump()를 사용해 UTF-8 형식의 state.json으로 저장합니다.
        """
        payload = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        try:
            with open(self.state_file_path, "w", encoding="utf-8") as f:
                # ensure_ascii=False로 한글이 깨지지 않고 온전히 저장되도록 하며, indent=4로 예쁘게 들여쓰기합니다.
                json.dump(payload, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {e}")

    def input_number(self, prompt: str, min_val: int, max_val: int) -> int:
        """
        [메서드: input_number (공통 입력 및 예외 검증)]
        - 왜 필요한가(Why): 사용자가 잘못된 값(문자열, 빈 엔터, 범위 밖 숫자)을 입력했을 때
          프로그램이 빨간색 에러를 내며 강제 종료되지 않고, 안내 메시지를 띄우며 다시 입력받기 위함입니다.
        - 어떻게 동작하는가(How):
          1. while True 무한 루프를 통해 올바른 숫자가 들어올 때까지 반복합니다.
          2. input()으로 받은 문자열의 앞뒤 공백을 strip()으로 제거합니다.
          3. 빈 입력("")인 경우 안내 메시지를 출력하고 다시 반복합니다.
          4. int() 변환을 시도하여 숫자가 아니면 ValueError를 잡아 안내 메시지를 출력합니다.
          5. 숫자가 min_val ~ max_val 범위에 속하는지 확인 후, 정상이면 해당 정수를 반환(return)합니다.
        
        :param prompt: 사용자에게 보여줄 입력 안내 문구
        :param min_val: 허용 가능한 최소 정수
        :param max_val: 허용 가능한 최대 정수
        :return: 유효성이 검증된 정수
        """
        while True:
            raw_input = input(prompt).strip()

            # 케이스 1: 아무것도 입력하지 않고 엔터만 친 경우
            if not raw_input:
                print(f"⚠️ 입력을 하지 않았습니다. {min_val}~{max_val} 사이의 숫자를 입력해 주세요.")
                continue

            # 케이스 2: 숫자로 변환 시도 (문자열이 섞여있으면 ValueError 발생)
            try:
                number = int(raw_input)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue

            # 케이스 3: 숫자는 맞으나 허용 범위 밖인 경우
            if not (min_val <= number <= max_val):
                print(f"⚠️ 잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue

            # 모든 유효성 검사를 통과한 정수 반환
            return number

    def input_non_empty_text(self, prompt: str) -> str:
        """
        [메서드: input_non_empty_text]
        - 왜 필요한가(Why): 새 퀴즈 추가 시 문제나 보기가 빈 문자열(공백)로 들어가지 않도록 검증하기 위함입니다.
        - 어떻게 동작하는가(How): strip()을 거친 후 비어있으면 경고를 출력하고 다시 입력을 받습니다.
        """
        while True:
            text = input(prompt).strip()
            if not text:
                print("⚠️ 공백은 허용되지 않습니다. 내용을 1자 이상 입력해 주세요.")
                continue
            return text

    def display_menu(self) -> None:
        """
        [메서드: display_menu]
        - 왜 필요한가(Why): 프로그램의 메인 화면에서 사용자가 선택할 수 있는 기능 목록을 일관되게 보여주기 위함입니다.
        - 어떻게 동작하는가(How): 콘솔 화면에 구분선과 1~5번 메뉴 항목을 깔끔하게 출력합니다.
        """
        print("\n" + "=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def run(self) -> None:
        """
        [메서드: run]
        - 왜 필요한가(Why): 프로그램의 메인 제어 루프(Main Loop)를 실행하여 사용자가 종료(5번)를 선택할 때까지 게임을 계속 유지하기 위함입니다.
        - 어떻게 동작하는가(How):
          1. while True 무한 루프 안에서 메뉴를 출력합니다.
          2. input_number()를 통해 1~5 사이의 검증된 번호를 입력받습니다.
          3. if/elif/else 분기를 통해 선택된 번호에 매칭되는 메서드를 호출합니다.
          4. 5번을 선택하면 break 문으로 루프를 탈출하여 게임을 안전하게 종료합니다.
        """
        while True:
            self.display_menu()
            choice = self.input_number("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("\n👋 퀴즈 게임을 종료합니다. 언제든 다시 도전해 보세요!")
                break

    def play_quiz(self) -> None:
        """(스텁) 퀴즈 풀기 기능 - 브랜치 작업 예정"""
        print("\n[알림] 퀴즈 풀기 기능을 준비 중입니다.")

    def add_quiz(self) -> None:
        """(스텁) 퀴즈 추가 기능 - 후속 작업 예정"""
        print("\n[알림] 퀴즈 추가 기능을 준비 중입니다.")

    def list_quizzes(self) -> None:
        """(스텁) 퀴즈 목록 보기 기능 - 후속 작업 예정"""
        print("\n[알림] 퀴즈 목록 기능을 준비 중입니다.")

    def show_score(self) -> None:
        """(스텁) 최고 점수 확인 기능 - 후속 작업 예정"""
        print("\n[알림] 점수 확인 기능을 준비 중입니다.")


