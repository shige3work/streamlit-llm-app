from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# OpenAI APIで使うLLMインスタンス（gpt-4o-mini使用）
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# 専門家ごとのシステムプロンプトを定義
expert_prompts = {
    "医師": "あなたは経験豊富な内科医です。医学的な質問に対して、正確で専門的な回答を行ってください。",
    "弁護士": "あなたは法律の専門家です。法的な質問に対して分かりやすく、実用的なアドバイスを提供してください。",
    "エンジニア": "あなたはソフトウェアエンジニアです。プログラミングやシステム設計に関する質問に的確に答えてください。"
}

# 入力と選択を受け取り、LLMの回答を返す関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    system_prompt = expert_prompts.get(expert_type, "あなたは親切なアシスタントです。")
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    response = llm(messages)
    return response.content

# StreamlitのUI構築
st.title("専門家AIチャット")
st.markdown("""
このアプリは、AI「医師」「弁護士」「エンジニア」などの各専門家が、あなたの質問に対して最適な回答を提供します。  
下記のフォームに質問を入力し、専門家を選んで送信してください。
""")

# 専門家の種類選択（ラジオボタン）
expert_type = st.radio("専門家を選んでください", list(expert_prompts.keys()))

# 入力フォーム
user_input = st.text_area("質問内容を入力してください", height=100)

# 送信ボタン
if st.button("送信"):
    if user_input.strip():
        with st.spinner("AIが考え中..."):
            result = get_llm_response(user_input, expert_type)
            st.markdown("### 回答：")
            st.write(result)
    else:
        st.warning("質問内容を入力してください。")
