# -*- coding: utf‑8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="지하철 혼잡도 기반 최선 경로 추천", layout="wide")

st.title("📍 지하철 혼잡도 기반 ‘덜 붐비는’ 경로 추천")

# --- 사용자 입력 ---
st.sidebar.header("이용 정보 입력")
start_station = st.sidebar.text_input("출발역명", value="잠실역")
end_station   = st.sidebar.text_input("도착역명", value="강남역")
time_hour     = st.sidebar.slider("이용 시간대(시)", 5, 24, 18)
recommendation_type = st.sidebar.selectbox("추천 기준", ["혼잡도 최소", "환승 최소"])

# --- 데이터 로드 ---
# 실제 데이터를 다운로드한 후 실제 파일 경로/파일명을 적절히 조정하세요.
# 예: "seoul_subway_congestion.csv"
congestion_df = pd.read_csv("서울교통공사_지하철혼잡도정보_20241231.csv", encoding="utf‑8")

# --- 데이터 처리 함수 ---
def get_station_congestion(station: str, hour: int, df: pd.DataFrame) -> float:
    """주어진 역명과 시간대에서 혼잡도(%)를 반환. 데이터 없으면 None."""
    rec = df[(df["역명"] == station) & (df["시간대"] == hour)]
    if not rec.empty:
        return float(rec["혼잡도(%)"].iloc[0])
    else:
        return None

def compute_path_score(path_stations: list, hour: int, df: pd.DataFrame) -> float:
    """경로에 포함된 역들의 평균 혼잡도(%) 계산. None인 역은 무시."""
    scores = []
    for s in path_stations:
        val = get_station_congestion(s, hour, df)
        if val is not None:
            scores.append(val)
    if scores:
        return sum(scores) / len(scores)
    else:
        return float("inf")

# --- 경로 후보 예시 (단순화) ---
paths = {
    "경로 A (직접 환승 적음)": ["잠실역", "선릉역", "강남역"],
    "경로 B (환승 많음 예상)": ["잠실역", "교대역", "서초역", "강남역"]
}

# --- 점수 계산 ---
scores = {p: compute_path_score(paths[p], time_hour, congestion_df) for p in paths}

# --- 추천 결정 ---
best_path = min(scores, key=scores.get)

# --- 출력 ---
st.subheader("추천 결과")
st.write(f"**추천 경로:** {best_path}")
st.write(f"예상 평균 혼잡도: {scores[best_path]:.1f}%")

df_out = pd.DataFrame({
    "경로": list(scores.keys()),
    "예상 평균 혼잡도(%)": list(scores.values())
})

fig = px.bar(df_out, x="경로", y="예상 평균 혼잡도(%)",
             color="예상 평균 혼잡도(%)",
             color_continuous_scale=["green","yellow","red"],
             labels={"예상 평균 혼잡도(%)": "혼잡도(%)"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("✅ 혼잡 대비 팁 및 안내")
st.markdown("""
- 혼잡도가 낮은 경로를 선택하는 것이 덜 붐비는 이동을 돕습니다.
- 환승이 많은 경로는 환승역에서 체류 시간이 길어져 혼잡 가능성이 커질 수 있습니다.
- 추천된 경로라도 실제 상황(이벤트, 비상사태 등)에 따라 다를 수 있으므로 **참고용**으로 활용하세요.
- 이동 중 **출입구 위치**, **환승 거리**, **시간 여유** 등을 미리 확인하면 안전한 이동에 도움이 됩니다.
""")
