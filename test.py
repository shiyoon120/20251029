import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="마음 온도계 – 자살 예방 지원", layout="wide")
st.title("💛 마음 온도계 – 자살 예방 지원 대시보드")

# -------------------------------
# 1️⃣ 오늘의 마음 체크
# -------------------------------
st.header("1️⃣ 오늘의 마음을 체크해보세요")
st.markdown("한 줄로 지금 기분을 표현하거나 감정을 선택해보세요.")

# 감정 선택
emotion = st.selectbox("기분 선택", ["😊 행복", "😐 보통", "😔 슬픔", "😢 외로움", "😡 화남", "😰 불안"])

# 자유 텍스트 입력
text_input = st.text_area("자유롭게 지금 기분을 적어보세요 (선택)")

# -------------------------------
# 2️⃣ 간단 감정 분석 + 위험도
# -------------------------------
st.header("2️⃣ 분석 결과")

def analyze_emotion(text, selected_emotion):
    # 텍스트 입력 없으면 선택 감정 기준
    if text.strip() != "":
        text_lower = text.lower()
        if any(word in text_lower for word in ["우울", "슬픔", "외로움", "힘들", "죽고"]):
            risk = "높음 ⚠️"
            feedback = "지금 힘든 감정을 느끼고 있네요. 혼자가 아니에요."
        elif any(word in text_lower for word in ["걱정", "불안"]):
            risk = "보통 ⚠"
            feedback = "조금 불안한 기분이 있군요. 작은 산책이나 휴식이 도움될 수 있어요."
        else:
            risk = "낮음 ✅"
            feedback = "좋아요! 오늘 기분이 비교적 안정적이에요."
    else:
        # 선택 감정 기준
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
