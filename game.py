# -*- coding: utf-8 -*-
"""
[파일 용도 설명]
이 파일(game.py)은 퀴즈 게임의 전체 흐름을 관장하는 'QuizGame' 클래스를 정의합니다.
보너스 과제 5종이 모두 통합 반영되었습니다:
 1) 랜덤 출제 (random 모듈 활용)
 2) 풀 문제 수 선택
 3) 힌트 기능 및 힌트 사용 시 점수 차감
 4) 퀴즈 삭제 기능 및 state.json 즉시 동기화
 5) 플레이 기록 히스토리 (datetime 날짜/시간, 문제수, 점수 보관)
"""

import json
import os
import random
from datetime import datetime
from quiz import Quiz
from default_data import get_default_quizzes

class QuizGame:
    """
    [클래스 역할]
    퀴즈 게임 전체의 상태(퀴즈 목록, 최고 점수, 플레이 히스토리)와 진행 로직을 담당하는 총괄 매니저 클래스입니다.
    """

    def __init__(self, state_file_path: str | None = None):
        """
        [생성자 메서드: __init__]
        - 왜 필요한가(Why): 게임을 시작할 때 데이터를 보관할 파일 경로를 지정하고, 
          기존에 저장된 퀴즈, 최고 점수, 플레이 기록을 불러와 초기화하기 위함입니다.
        - 어떻게 동작하는가(How): 경로가 주어지지 않으면 현재 실행 위치와 상관없이 프로젝트 폴더 내부의 'state.json'을 가리킵니다.
        """
        if state_file_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.state_file_path = os.path.join(base_dir, "state.json")
        else:
            self.state_file_path = state_file_path

        self.quizzes: list[Quiz] = []
        self.best_score: int = 0
        self.history: list[dict] = []  # [보너스 기능] 게임 플레이 히스토리 목록
        
        # 파일에서 데이터 불러오기
        self.load_data()

    def load_data(self) -> None:
        """
        [메서드: load_data]
        - 왜 필요한가(Why): 프로그램 재시작 시 퀴즈 목록, 최고 점수, 플레이 기록을 안전하게 복원하기 위함입니다.
        - 어떻게 동작하는가(How):
          1. 파일이 없으면 기본 퀴즈 5개로 초기 세팅하고 저장합니다.
          2. 파일이 깨졌거나 손상된 경우 try/except로 감지하여 기본 데이터로 자동 복구합니다.
          3. 정상 파일이면 퀴즈 목록, 최고 점수, 히스토리 리스트를 불러옵니다.
        """
        if not os.path.exists(self.state_file_path):
            print("📂 저장된 데이터 파일이 없어 기본 퀴즈 데이터로 시작합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            self.history = []
            self.save_data()
            return

        try:
            with open(self.state_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_quizzes = data.get("quizzes", [])
            self.quizzes = [Quiz.from_dict(q) for q in raw_quizzes]
            self.best_score = data.get("best_score", 0)
            self.history = data.get("history", [])

            # 퀴즈 목록이 비어있다면 최소 5개의 기본 퀴즈를 보장합니다.
            if not self.quizzes:
                self.quizzes = get_default_quizzes()
                self.save_data()

            print(f"📂 저장된 데이터를 성공적으로 불러왔습니다. (등록된 퀴즈 {len(self.quizzes)}개, 최고 기록 {self.best_score}점, 누적 기록 {len(self.history)}건)")

        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as e:
            print(f"⚠️ 경고: 데이터 파일({self.state_file_path})이 손상되었거나 올바르지 않습니다: {e}")
            print("🔄 안전을 위해 기본 퀴즈 데이터로 복구 및 초기화를 진행합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = 0
            self.history = []
            self.save_data()

    def save_data(self) -> None:
        """
        [메서드: save_data]
        - 왜 필요한가(Why): 퀴즈 추가/삭제, 점수 갱신, 플레이 기록 추가 시 변경사항을 영구 보존하기 위함입니다.
        - 어떻게 동작하는가(How):
          Quiz 객체들을 딕셔너리로 변환하고, 최고 점수 및 히스토리와 함께 state.json(UTF-8)으로 저장합니다.
        """
        payload = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "history": self.history
        }
        try:
            with open(self.state_file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"⚠️ 파일 저장 중 오류가 발생했습니다: {e}")

    def input_number(self, prompt: str, min_val: int, max_val: int) -> int:
        """
        [메서드: input_number (공통 숫자 입력 및 예외 검증)]
        - 왜 필요한가(Why): 문자가 섞이거나(abc), 엔터만 치거나, 범위 밖 숫자를 입력했을 때 비정상 종료를 방지하기 위함입니다.
        """
        while True:
            raw_input = input(prompt).strip()

            if not raw_input:
                print(f"⚠️ 입력을 하지 않았습니다. {min_val}~{max_val} 사이의 숫자를 입력해 주세요.")
                continue

            try:
                number = int(raw_input)
            except ValueError:
                print(f"⚠️ 잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue

            if not (min_val <= number <= max_val):
                print(f"⚠️ 잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue

            return number

    def input_non_empty_text(self, prompt: str) -> str:
        """
        [메서드: input_non_empty_text]
        - 왜 필요한가(Why): 문제나 보기가 빈 문자열(공백)로 등록되지 않도록 막기 위함입니다.
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
        - 메인 메뉴 화면을 콘솔에 출력합니다.
        """
        print("\n" + "=" * 42)
        print("         🎯 나만의 퀴즈 게임 🎯")
        print("=" * 42)
        print(" 1. 퀴즈 풀기 (랜덤 출제 / 문제수 선택 / 힌트)")
        print(" 2. 퀴즈 추가")
        print(" 3. 퀴즈 목록 보기")
        print(" 4. 퀴즈 삭제 (보너스 기능)")
        print(" 5. 점수 및 히스토리 확인 (보너스 기능)")
        print(" 6. 종료")
        print("=" * 42)

    def run(self) -> None:
        """
        [메서드: run]
        - 메인 제어 루프를 실행하여 사용자가 6번(종료)을 고를 때까지 반복합니다.
        """
        while True:
            self.display_menu()
            choice = self.input_number("선택 (1-6): ", 1, 6)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.delete_quiz()
            elif choice == 5:
                self.show_score()
            elif choice == 6:
                print("\n👋 퀴즈 게임을 종료합니다. 다음에 또 도전해 보세요!")
                break

    def play_quiz(self) -> None:
        """
        [메서드: play_quiz (보너스 기능 포함)]
        - 왜 필요한가(Why): 문제 수 선택, 랜덤 섞기, 힌트 열람 및 감점 처리, 플레이 히스토리 기록을 수행하기 위함입니다.
        - 어떻게 동작하는가(How):
          1. 등록된 퀴즈가 없으면 즉시 복귀합니다.
          2. 사용자가 몇 문제를 풀지(count) 선택합니다.
          3. random.sample()을 통해 퀴즈를 무작위로 섞어서 추출합니다.
          4. 0번 입력 시 힌트를 보여주며, 힌트를 사용한 문제는 배점의 50%만 부여(점수 차감)합니다.
          5. 최종 점수를 계산하고 datetime으로 날짜를 찍어 history 리스트에 추가 후 저장합니다.
        """
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 메뉴에서 퀴즈를 추가해 주세요!")
            return

        total_available = len(self.quizzes)
        print(f"\n현재 총 {total_available}개의 퀴즈가 등록되어 있습니다.")

        # [보너스 1] 문제 수 선택 기능
        question_count = self.input_number(
            f"풀고 싶은 문제 수를 입력하세요 (1~{total_available}): ", 1, total_available
        )

        # [보너스 2] 랜덤 출제 기능 (random.sample 활용)
        selected_quizzes = random.sample(self.quizzes, question_count)

        print(f"\n🎲 퀴즈 {question_count}문제를 무작위로 출제합니다! 시작합니다!")
        
        earned_points_total = 0.0
        correct_count = 0
        hints_used_count = 0
        point_per_question = 100.0 / question_count

        for idx, quiz in enumerate(selected_quizzes, start=1):
            quiz.display(question_number=idx)
            hint_viewed_this_question = False

            # [보너스 3] 힌트 기능 및 입력 루프
            while True:
                user_choice = self.input_number("정답 입력 (1-4, 0: 힌트보기): ", 0, len(quiz.choices))

                # 0을 입력하여 힌트를 요청한 경우
                if user_choice == 0:
                    if quiz.hint:
                        print(f"💡 [힌트]: {quiz.hint}")
                    else:
                        print("💡 [힌트]: 이 문제에는 등록된 힌트가 없습니다.")
                    
                    if not hint_viewed_this_question:
                        print("⚠️ (주의: 힌트를 확인하여 정답 시 50% 점수만 인정됩니다.)")
                        hint_viewed_this_question = True
                        hints_used_count += 1
                    continue
                else:
                    # 1~4번 정답을 선택한 경우
                    if quiz.is_correct(user_choice):
                        if hint_viewed_this_question:
                            print("✅ 정답입니다! (힌트 사용으로 절반 점수 획득)")
                            earned_points_total += (point_per_question * 0.5)
                        else:
                            print("✅ 정답입니다! (완전 득점)")
                            earned_points_total += point_per_question
                        correct_count += 1
                    else:
                        correct_text = quiz.choices[quiz.answer - 1]
                        print(f"❌ 틀렸습니다! 정답은 [{quiz.answer}번: {correct_text}] 입니다.")
                    break

        # 최종 점수 계산 (반올림하여 정수화)
        final_score = round(earned_points_total)

        print("\n" + "=" * 42)
        print(f"🏆 결과: {question_count}문제 중 {correct_count}문제 정답! (힌트 사용: {hints_used_count}회)")
        print(f"🎖️ 최종 획득 점수: {final_score}점 / 100점")

        # 최고 점수 갱신 확인
        if final_score > self.best_score:
            print(f"🎉 축하합니다! 새로운 최고 점수입니다! (기존: {self.best_score}점 ➔ 신규: {final_score}점)")
            self.best_score = final_score
        else:
            print(f"📊 역대 최고 기록은 {self.best_score}점입니다.")

        # [보너스 4] 플레이 기록 히스토리 저장 (날짜/시간, 문제 수, 정답 수, 점수)
        history_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": question_count,
            "correct_answers": correct_count,
            "hints_used": hints_used_count,
            "score": final_score
        }
        self.history.append(history_record)
        
        # 파일에 즉시 영구 저장
        self.save_data()
        print("=" * 42)

    def add_quiz(self) -> None:
        """
        [메서드: add_quiz]
        - 문제 지문, 4개 선택지, 정답 번호, 그리고 힌트를 입력받아 새 퀴즈를 생성하고 파일에 저장합니다.
        """
        print("\n" + "=" * 42)
        print("📌 새로운 퀴즈를 추가합니다.")
        print("=" * 42)

        question = self.input_non_empty_text("문제를 입력하세요: ")

        choices: list[str] = []
        for i in range(1, 5):
            choice = self.input_non_empty_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = self.input_number("정답 번호 (1-4): ", 1, 4)
        
        # 힌트 입력 받기 (생략 가능)
        hint = input("힌트를 입력하세요 (생략하려면 엔터): ").strip()

        new_quiz = Quiz(question=question, choices=choices, answer=answer, hint=hint)
        self.quizzes.append(new_quiz)
        self.save_data()

        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")
        print("=" * 42)

    def list_quizzes(self) -> None:
        """
        [메서드: list_quizzes]
        - 현재 등록된 모든 퀴즈 목록을 번호와 함께 출력합니다.
        """
        print("\n" + "=" * 42)
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("=" * 42)

        if not self.quizzes:
            print("현재 등록된 퀴즈가 없습니다. 퀴즈를 추가해 보세요!")
            print("=" * 42)
            return

        for idx, quiz in enumerate(self.quizzes, start=1):
            hint_str = f" [💡힌트: {quiz.hint}]" if quiz.hint else ""
            print(f"[{idx}] {quiz.question}{hint_str}")
        print("=" * 42)

    def delete_quiz(self) -> None:
        """
        [메서드: delete_quiz (보너스 기능)]
        - 왜 필요한가(Why): 잘못 등록된 퀴즈나 원치 않는 퀴즈를 삭제하고 파일에 반영하기 위함입니다.
        - 어떻게 동작하는가(How):
          1. 퀴즈가 1개 이하일 경우 게임 유지를 위해 삭제를 차단합니다.
          2. 현재 퀴즈 목록을 보여주고 삭제할 번호를 입력받습니다.
          3. '정말 삭제하시겠습니까?' 2차 확인 후 pop() 메서드로 리스트에서 제거하고 state.json에 저장합니다.
        """
        print("\n" + "=" * 42)
        print("🗑️ 퀴즈 삭제")
        print("=" * 42)

        if len(self.quizzes) <= 1:
            print("⚠️ 최소 1개 이상의 퀴즈가 유지되어야 하므로 삭제할 수 없습니다.")
            print("=" * 42)
            return

        # 삭제를 돕기 위해 현재 목록 출력
        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f" [{idx}] {quiz.question}")
        print("-" * 42)

        target_idx = self.input_number(f"삭제할 퀴즈 번호를 선택하세요 (1~{len(self.quizzes)}): ", 1, len(self.quizzes))

        # 실수 방지를 위한 삭제 확인 절차
        print(f"\n선택한 문제: '{self.quizzes[target_idx - 1].question}'")
        confirm = self.input_number("정말 삭제하시겠습니까? (1: 예, 삭제함 / 2: 아니오, 취소): ", 1, 2)

        if confirm == 1:
            # pop(index) 메서드는 리스트에서 특정 위치의 항목을 꺼내어 제거합니다.
            deleted_quiz = self.quizzes.pop(target_idx - 1)
            self.save_data()
            print(f"\n✅ [{target_idx}번] 퀴즈가 삭제되었습니다.")
        else:
            print("\n❌ 삭제가 취소되었습니다.")
        print("=" * 42)

    def show_score(self) -> None:
        """
        [메서드: show_score (보너스 기능 포함)]
        - 최고 점수뿐만 아니라 날짜/시간별 모든 플레이 기록 히스토리를 테이블 형식으로 출력합니다.
        """
        print("\n" + "=" * 42)
        print("🏆 점수 및 플레이 히스토리 기록")
        print("=" * 42)

        if self.best_score == 0 and not self.history:
            print("아직 퀴즈를 완료한 기록이 없습니다. 먼저 [1. 퀴즈 풀기]에 도전해 보세요!")
            print("=" * 42)
            return

        print(f"🌟 역대 최고 점수: [{self.best_score}점]\n")

        print("📜 최근 플레이 기록 히스토리:")
        print("-" * 50)
        # enumerate로 최근 기록부터 차례대로 출력
        for idx, rec in enumerate(self.history, start=1):
            ts = rec.get("timestamp", "-")
            total = rec.get("total_questions", 0)
            correct = rec.get("correct_answers", 0)
            hints = rec.get("hints_used", 0)
            sc = rec.get("score", 0)
            print(f" [{idx}] 일시: {ts} | {total}문제 중 {correct}문제 정답 (힌트 {hints}회) ➔ {sc}점")
        print("-" * 50)
        print("=" * 42)
