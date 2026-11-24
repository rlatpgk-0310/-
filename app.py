import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="만나면 피해야 할 야생동물 가이드북",
    page_icon="🐾",
    layout="centered"
)

# 야생동물 데이터 리스트 (이름, 위험도, 이유, 기본점수, 대처메시지)
animal_list = [
    ["고양이", "별 한 개", "발톱에 긁힐 수 있으나 먼저 위협하지 않으면 안전합니다.", 10, "길고양이는 먼저 건드리지 말고 조용히 지나가세요."],
    ["강아지", "별 세 개", "주인 없는 들개는 무리를 지어 다니며 영역 본능이 강해 위험합니다.", 45, "들개를 마주쳤을 시 눈을 마주치지 말고 천천히 뒷걸음질 치세요."],
    ["멧돼지", "별 네 개", "시속 40km 이상의 돌진력과 날카로운 엄니를 가지고 있어 치명적입니다.", 75, "멧돼지를 마주쳤을 시 등을 보이지 말고 은폐물 뒤로 숨으세요."],
    ["곰", "별 다섯 개", "인간의 배가 되는 몸무게와 3m에 육박한 피지컬을 가진 곰은 총을 소지하고 있지 않는 이상 이길 수 없습니다.", 80, "야생곰을 마주쳤을 시 도주가 필요합니다."],
    ["코끼리", "별 다섯 개", "거대한 몸집과 괴력으로 흥분 시 주변의 모든 것을 파괴할 수 있습니다.", 85, "코끼리를 마주쳤을 시 즉시 차량이나 안전한 건물로 대피하세요."]
]

# 위험도 점수 및 경고문 계산 함수
def analyze_animal(animal_name, age):
    base_score = 0
    action_msg = ""
    
    for item in animal_list:
        if item[0] == animal_name:
            base_score = item[3]
            action_msg = item[4]
            break
            
    if age < 14 or age >= 65:
        bonus = 15
    elif 14 <= age <= 19:
        bonus = 3
    else:
        bonus = 0
        
    final_score = min(100, base_score + bonus)
    return final_score, action_msg

# 앱 UI 구성
st.title("🐾 만나면 피해야 할 야생동물 가이드북")
st.caption("10604 김세하 | 야생동물 마주침 대처 및 위험도 분석 서비스")

animal_names = [item[0] for item in animal_list]
selected_animal = st.selectbox("(1) 동물 선택 :", animal_names, index=3)
user_age = st.slider("(2) 나이 입력 :", min_value=1, max_value=150, value=17)

if st.button("분석하기"):
    score, message = analyze_animal(selected_animal, user_age)
    
    st.divider()
    st.subheader("[결과 출력 화면]")
    
    if score >= 70:
        st.error(f'"{message}"')
    elif score >= 40:
        st.warning(f'"{message}"')
    else:
        st.success(f'"{message}"')
        
    table_rows = []
    for item in animal_list:
        if item[0] == selected_animal:
            table_rows.append({
                "야생동물 이름": item[0],
                "위험도": item[1],
                "이유": item[2]
            })
            
    st.write("**피해야 할 야생동물과 이유**")
    df = pd.DataFrame(table_rows)
    st.table(df)
    
    st.metric(label=f"{user_age}세 기준 위험도 점수", value=f"{score}점")
