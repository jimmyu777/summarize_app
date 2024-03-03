#### 기본 정보 불러오기 ####
# Streamlit 패키지를 st라는 이름으로 가져옵니다. Streamlit을 사용하면 웹 애플리케이션을 쉽게 만들 수 있습니다.
import streamlit as st
# OpenAI의 GPT 모델을 사용하기 위해 openai 패키지를 가져옵니다.
import openai

#### 기능 구현 함수 ####
# GPT에 질문하고 응답을 받는 함수입니다.
def askGpt(prompt, apikey):
    # OpenAI 클라이언트를 생성하고, 사용자의 API 키로 인증합니다.
    client = openai.OpenAI(api_key=apikey)
    # GPT-3.5 모델에게 사용자의 질문(prompt)을 전달하고, 응답을 받습니다.
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",  # 사용할 모델 지정
        messages = [{"role": "user", "content": prompt}]  # 사용자 역할과 내용을 메시지로 전달
    )
    # 응답에서 첫 번째 선택의 메시지 내용을 추출합니다.
    gptResponse = response.choices[0].message.content
    # 추출한 응답을 반환합니다.
    return gptResponse

#### 메인 함수 ####
def main():
    # 페이지 설정: 페이지 제목을 "요약 프로그램"으로 설정합니다.
    st.set_page_config(page_title="요약 프로그램")
    # 세션 상태에 OPENAI_API 키가 없다면 초기화합니다.
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""

    # 사이드바 생성
    with st.sidebar:
        # 사이드바에 OpenAI API 키를 입력받는 텍스트 입력 필드를 생성합니다. 비밀번호 형식으로 입력됩니다.
        open_apikey = st.text_input(label='OPEN API 키', placeholder='Enter Your API Key', type='password')
        # 사용자가 API 키를 입력하면 세션 상태에 저장합니다.
        if open_apikey:
            st.session_state["OPENAI_API"] = open_apikey
        # 사이드바에 구분선을 추가합니다.
        st.markdown('---')
        
    # 페이지의 헤더를 추가합니다.
    st.header("📃요약 프로그램")
    # 페이지에 구분선을 추가합니다.
    st.markdown('---')
    
    # 사용자로부터 요약할 텍스트를 입력받습니다.
    text = st.text_area("요약 할 글을 입력하세요")
    # "요약" 버튼이 클릭되면 아래의 코드를 실행합니다.
    if st.button("요약"):
        # GPT에 전달할 질문을 구성합니다. 여기서는 텍스트를 한국어로 요약하는 지시를 포함합니다.
        prompt = f'''
        **Instructions** :
        - You are an expert assistant that summarizes text into **Korean language**.
        - Your task is to summarize the **text** sentences in **Korean language**.
        - Your summaries should include the following :
        - Omit duplicate content, but increase the summary weight of duplicate content.
        - Summarize by emphasizing concepts and arguments rather than case evidence.
        - Summarize in 3 lines.
        - Use the format of a bullet point.
        - text: {text}
        '''
        # askGpt 함수를 호출하여 GPT로부터 요약된 응답을 받고, 이를 정보 상자로 페이지에 표시합니다.
        st.info(askGpt(prompt, st.session_state["OPENAI_API"]))
        
# 스크립트가 직접 실행되면 main 함수를 호출합니다.
if __name__ == "__main__":
    main()
