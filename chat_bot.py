import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from .utils import fetch_data_from_url, parse_data, generate_response

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

    if data:
        # データの解析
        parsed_data = parse_data(data)

        # ユーザーの入力を監視
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area(label='Message: ', key='input', height=100, value='')
            submit_button = st.form_submit_button(label='Send')

            if submit_button and user_input:
                # ユーザーが入力し、Submitボタンが押された場合に実行されるコード
                st.session_state.messages.append(HumanMessage(content=user_input))

                # 解析したデータを使用して回答を生成
                response = generate_response(parsed_data, user_input)

                if response is None:
                    # 関連する情報が見つからなかった場合、GPTに回答を生成させる
                    with st.spinner("お馬さんが一生懸命考えています...."):
                        response = llm(st.session_state.messages)

                    st.session_state.messages.append(AIMessage(content=response.content))

                else:
                    with st.spinner("関連する情報を検索中..."):
                        st.session_state.messages.append(AIMessage(content=str(response)))

    else:
        st.write("データの取得に失敗しました。")

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
