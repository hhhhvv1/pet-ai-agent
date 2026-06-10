EMERGENCY_KEYWORDS = [
    "경련",
    "의식 없음",
    "호흡곤란",
    "혈변",
    "피를 토함",
    "쓰러짐"
]

def check_emergency(symptom):

    for word in EMERGENCY_KEYWORDS:

        if word in symptom:
            return True

    return False


def prevention_check():

    return """
예방 건강 체크

1. 식사는 정상인가요?
2. 물은 잘 마시나요?
3. 배변 상태는 정상인가요?
4. 산책은 했나요?
5. 평소보다 무기력한가요?
"""


def hospital_prepare():

    return """
병원 방문 전 준비

1. 증상 시작 시점
2. 최근 식사 여부
3. 최근 배변 상태
4. 복용 중인 약
5. 과거 병력
"""


def hospital_aftercare():

    return """
병원 방문 후 관리

1. 처방약 복용 시간 기록
2. 식욕 변화 기록
3. 배변 상태 기록
4. 활동량 기록
5. 증상 개선 여부 확인
"""