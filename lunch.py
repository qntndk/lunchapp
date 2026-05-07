import streamlit as st
import random
import time
import os

# 1. 페이지 설정
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍱", layout="centered")

# 2. 데이터 파일 설정 (파일 저장 방식)
DB_FILE = "lunch_comments.txt"

def load_comments():
    """파일에서 댓글 읽어오기"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    return []

def save_comment(text):
    """파일에 댓글 추가하기"""
    now = time.strftime('%Y-%m-%d %H:%M')
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{now} | {text}\n")

# 3. 고정 메뉴 데이터 (슬롯 머신용)
DEFAULT_MENU = [
    {"name": "김가네분식", "menu": "분식", "image": "https://img.tping.link/Content/Upload/Images/2018011519360001_Sld_20180115194046_5.JPG"},
    {"name": "성림돼지", "menu": "불백정식 & 냉면", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSqARByjEipU15FJrvJnE1sVzvVIz-XFS_UA&s"},
    {"name": "명동보리밥", "menu": "보리밥", "image": "https://pds.skyedaily.com/news_data/1361978092aeIfUjehNI2TJwjZvIE6RHC8LJ9Dc6.jpg"},
    {"name": "낙원참숯불갈비", "menu": "제육 쌈밥", "image": "https://mblogthumb-phinf.pstatic.net/MjAyMzA2MjRfMTg1/MDAxNjg3NjAyOTYyMzI4.YVrYjOS9JyVYvJGyOPufyVaWQ6gQE7T3MdSkC0uEiF4g.XYG-xAGEr_KDpxEdgaO6Bp-dvz5TQzdm1fqAZJ8OG9kg.JPEG.bojoh/1687602692781.jpg?type=w800"},
    {"name": "도삭면", "menu": "중식", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlEylDWD0rklIux_GHL9as5s1blThVi7i_wQ&s"},
    {"name": "만다린", "menu": "중식", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3dpqDswZ7kSyfT4gyQx2Sd3B_95mMEVMMGA&s"},
    {"name": "식위천", "menu": "중식", "image": "data:image/jpeg;base64,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"}
]

# 세션 상태 초기화
if 'menu_list' not in st.session_state:
    st.session_state.menu_list = DEFAULT_MENU.copy()

# --- 메인 영역: 점심 메뉴 슬롯 ---
st.title("🍱 점심 메뉴 슬롯")
st.write("지정 식당 리스트에서 오늘의 메뉴를 골라줍니다!")

st.subheader(f"현재 후보: {len(st.session_state.menu_list)}개")
placeholder = st.empty()

if st.button("🚀 점심 메뉴 정하기 START!", use_container_width=True):
    steps = 30
    delay = 0.05

    for i in range(steps):
        current = random.choice(st.session_state.menu_list)
        with placeholder.container():
            html_code = f"""
            <div style="text-align: center; border: 5px solid #FFD700; border-radius: 15px; padding: 20px; background-color: white; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #ff4b4b; margin-bottom: 5px;">{current['name']}</h1>
                <h3 style="color: #333; font-weight: normal;">{current['menu']}</h3>
                <div style="width: 100%; height: 300px; display: flex; align-items: center; justify-content: center; background-color: #f9f9f9; border-radius: 10px; margin-top: 15px; overflow: hidden;">
                    <img src="{current['image']}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                </div>
            </div>
            """
            st.markdown(html_code, unsafe_allow_html=True)

        if i > 20: delay += 0.05
        elif i > 25: delay += 0.15
        time.sleep(delay)

    st.balloons()
    st.success(f"결정! 오늘의 메뉴는 **{current['name']}**입니다!")

if st.button("다시 돌리기"):
    st.rerun()

st.markdown("---")

# --- 게시판 영역: 추가를 원하는 지정 식당 ---
st.header("📝 추가를 원하는 지정 식당")
st.write("맛집을 추천해주세요! (※ 서버 환경에 따라 가끔 초기화될 수 있습니다.)")

# 1. 댓글 입력 폼
with st.form(key="comment_form", clear_on_submit=True):
    new_comment = st.text_input("추천 식당 (메뉴)", placeholder="예: 무교동 돈까스 추가해주세요!")
    submit_button = st.form_submit_button(label="의견 보내기")

    if submit_button and new_comment:
        save_comment(new_comment)
        st.success("의견이 기록되었습니다!")
        time.sleep(0.5)
        st.rerun()

# 2. 댓글 목록 표시
st.subheader("💬 동료들의 추천 목록")
comments = load_comments()

if comments:
    # 최신글이 위로 오도록 역순 출력
    for c in reversed(comments):
        # 시간과 내용을 분리해서 예쁘게 표시
        try:
            timestamp, content = c.split(" | ", 1)
            st.markdown(f"""
            <div style="padding: 12px; border-bottom: 1px solid #eee; background-color: #fafafa; border-radius: 5px; margin-bottom: 5px;">
                <small style="color: #888;">{timestamp} | 익명</small><br>
                <span style="font-size: 1.1em; color: #333;">{content.strip()}</span>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.text(c.strip())
else:
    st.info("아직 추천된 식당이 없습니다. 첫 의견을 남겨보세요!")
