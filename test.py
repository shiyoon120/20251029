# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob

st.set_page_config(page_title="마음 온도계 – 자살 예방 지원", layout="wide")
st.title("💛 마음 온도계 – 자살 예방 지원 대시보드")

# -------------------------------
# 1️⃣ 오늘의 마음 체크
# -------------------------------
st.header("1️⃣ 오늘의 마음을 체크해보세요")
st.markdown("간단히 한 문장으로 지금 기분을 표현하거나 감정을 선택해주세요.")

# 옵션 1: 감정 선택
emotion = st.selectbox("기분 선택", ["😊 행복", "😐 보통", "😔 슬픔", "😢 외로움", "😡 화남", "😰 불안"])

# 옵션 2: 자유 텍스트 입력
text_input = st.text_area("자유롭게 지금 기분을 적어보세요 (선택)")

# -------------------------------
# 2️⃣ 감정 분석 + 위험도
# -------------------------------
st.header("2️⃣ 분석 결과")

def analyze_emotion(text, selected_emotion):
    if text.strip() != "":
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 ~ +1
        if polarity < -0.5:
            risk = "높음 ⚠️"
            feedback = "지금 힘든 감정을 느끼고 있네요. 혼자가 아니에요."
        elif polarity < 0:
            risk = "보통 ⚠"
            feedback = "조금 우울한 기분이 있군요. 작은 산책이나 휴식이 도움될 수 있어요."
        else:
            risk = "낮음 ✅"
            feedback = "좋아요! 오늘 기분이 비교적 안정적이에요."
    else:
        # 선택 감정 기반 간단 위험도
        if selected_emotion in ["😔 슬픔", "😢 외로움", "😰 불안"]:
            risk = "보통 ⚠"
            feedback = "조금 우울하거나 외로운 감정이 있군요. 스스로 돌보는 시간을 가지세요."
        else:
            risk = "낮음 ✅"
            feedback = "좋아요! 오늘 기분이 비교적 안정적이에요."
    return risk, feedback

risk_level, feedback_text = analyze_emotion(text_input, emotion)
st.metric(label="현재 위험도", value=risk_level)
st.info(feedback_text)

# -------------------------------
# 3️⃣ 상담 및 도움 정보
# -------------------------------
st.header("3️⃣ 긴급 상담/지원 정보")

st.markdown("""
- ☎️ **1393**: 자살예방상담전화  
- ☎️ **1588-9191**: 생명의전화  
- ☎️ **1577-0199**: 정신건강상담  
- 지역별 정신건강복지센터 검색: [바로가기](https://www.mindmap.or.kr)
""")

# -------------------------------
# 4️⃣ 자살률 통계 시각화
# -------------------------------
st.header("4️⃣ 연령별/성별 자살률 통계 (샘플 데이터)")

# 샘플 통계 데이터
data = {
    "연령대": ["10대","20대","30대","40대","50대","60대"],
    "남성 자살률": [8, 22, 30, 35, 40, 45],
    "여성 자살률": [5, 12, 18, 20, 25, 30]
}
df = pd.DataFrame(data)

fig = px.bar(df, x="연령대", y=["남성 자살률","여성 자살률"], barmode="group",
             labels={"value":"자살률 (명/10만명)", "연령대":"연령대"})
st.plotly_chart(fig, use_container_width=True)

st.markdown("※ 실제 데이터 기반으로 연령별·성별 자살률 변화를 시각화한 예시입니다.")
