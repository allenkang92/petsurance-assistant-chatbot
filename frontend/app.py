import streamlit as st
import requests
import json
import uuid

st.set_page_config(page_title="Petsurance AI", layout="centered", page_icon="🐾")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 모드별 대화 기록 격리
if "messages_dict" not in st.session_state:
    st.session_state.messages_dict = {"최신 판매 중 상품의 약관 챗봇": [], "이외 상품의 약관 챗봇": []}

if "mode" not in st.session_state:
    st.session_state.mode = "최신 판매 중 상품의 약관 챗봇"

with st.sidebar:
    st.header("⚙️ 설정")
    selected_mode = st.radio("상담 모드 선택", ["최신 판매 중 상품의 약관 챗봇", "이외 상품의 약관 챗봇"])
    
    if selected_mode != st.session_state.mode:
        st.session_state.mode = selected_mode
        st.rerun()

    if st.session_state.mode == "이외 상품의 약관 챗봇":
        st.subheader("📄 약관 문서 업로드")
        file = st.file_uploader("파일 선택", type=["pdf", "txt", "md"])
        if file and st.button("학습 시작"):
            with st.spinner("분석 중..."):
                res = requests.post(f"http://localhost:8000/upload?session_id={st.session_state.session_id}_custom", files={"file": (file.name, file.getvalue())})
                if res.status_code == 200: st.success("완료!")
                else: st.error("실패")

    if st.button("대화 초기화"):
        st.session_state.messages_dict[st.session_state.mode] = []
        st.rerun()

st.title("🐾 PETSURANCE 약관 챗봇")
st.info(f"현재 모드: **{st.session_state.mode}**")

for message in st.session_state.messages_dict[st.session_state.mode]:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("질문하세요"):
    st.session_state.messages_dict[st.session_state.mode].append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        suffix = "fixed" if st.session_state.mode == "최신 판매 중 상품의 약관 챗봇" else "custom"
        endpoint = "/chat" if st.session_state.mode == "최신 판매 중 상품의 약관 챗봇" else "/chat/custom"
        
        try:
            r = requests.post(f"http://localhost:8000{endpoint}", json={"question": prompt, "session_id": f"{st.session_state.session_id}_{suffix}"}, stream=True)
            if r.status_code == 200:
                for line in r.iter_lines():
                    if line:
                        data = json.loads(line.decode('utf-8')[6:])
                        full_res += data["chunk"]
                        placeholder.markdown(full_res + "▌")
                placeholder.markdown(full_res)
                st.session_state.messages_dict[st.session_state.mode].append({"role": "assistant", "content": full_res})
            else: st.error(f"오류: {r.json().get('detail')}")
        except Exception as e: st.error(f"연결 실패: {e}")
