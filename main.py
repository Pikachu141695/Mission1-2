class Quiz:
    """퀴즈 하나하나의 정보를 담는 클래스"""
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class QuizGame:
    """게임의 전체 로직(메뉴, 실행 등)을 담당하는 클래스"""
    def __init__(self):
        self.quizzes = []  # 퀴즈 목록을 담을 리스트

    def display_menu(self):
        print("\n--- 퀴즈 게임 메뉴 ---")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 점수 확인")
        print("5. 종료")
        return input("번호를 선택하세요: ")

    def run(self):
        while True:
            choice = self.display_menu()
            if choice == '5':
                print("게임을 종료합니다.")
                break
            else:
                print(f"\n선택하신 {choice}번 기능은 아직 준비 중입니다!")

# 프로그램 시작점
if __name__ == "__main__":
    game = QuizGame()
    game.run()