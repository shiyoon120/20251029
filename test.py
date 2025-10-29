import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📍 지하철 혼잡도 기반 최선 경로 추천 (샘플)")

# --- CSV 불러오기 ---
congestion_df = pd.read_csv("subway_congestion_sample.csv")

# --- 사용자 입력 ---
start_station = st.sidebar.text_input("출발역명", "잠실역")
end_station = st.sidebar.text_input("도착역명", "강남역")
time_hour = st.sidebar.slider("이용 시간대(시)", 5, 24, 18)

# --- 데이터 처리 함수 ---
def get_station_congestion(station, hour):
    rec = congestion_df[(congestion_df["역명"] == station) & (congestion_df["시간대"] == hour)]
    return rec["혼잡도(%)"].iloc[0] if not rec.empty else None

def compute_path_score(path):
    scores = [get_station_congestion(s, time_hour) for s in path]
    scores = [s for s in scores if s is not None]
    return sum(scores)/len(scores) if scores else float("inf")

# --- 경로 후보 ---
paths = {
    "경로 A": ["잠실역","선릉역","강남역"],
    "경로 B": ["잠실역","교대역","서초역","강남역"]
}

scores = {p: compute_path_score(paths[p]) for p in paths}
best_path = min(scores, key=scores.get)

# --- 출력 ---
st.subheader("추천 경로")
st.write(f"**{best_path}** (예상 평균 혼잡도: {scores[best_path]:.1f}%)")

df_out = pd.DataFrame({
    "경로": list(scores.keys()),
    "예상 평균 혼잡도(%)": list(scores.values())
})

fig = px.bar(df_out, x="경로", y="예상 평균 혼잡도(%)",
             color="예상 평균 혼잡도(%)",
             color_continuous_scale=["green","yellow","red"])
st.plotly_chart(fig)

st.subheader("혼잡 대비 팁")
st.markdown("""
- 혼잡도가 높은 시간대·역은 피하는 것이 좋습니다.
- 환승이 많은 경로는 환승역 체류 시간이 길어져 혼잡 가능성이 있습니다.
- 추천 경로라도 실시간 상황을 참고하세요.
""")
