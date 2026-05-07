import streamlit as st
import random
import time
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍱")

# 1. 구글 시트 연결 설정
# 시트 URL을 아래 "YOUR_SHEET_URL" 부분에 넣으세요
SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_URL_HERE/edit#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

# --- [메뉴 데이터 및 슬롯 로직은 이전과 동일하므로 생략하거나 그대로 유지] ---
DEFAULT_MENU = [
    {"name": "김가네분식", "menu": "분식", "image": "https://img.tping.link/Content/Upload/Images/2018011519360001_Sld_20180115194046_5.JPG"},
    {"name": "성림돼지", "menu": "불백정식 & 냉면", "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSqARByjEipU15FJrvJnE1sVzvVIz-XFS_UA&s"},
    {"name": "식위천", "menu": "중식", "image": "https://images.unsplash.com/photo-1512058560366-cd2429598632?q=80&w=600&h=400&fit=crop"}
]

st.title("🍱 점심 메뉴 슬롯")
# ... (중략: 기존 슬롯 머신 코드 삽입 부분) ...

st.markdown("---")

# --- 게시판 영역: 구글 시트 연동 ---
st.header("📝 추가를 원하는 지정 식당")

# 시트에서 기존 데이터 불러오기 (캐시를 없애서 실시간 확인)
existing_data = conn.read(spreadsheet=SHEET_URL, usecols=[0, 1]).dropna()

# 댓글 입력창
with st.form(key="comment_form", clear_on_submit=True):
    new_comment = st.text_input("추천할 식당이나 하고 싶은 말", placeholder="예: 무교동 돈까스 추가해주세요!")
    submit_button = st.form_submit_button(label="등록")

    if submit_button and new_comment:
        now = time.strftime('%Y-%m-%d %H:%M')
        # 새 데이터 프레임 생성
        new_row = pd.DataFrame([{"date": now, "content": new_comment}])
        # 기존 데이터와 합치기
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        # 구글 시트에 업데이트
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        st.success("의견이 전송되었습니다!")
        st.rerun()

# 댓글 목록 표시 (최신순)
if not existing_data.empty:
    for i in range(len(existing_data)-1, -1, -1):
        row = existing_data.iloc[i]
        st.markdown(f"""
        <div style="padding: 10px; border-bottom: 1px solid #eee;">
            <small style="color: #888;">{row['date']} | 익명</small><br>
            <strong>{row['content']}</strong>
        </div>
        """, unsafe_allow_html=True)
