import streamlit as st
import random
import time

# 1. 고정 메뉴 데이터
DEFAULT_MENU = [
    {"name": "김가네분식", "menu": "분식", "image": "https://img.tping.link/Content/Upload/Images/2018011519360001_Sld_20180115194046_5.JPG"},
    {"name": "성림돼지", "menu": "불백정식 & 냉면", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSqARByjEipU15FJrvJnE1sVzvVIz-XFS_UA&s"},
    {"name": "명동보리밥", "menu": "보리밥", "image": "https://pds.skyedaily.com/news_data/1361978092aeIfUjehNI2TJwjZvIE6RHC8LJ9Dc6.jpg"},
    {"name": "낙원참숯불갈비", "menu": "제육 쌈밥", "image": "https://mblogthumb-phinf.pstatic.net/MjAyMzA2MjRfMTg1/MDAxNjg3NjAyOTYyMzI4.YVrYjOS9JyVYvJGyOPufyVaWQ6gQE7T3MdSkC0uEiF4g.XYG-xAGEr_KDpxEdgaO6Bp-dvz5TQzdm1fqAZJ8OG9kg.JPEG.bojoh/1687602692781.jpg?type=w800"},
    {"name": "도삭면", "menu": "중식", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlEylDWD0rklIux_GHL9as5s1blThVi7i_wQ&s"},
    {"name": "만다린", "menu": "중식", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3dpqDswZ7kSyfT4gyQx2Sd3B_95mMEVMMGA&s"},
    {"name": "식위천", "menu": "중식", "image": "https://mblogthumb-phinf.pstatic.net/MjAyMzAyMTZfMTk1/MDAxNjc2NTA5NzMzMTM3.GltYqLyMJRxUTs_IH92XkqcnMsvOzKORv9rWHfCR2ugg.WFhMWuuMIPCgWLCYXob9VtAa3JVtJYCAkUBUdnO_7Scg.PNG.ukikiki32/SE-71602ba9-a32b-4f8c-92fb-bbad128d539e.png?type=w800"}
]

# 페이지 설정
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍱")

if 'menu_list' not in st.session_state:
    st.session_state.menu_list = DEFAULT_MENU.copy()

st.title("🍱 점심 메뉴 슬롯")
st.write("지정 식당 리스트에서 오늘의 메뉴를 골라줍니다!")

# --- 랜덤 슬롯 로직 ---
st.subheader(f"현재 후보: {len(st.session_state.menu_list)}개")
placeholder = st.empty()

if st.button("🚀 점심 메뉴 정하기 START!", use_container_width=True):
    steps = 30
    delay = 0.05

    for i in range(steps):
        current = random.choice(st.session_state.menu_list)

        # 💡 [핵심] f-string의 중괄호 충돌을 피하기 위해 CSS와 변수를 분리해서 작성했습니다.
        with placeholder.container():
            html_code = f"""
            <div style="text-align: center; border: 5px solid #FFD700; border-radius: 15px; padding: 20px; background-color: white;">
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