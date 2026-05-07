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
    {"name": "식위천", "menu": "중식", "image": "https://images.unsplash.com/photo-1512058560366-cd2429598632?q=80&w=600&h=400&fit=crop"}
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
