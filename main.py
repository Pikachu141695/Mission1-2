# -*- coding: utf-8 -*-
"""
[파일 용도 설명]
이 파일(main.py)은 퀴즈 게임 프로그램의 '진입점(Entry Point)' 역할을 합니다.
파이썬 프로그램을 실행할 때 가장 먼저 호출되는 파일이며,
전체 게임 객체를 생성하고 예기치 못한 강제 종료 신호(Ctrl+C 등)로부터 안전하게 보호하는 방패 역할을 수행합니다.
"""

import sys
from game import QuizGame

def main() -> None:
    """
    [메인 함수: main]
    - 왜 필요한가(Why): 전역 영역(Global Scope)에 코드를 마구 작성하지 않고 함수로 묶어 관리하는 것이 실무 표준(Best Practice)입니다.
    - 어떻게 동작하는가(How):
      1. QuizGame 인스턴스를 생성합니다.
      2. try/except 블록 안에서 game.run()을 실행합니다.
      3. 사용자가 언제든 Ctrl+C(KeyboardInterrupt)를 누르거나 터미널 입력이 닫히면(EOFError)
         빨간색 에러 메시지(Traceback)가 뜨는 대신, 안전 안내 문구를 출력하고 저장 후 정상 종료합니다.
    """
    # state_file_path를 생략하면 프로젝트 폴더 기준의 state.json이 자동으로 적용됩니다.
    game = QuizGame()

    try:
        # 게임 메인 루프 실행
        game.run()

    except (KeyboardInterrupt, EOFError):
        # [예외 처리: 강제 중단 신호 감지]
        # 사용자가 Ctrl+C 또는 Ctrl+D/Z를 눌렀을 때 비정상 종료(Crash)를 방지합니다.
        print("\n\n⚠️ 사용자에 의해 프로그램이 강제 중단되었습니다.")
        print("💾 데이터를 안전하게 저장한 뒤 종료합니다...")
        game.save_data()
        print("👋 이용해 주셔서 감사합니다. 안녕히 가세요!")
        sys.exit(0)

# [진입점 조건문: __name__ == '__main__']
# - 왜 필요한가(Why): 이 파이썬 파일이 직접 실행되었을 때만 main()을 실행하고,
#   다른 파일에서 import 되었을 때는 자동으로 실행되지 않도록 방지하는 파이썬 고유의 관례입니다.
if __name__ == "__main__":
    main()
