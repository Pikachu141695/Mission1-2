# -*- coding: utf-8 -*-
"""
[파일 용도 설명]
이 파일(quiz.py)은 개별 퀴즈 문제 1개를 객체(Object)로 표현하기 위한 'Quiz' 클래스를 정의합니다.
실무에서는 이처럼 프로그램에서 다루는 핵심 데이터 단위를 별도의 클래스(Model)로 분리하여 관리합니다.
이렇게 분리해두면 나중에 퀴즈 형식에 힌트나 해설이 추가되어도 이 파일만 수정하면 되므로 관리가 매우 쉬워집니다.
"""

class Quiz:
    """
    [클래스 역할]
    개별 퀴즈의 '문제', '4개의 선택지', '정답 번호'를 묶어서 관리하는 틀(붕어빵 틀)입니다.
    """

    def __init__(self, question: str, choices: list[str], answer: int):
        """
        [생성자 메서드: __init__]
        - 왜 필요한가(Why): 새 퀴즈 객체가 생성될 때 필수적인 정보(문제, 보기, 정답)를 초기 세팅하기 위해 호출됩니다.
        - 어떻게 동작하는가(How): self는 만들어진 자기 자신 객체를 가리키며, 전달받은 인자들을 self의 속성으로 저장합니다.
        
        :param question: 문제 지문 (예: "Python의 창시자는?")
        :param choices: 4개의 보기 목록 (예: ["Guido", "Linus", "Bjarne", "James"])
        :param answer: 정답 번호 (1부터 4 사이의 정수)
        """
        # 문제 지문을 속성에 저장합니다.
        self.question = question
        
        # 4개의 보기를 리스트 형태로 저장합니다.
        self.choices = choices
        
        # 정답 번호(1~4)를 정수 형태로 저장합니다.
        self.answer = answer

    def display(self, question_number: int | None = None) -> None:
        """
        [메서드: display]
        - 왜 필요한가(Why): 퀴즈 문제와 1~4번 선택지를 사용자가 읽기 좋은 형식으로 터미널 화면에 출력하기 위함입니다.
        - 어떻게 동작하는가(How): 문제 번호가 있으면 [문제 1] 형식으로 출력하고, for 반복문을 통해 보기 앞마다 1. 2. 번호를 붙여 출력합니다.
        
        :param question_number: 화면에 표시할 문제 번호 (생략 시 문제만 출력)
        """
        # 문제 번호가 전달되었으면 [문제 X] 헤더를 붙여서 출력합니다.
        if question_number is not None:
            print(f"\n[문제 {question_number}] {self.question}")
        else:
            print(f"\n[문제] {self.question}")

        print("-" * 40)
        
        # enumerate() 함수를 사용해 0부터 시작하는 인덱스(idx)와 보기 내용(choice)을 함께 가져옵니다.
        # 화면에는 사용자 친화적으로 1부터 보이도록 idx + 1을 표시합니다.
        for idx, choice in enumerate(self.choices):
            print(f"  {idx + 1}. {choice}")
        print("-" * 40)

    def is_correct(self, user_answer: int) -> bool:
        """
        [메서드: is_correct]
        - 왜 필요한가(Why): 사용자가 고른 답과 실제 정답이 일치하는지 판별하기 위함입니다.
        - 어떻게 동작하는가(How): 전달받은 user_answer 정수와 self.answer 정수가 같으면 True, 다르면 False를 반환합니다.
        
        :param user_answer: 사용자가 입력한 번호 (1~4)
        :return: 정답 여부 (참/거짓)
        """
        # 비교 연산자(==)를 사용하여 정답 번호가 같은지 검사합니다.
        return self.answer == user_answer

    def to_dict(self) -> dict:
        """
        [메서드: to_dict]
        - 왜 필요한가(Why): JSON 파일(state.json)로 저장하려면 Python 객체를 딕셔너리 형태로 변환(직렬화)해야 합니다.
        - 어떻게 동작하는가(How): question, choices, answer 키를 가진 표준 딕셔너리를 만들어 반환합니다.
        """
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """
        [클래스 메서드: from_dict]
        - 왜 필요한가(Why): JSON 파일에서 읽어온 딕셔너리 데이터를 다시 Quiz 클래스의 인스턴스로 복원(역직렬화)하기 위함입니다.
        - 어떻게 동작하는가(How): cls는 Quiz 클래스 자신을 의미하며, data 딕셔너리의 값들을 꺼내 새 Quiz 인스턴스를 생성해 반환합니다.
        
        :param data: question, choices, answer 키를 포함하는 딕셔너리
        :return: 복원된 Quiz 인스턴스
        """
        return cls(
            question=data.get("question", "제목 없는 문제"),
            choices=data.get("choices", ["보기1", "보기2", "보기3", "보기4"]),
            answer=data.get("answer", 1)
        )
