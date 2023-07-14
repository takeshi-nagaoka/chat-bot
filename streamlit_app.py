import streamlit as st
import requests
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage, AIMessage)


def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to fetch data from URL: {url}")
        return None


def main():
    llm = ChatOpenAI(temperature=0)

    st.set_page_config(
        page_title="ツォクトモンゴル乗馬ツアーのAIチャットボット🐴",
        page_icon="🐴"
    )
    st.header("ツォクトモンゴル乗馬ツアーのAIチャットボット🐴")

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="ご質問を入力ください。QAを元にAIが回答いたします。")
        ]

    # URLからデータを取得
    url = "https://mongol-jyouba-gakkou.com/attention"
    data = fetch_data_from_url(url)

    if data:
        # ユーザーの入力を監視
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area(label='Message: ', key='input', height=100, value=data, readonly=True)
            submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                # ユーザーが入力し、Submitボタンが押された場合に実行されるコード
                st.session_state.messages.append(HumanMessage(content=user_input))
                with st.spinner("お馬さんが考えています...."):
                    response = llm(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))

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

    else:
        st.error("Failed to fetch data from URL.")


if __name__ == '__main__':
    main()
