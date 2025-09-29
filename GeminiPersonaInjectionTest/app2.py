import streamlit as st
import google.generativeai as genai
import json
import os

# -------------------------
# 1. API Key 설정
# -------------------------
genai.configure(api_key="AIzaSyBK0YF3_0RRC_KiWV4uSK_-m_hC-usk6o0")

# -------------------------
# 2. 캐릭터별 페르소나 정의
# -------------------------

# TODO: need to get persona and personality list from server for production ENV or define the list as contant value 
with open("../data/namuwiki_persona.json", "r") as f:
    personas = json.load(f)

# -------------------------
# 3. 세션 상태 초기화
# -------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "home"   # home → 캐릭터 선택, chat → 대화화면
if "character" not in st.session_state:
    st.session_state["character"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# -------------------------
# 4. 홈 화면 (캐릭터 선택)
# -------------------------
if st.session_state["page"] == "home":
    st.set_page_config(page_title="ChatWithYourIdol", page_icon="🎭", layout="centered")
    st.title("ChatWithYourIdol 🎭")
    st.subheader("대화할 캐릭터를 선택하세요")

    # Create as many columns as dictionary entries
    cols = st.columns(len(personas))

    # Iterate and fill the columns
    for col, name in zip(cols, personas.keys()):
        with col:
            if st.button(name, use_container_width=True):
                st.session_state["character"] = name
                st.session_state["page"] = "chat"
                st.session_state["messages"] = []  # 캐릭터 바뀌면 대화 초기화
                st.rerun()

# -------------------------
# 5. 채팅 화면
# -------------------------
elif st.session_state["page"] == "chat":
    character = st.session_state["character"]
    system_prompt = f"""
    # 너는 앞으로 제공된 CONTEXT에 맞춰서 답변하는 영화나 만화의 주인공이야. 너는 더이상 범용적인 인공지능이 아니기 때문에 내가 제공한 CONTEXT에 기반한 캐릭터 처럼 답변해.

    ## CONTEXT
    {personas[character]}
    
    """
    
    # 모델 생성
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt
    )

    st.set_page_config(page_title=f"{character}와 대화하기", page_icon="🤖", layout="centered")
    st.title(f"✨ {character}와 대화하기 ✨")

    # 대화 로그 표시
    for role, msg in st.session_state["messages"]:
        if role == "user":
            st.markdown(
                f"""
                <div style="background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0; text-align:right">
                    <b>👤 You:</b> {msg}
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="background-color:#FFF176; padding:10px; border-radius:10px; margin:5px 0; text-align:left">
                    <b>{character}:</b> {msg}
                </div>
                """, unsafe_allow_html=True
            )

    # 입력창
    user_input = st.chat_input(f"{character}에게 뭐라고 할래?")

    if user_input:
        # 사용자 메시지 저장
        st.session_state["messages"].append(("user", user_input))

        # 모델 응답
        with st.spinner(f"{character}가 대답 중... 🤔"):
            response = model.generate_content(user_input)
            bot_reply = response.text

        st.session_state["messages"].append(("bot", bot_reply))
        st.rerun()

    # 홈으로 돌아가기 버튼
    if st.button("⬅️ 캐릭터 선택으로 돌아가기"):
        st.session_state["page"] = "home"
        st.rerun()
