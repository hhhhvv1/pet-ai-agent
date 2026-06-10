import sqlite3
from openai import OpenAI

from memory import (
    get_recent_history,
    get_all_history,
    symptom_trend
)

from prompt_builder import build_prompt

from health_tools import (
    check_emergency,
    prevention_check,
    hospital_prepare,
    hospital_aftercare
)

from report import generate_health_report


client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

conn = sqlite3.connect("memory.db")
cursor = conn.cursor()


# -------------------------
# 반려동물 선택
# -------------------------

def select_pet():

    cursor.execute(
        "SELECT * FROM pets"
    )

    pets = cursor.fetchall()

    if len(pets) == 0:

        print("등록된 반려동물이 없습니다.")

        return None

    print("\n===== 반려동물 목록 =====\n")

    for i, pet in enumerate(pets):

        print(
            f"{i+1}. {pet[1]} ({pet[2]})"
        )

    choice = int(
        input("\n번호 선택: ")
    )

    return pets[choice-1]


# -------------------------
# 반려동물 등록
# -------------------------

def add_pet():

    print("\n===== 반려동물 등록 =====")

    name = input("이름: ")
    species = input("종류: ")
    age = int(input("나이: "))
    weight = float(input("체중: "))
    personality = input("성격: ")

    cursor.execute(
        """
        INSERT INTO pets(
            name,
            species,
            age,
            weight,
            personality
        )
        VALUES(?,?,?,?,?)
        """,
        (
            name,
            species,
            age,
            weight,
            personality
        )
    )

    conn.commit()

    print("\n등록 완료")


# -------------------------
# 결과 저장
# -------------------------

def save_result(
    pet_name,
    symptom,
    result,
    risk_score
):

    risk = "알 수 없음"

    if risk_score >= 80:

        risk = "높음"

    elif risk_score >= 50:

        risk = "중간"

    else:

        risk = "낮음"

    cursor.execute(
        """
        INSERT INTO health_logs(
            pet_name,
            symptom,
            analysis,
            risk,
            risk_score
        )
        VALUES(?,?,?,?,?)
        """,
        (
            pet_name,
            symptom,
            result,
            risk,
            risk_score
        )
    )

    conn.commit()


# -------------------------
# 위험도 계산
# -------------------------

def calculate_risk_score(result):

    result = result.lower()

    if "응급" in result:

        return 95

    if "즉시 병원" in result:

        return 90

    if "높음" in result:

        return 85

    if "중간" in result:

        return 60

    if "낮음" in result:

        return 20

    return 50


# -------------------------
# 메인 루프
# -------------------------

