import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)
import requests


def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def main():
    llm = ChatOpenAI(temperature=0)

    st.set_page_config(
        page_title="My Great ChatGPT",
        page_icon="🐴"
    )
    st.header("ツォクトモンゴル乗馬ツアーのAIチャットボット🐴")

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="ご質問を入力ください。QAを元にAIが回答いたします。")
        ]

    # サイドバーのタイトルを表示
    st.sidebar.title("Options")

    def init_messages():
        clear_button = st.sidebar.button("チャット履歴を削除", key="clear")
        if clear_button:
            st.session_state.messages = []

    init_messages()

    # URLからデータを取得
    url = "https://mongol-jyouba-gakkou.com/attention"
    data = fetch_data_from_url(url)

    # ユーザーの入力を監視
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area(label='Message: ', key='input', height=100, value='')
        submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            # ユーザーが入力し、Submitボタンが押された場合に実行されるコード
            st.session_state.messages.append(HumanMessage(content=user_input))

            # URLの内容を使用して回答を生成
            response = generate_response(data, user_input)

            st.session_state.messages.append(AIMessage(content=response))

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")


def generate_response(data, user_input):
    # URLの内容を使用して回答を生成するロジックを実装
    # ここでは単純にURLの内容をそのまま返す例としています
    return data


if __name__ == '__main__':
    main()
