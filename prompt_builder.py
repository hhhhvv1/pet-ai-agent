def build_prompt(
    pet,
    symptom,
    history
):

    history_text = ""

    for item in history:

        history_text += f"""
증상: {item[0]}
위험도: {item[1]}
"""

    return f"""
당신은 반려동물 헬스케어 AI 에이전트입니다.

반려동물 정보

이름: {pet[1]}
종류: {pet[2]}
나이: {pet[3]}
체중: {pet[4]}
성격: {pet[5]}

최근 건강 기록

{history_text}

현재 증상

{symptom}

다음 형식으로 답변하세요.

위험도:
위험점수:
증상분석:
권장행동:
"""