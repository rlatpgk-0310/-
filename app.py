import pandas as pd
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="만나면 피해야 할 야생동물 가이드북",
    page_icon="🐾",
    layout="centered",
)

# 2. 야생동물 데이터베이스 (리스트 구조)
# 형식: [동물이름, 위험도(별점), 위험 이유, 기본 위험 점수, 대처 메시지, 긴급 연락처]
ANIMAL_DATA = [
    [
        "고양이",
        "⭐ (별 한 개)",
        "발톱에 긁히거나 물릴 수 있으나, 먼저 위협하지 않으면 공격하지 않습니다.",
        10,
        "길고양이는 먼저 건드리지 말고 조용히 지나가세요.",
        "120 (다산콜센터 / 지자체 동물보호센터)",
    ],
    [
        "강아지(들개)",
        "⭐⭐⭐ (별 세 개)",
        "주인 없이 무리 지어 다니는 들개는 영역 본능과 공격성이 매우 강합니다.",
        45,
        "들개를 마주쳤을 시 눈을 마주치지 말고 천천히 뒷걸음질 치세요.",
        "119 (소방서 구조대)",
    ],
    [
        "멧돼지",
        "⭐⭐⭐⭐ (별 네 개)",
        "시속 40km 이상의 빠른 돌진력과 날카로운 엄니를 지녀 부딪히면 치명적입니다.",
        75,
        "멧돼지를 마주쳤을 시 절대 등을 보이지 말고 바위나 나무 뒤로 숨으세요.",
        "119 (긴급구조) / 112",
    ],
    [
        "곰",
        "⭐⭐⭐⭐⭐ (별 다섯 개)",
        "인간의 배가 되는 몸무게와 3m에 육박하는 피지컬을 가진 곰은 맨손으로 절대 이길 수 없습니다.",
        80,
        "야생곰을 마주쳤을 시 즉각적인 도주(대피)가 필요합니다.",
        "119 (긴급구조) / 국립공원관리공단",
    ],
    [
        "코끼리",
        "⭐⭐⭐⭐⭐ (별 다섯 개)",
        "지구상 가장 큰 육상 동물로, 흥분하면 차량도 뒤집을 수 있는 괴력을 가졌습니다.",
        85,
        "코끼리를 마주쳤을 시 즉시 차량이나 튼튼한 건물 내부로 대피하세요.",
        "119 (긴급구조)",
    ],
]


# 3. 위험도 분석 함수 (def)
def analyze_wildlife_risk(animal_name: str, age: int) -> tuple:
    """
    선택한 야생동물 이름과 사용자 나이를 입력받아
    최종 위험도 점수, 대처 행동 요령, 신고처를 반환합니다.
    """
    base_score = 0
    action_msg = ""
    emergency_contact = ""

    # 반복문(for)을 통해 리스트에서 해당 동물 데이터 탐색
    for animal in ANIMAL_DATA:
        if animal[0] == animal_name:
            base_score = animal[3]
            action_msg = animal[4]
            emergency_contact = animal[5]
            break

    # 조건문(if-elif-else)을 통한 연령별 대처 능력 가중치 부여
    if age < 14 or age >= 65:
        age_weight = 15  # 어린이 및 노약자: 도주·방어 능력이 낮아 위험도 가산
        age_group = "어린이/노약자"
    elif 14 <= age <= 19:
        age_weight = 3   # 청소년: 성인 대비 소폭 가산 (예: 곰 80 + 3 = 83점)
        age_group = "청소년"
    else:
        age_weight = 0   # 성인: 기본 위험도 적용
        age_group = "성인"

    # 최종 점수는 최대 100점으로 제한
    final_score = min(100, base_score + age_weight)
    return final_score, age_weight, age_group, action_msg, emergency_contact


# 4. 웹 화면 UI 구성
def main():
    st.title("🐾 만나면 피해야 할 야생동물 가이드북")
    st.markdown("**개발자:** 10604 김세하 | **목적:** 야생동물 조우 시 맞춤형 위험도 및 대처 요령 안내")
    st.divider()

    # 입력 영역
    st.subheader("🔍 상황 입력")
    col1, col2 = st.columns([1, 1])

    with col1:
        animal_names = [item[0] for item in ANIMAL_DATA]
        selected_animal = st.selectbox("(1) 마주친 동물 선택:", animal_names, index=3)

    with col2:
        user_age = st.slider("(2) 사용자 나이 입력:", min_value=1, max_value=150, value=17)

    # 분석 실행 버튼
    if st.button("분석하기", type="primary", use_container_width=True):
        score, weight, group, message, contact = analyze_wildlife_risk(selected_animal, user_age)

        st.divider()
        st.subheader("📊 분석 결과")

        # (1) 텍스트 메시지 출력 (위험도 수준에 따라 경고창 색상 구분)
        if score >= 70:
            st.error(f'🚨 **행동 요령:** "{message}"')
        elif score >= 40:
            st.warning(f'⚠️ **행동 요령:** "{message}"')
        else:
            st.success(f'✅ **행동 요령:** "{message}"')
