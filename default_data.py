# -*- coding: utf-8 -*-
"""
[파일 용도 설명]
이 파일(default_data.py)은 프로그램 최초 실행 시 제공할 기본 퀴즈 5종 시드 데이터를 정의합니다.
이번 버전에서는 '파이썬 첫걸음' 학습자 수준에 맞는 아주 기초적인 Python 입문 문제 5개를 제공합니다.
보너스 과제 요구사항에 맞춰 각 퀴즈마다 '힌트(hint)' 내용도 함께 포함되어 있습니다.
"""


from quiz import Quiz

def get_default_quizzes() -> list[Quiz]:
    """
    [함수 역할]
    '파이썬 첫걸음' 학습자용 기초 문제 5개를 힌트와 함께 Quiz 인스턴스 리스트로 생성합니다.
    문제 주제는 print, 변수, 자료형, 리스트, 반복문처럼 입문자가 가장 먼저 배우는 핵심 개념들로 구성했습니다.
    """

    return [
                Quiz(
            question="파이썬에서 화면에 문장을 출력할 때 사용하는 함수는 무엇일까요?",
            choices=[
                "input()",
                "print()",
                "len()",
                "range()"
            ],
            answer=2,
            hint="괄호 안의 내용을 터미널에 보여주는 가장 대표적인 출력 함수입니다."
        ),
        Quiz(
            question="다음 중 변수에 숫자 10을 저장하는 올바른 코드는 무엇일까요?",
            choices=[
                "10 = x",
                "x == 10",
                "x = 10",
                "x :=: 10"
            ],
            answer=3,
            hint="파이썬에서 변수에 값을 넣을 때는 '=' 기호를 사용합니다. 왼쪽은 변수 이름, 오른쪽은 값입니다."
        ),
        Quiz(
            question="다음 중 문자열(String) 데이터는 무엇일까요?",
            choices=[
                "123",
                "3.14",
                "True",
                "\"안녕하세요\""
            ],
            answer=4,
            hint="문자열은 보통 따옴표(작은따옴표 또는 큰따옴표)로 감싸서 표현합니다."
        ),
        Quiz(
            question="여러 값을 순서대로 저장할 때 자주 사용하는 파이썬 자료형은 무엇일까요?",
            choices=[
                "list",
                "int",
                "float",
                "bool"
            ],
            answer=1,
            hint="대괄호 [ ] 를 사용해서 만들며, 여러 값을 한 번에 담을 수 있습니다."
        ),
        Quiz(
            question="for문에서 일정한 범위의 숫자를 만들 때 자주 사용하는 함수는 무엇일까요?",
            choices=[
                "type()",
                "range()",
                "print()",
                "str()"
            ],
            answer=2,
            hint="for i in ___(5): 처럼 많이 사용합니다."
        )

    ]