while True:

    print("\n========================")
    print("반려동물 AI 에이전트")
    print("========================")

    print("1. 건강 분석")
    print("2. 건강 기록 조회")
    print("3. 예방 건강 체크")
    print("4. 병원 방문 준비")
    print("5. 병원 방문 후 관리")
    print("6. 반려동물 추가")
    print("7. 건강 변화 추적")
    print("8. 종료")

    menu = input("\n선택: ")

    # -------------------------
    # 건강 분석
    # -------------------------

    if menu == "1":

        pet = select_pet()

        if pet is None:
            continue

        symptom = input(
            "\n증상 입력: "
        )

        if check_emergency(symptom):

            print(
                "\n🚨 응급상황 가능성"
            )

            print(
                "즉시 병원 방문 권장\n"
            )

        history = get_recent_history(
            pet[1]
        )

        prompt = build_prompt(
            pet,
            symptom,
            history
        )

        print("\nAI 분석 중...\n")

        response = client.chat.completions.create(
            model="gemma-3-4b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        result = (
            response
            .choices[0]
            .message.content
        )

        risk_score = calculate_risk_score(
            result
        )

        print("\n===== 분석 결과 =====\n")

        print(result)

        print(
            f"\n위험도 점수: {risk_score}/100"
        )

        save_result(
            pet[1],
            symptom,
            result,
            risk_score
        )

        pdf_file = generate_health_report(
            pet[1],
            symptom,
            result
        )

        print(
            f"\nPDF 생성 완료: {pdf_file}"
        )

    # -------------------------
    # 건강 기록 조회
    # -------------------------

    elif menu == "2":

        pet = select_pet()

        if pet is None:
            continue

        logs = get_all_history(
            pet[1]
        )

        print(
            "\n===== 건강 기록 =====\n"
        )

        print("선택된 반려동물:", pet[1])
        print("조회된 기록 수:", len(logs))

        if len(logs) == 0:

            print("저장된 건강 기록이 없습니다.")

        else :

            for log in logs:

                print(
                     f"""
날짜: {log[0]}
증상: {log[1]}
위험도: {log[2]}
"""
            )

            input("\엔터를 누르세요...")

    # -------------------------
    # 예방 건강 체크
    # -------------------------

    elif menu == "3":

        pet = select_pet()

        if pet is None:
            continue

        print("\n===== 예방 건강 체크 =====\n")

        appetite = input("식사는 정상인가요? (예/아니오): ")
        water = input("물을 잘 마시나요? (예/아니오): ")
        poop = input("배변 상태는 정상인가요? (예/아니오): ")
        walk = input("산책 또는 활동량은 충분한가요? (예/아니오): ")

        warning_count = 0

        if appetite == "아니오":
            warning_count += 1

        if water == "아니오":
            warning_count += 1
                
        if poop == "아니오":
            warning_count += 1

        if walk == "아니오":
            warning_count += 1

        print("\n===== 예방 체크 결과 =====\n")

        if warning_count == 0:

            print("현재 건강 상태는 양호해 보입니다.")

        elif warning_count <= 2:

            print("주의가 필요합니다.")
            print("며칠간 상태를 관찰해 주세요.")

        else:
            
            print("건강 이상 가능성이 있습니다.")
            print("동물병원 상담을 권장합니다.")

        input("\n엔터를 누르세요...")

    # -------------------------
    # 병원 방문 준비
    # -------------------------

    elif menu == "4":
         
         pet = select_pet()

         if pet is None:
             continue

         print("\n===== 병원 방문 준비 =====\n")

         start_date = input("증상이 언제 시작됐나요?: ")
         appetite = input("최근 식사는 정상인가요?: ")
         poop = input("배변 상태는 어떤가요?: ")
         medicine = input("복용 중인 약이 있나요?: ")
         history = input("과거 병력이 있나요?: ")

         print("\n===== 병원 제출용 요약 =====\n")

         print(f"증상 시작일: {start_date}")
         print(f"식사 상태: {appetite}")
         print(f"배변 상태: {poop}")
         print(f"복용 약: {medicine}")
         print(f"과거 병력: {history}")

         input("\n엔터를 누르세요...")

    # -------------------------
    # 병원 방문 후 관리
    # -------------------------

    elif menu == "5":
         
         pet = select_pet()

         if pet is None:
             continue

         print("\n===== 병원 방문 후 관리 =====\n")

         diagnosis = input("진단명을 입력하세요: ")
         medicine = input("처방약 이름: ")
         days = input("복용 기간(일): ")

         print("\n===== 관리 계획 =====\n")

         print(f"진단명: {diagnosis}")
         print(f"처방약: {medicine}")
         print(f"복용 기간: {days}일")

         print("\n관리 체크리스트")

         print("1. 정해진 시간에 약 복용")
         print("2. 식욕 변화 관찰")
         print("3. 배변 상태 확인")
         print("4. 활동량 확인")
         print("5. 증상 개선 여부 기록")

         input("\n엔터를 누르세요...")

    # -------------------------
    # 반려동물 추가
    # -------------------------

    elif menu == "6":

        add_pet()

    # -------------------------
    # 건강 변화 추적
    # -------------------------

    elif menu == "7":

        pet = select_pet()

        if pet is None:
             continue

        logs = symptom_trend(
             pet[1]
        )

        print("\n===== 건강 변화 추적 =====\n")

        if len(logs) == 0:

            print("건강 기록이 없습니다.")

        else:

            symptom_count = {}

            for log in logs:

                symptom = log[0]

                symptom_count[symptom] = (
                    symptom_count.get(symptom, 0) + 1
                )

                print(
                    f"""
날짜: {log[2]}
증상: {log[0]}
위험도: {log[1]}
"""
)

        print("\n===== 분석 결과 =====\n")

        repeated = False

        for symptom, count in symptom_count.items():

            if count >= 2:

                repeated = True

                print(
                    f"'{symptom}' 증상이 {count}회 반복되었습니다."
                )

        if not repeated:

            print(
                "최근 반복되는 증상은 없습니다."
            )

        input("\n엔터를 누르세요...")

    # -------------------------
    # 종료
    # -------------------------

    elif menu == "8":

        print("\n프로그램 종료")

        break

    else:

        print("\n잘못된 입력입니다.")