import streamlit as st
import google.generativeai as genai
import os

# -------------------------
# 1. API Key 설정
# -------------------------
genai.configure(api_key="AIzaSyBK0YF3_0RRC_KiWV4uSK_-m_hC-usk6o0")

# -------------------------
# 2. 캐릭터별 페르소나 정의
# -------------------------
personas = {
    "짱구": """
너는 짱구는 못말려의 주인공 신짱구야. 
# 특징
- 나이: 5살
- 외모: 감자머리 별명, 까까머리
- 성격: 트러블메이커, 자기중심적, 활발, 귀찮음 많음
- 말투: 유아틱하고 장난스러움, "이런 이런", "으하하" 자주 사용
- 대화 규칙: 장난스럽게 대답하지만, 끝에는 유머/애교로 마무리
""",
    "영희": """
너는 '짱구는 못말려'의 캐릭터 영희야.
# 특징
- 나이: 5살
- 성격: 상냥하고 착하지만, 가끔은 짱구에게 휘둘림
- 말투: 또래보다 어른스럽게 말하려고 하지만 아이 같음
- 대화 규칙: 친절하고 예의 있게 답하지만, 가끔은 솔직하게 툭 튀어나오는 어린아이 같은 말투
"""
}

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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🟠 짱구", use_container_width=True):
            st.session_state["character"] = "짱구"
            st.session_state["page"] = "chat"
            st.session_state["messages"] = []  # 캐릭터 바뀌면 대화 초기화
            st.rerun()

    with col2:
        if st.button("🟢 영희", use_container_width=True):
            st.session_state["character"] = "영희"
            st.session_state["page"] = "chat"
            st.session_state["messages"] = []
            st.rerun()


# -------------------------
# 5. 채팅 화면
# -------------------------
elif st.session_state["page"] == "chat":
    character = st.session_state["character"]
    system_prompt = personas[character]

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
