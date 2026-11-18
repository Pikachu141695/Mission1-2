# -*- coding: utf-8 -*-
"""
[파일 용도 설명]
이 파일(default_data.py)은 프로그램 최초 실행 시(state.json 파일이 없을 때) 또는
기존 데이터 파일이 손상되었을 때 기본으로 제공할 5개 이상의 시드(기본) 퀴즈 데이터를 정의합니다.
실무에서도 데이터베이스가 비어있을 때 초기 데이터를 채워 넣는 '시드(Seed) 데이터' 방식을 자주 사용합니다.
"""

from quiz import Quiz

def get_default_quizzes() -> list[Quiz]:
    """
    [함수 역할]
    선정된 주제인 '흥미진진한 컴퓨터 & IT 상식' 퀴즈 5개를 Quiz 인스턴스 리스트로 생성하여 반환합니다.
    
    - 왜 필요한가(Why): 사용자가 퀴즈를 직접 추가하기 전에도 곧바로 게임을 플레이할 수 있도록 초기 퀴즈를 보장하기 위함입니다.
    - 어떻게 동작하는가(How): 각각의 문제, 4개 선택지, 1~4번 정답을 담아 Quiz 클래스로 객체화하고 리스트에 담아 반환합니다.
    """
    return [
        Quiz(
            question="컴퓨터의 두뇌에 해당하며 연산과 제어를 담당하는 핵심 부품(CPU)의 약자는?",
            choices=[
                "Central Processing Unit",
                "Computer Personal Unit",
                "Core Power Unit",
                "Control Program Unit"
            ],
            answer=1
        ),
        Quiz(
            question="파이썬(Python) 프로그래밍 언어의 이름은 어디에서 유래되었을까요?",
            choices=[
                "아프리카에 서식하는 거대한 비단뱀",
                "영국의 전설적인 코미디 쇼 '몬티 파이선 비행 서커스'",
                "그리스 신화에 등장하는 거대한 뱀 괴물",
                "창시자 귀도 반 로섬이 기르던 애완 앵무새"
            ],
            answer=2
        ),
        Quiz(
            question="웹 브라우저와 웹 서버 간 데이터를 안전하게 암호화하여 통신하는 프로토콜은?",
            choices=[
                "HTTP (HyperText Transfer Protocol)",
                "FTP (File Transfer Protocol)",
                "HTTPS (HyperText Transfer Protocol Secure)",
                "SMTP (Simple Mail Transfer Protocol)"
            ],
            answer=3
        ),
        Quiz(
            question="인터넷 웹사이트 주소(URL) 앞에 붙는 'www'의 약자는 무엇일까요?",
            choices=[
                "World Wide Web",
                "Wide World Web",
                "World Web Wireless",
                "Whole World Window"
            ],
            answer=1
        ),
        Quiz(
            question="소프트웨어 프로그램에서 논리적 오류(버그)를 찾아내고 수정하는 작업을 무엇이라고 할까요?",
            choices=[
                "리팩토링 (Refactoring)",
                "디버깅 (Debugging)",
                "컴파일 (Compiling)",
                "배포 (Deployment)"
            ],
            answer=2
        )
    ]
