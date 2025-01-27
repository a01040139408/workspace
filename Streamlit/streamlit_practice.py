import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# 제목 추가
st.title("Streamlit 연습하기")

# 텍스트 추가
st.write("이 페이지는 Streamlit의 기능을 연습하기 위해 만들어졌습니다.")

# 버튼 추가
if st.button("안녕하세요 버튼을 눌러보세요"):
    st.write("버튼이 눌렸습니다!")

# 제목
st.title("Streamlit 모든 기능 연습하기")

# 1. 텍스트와 버튼
st.header("1. 텍스트와 버튼 사용")
st.write("버튼을 눌러 결과를 확인하세요!")

if st.button("안녕하세요 버튼"):
    st.write("버튼이 눌렸습니다!")

# 2. 텍스트 입력
st.header("2. 텍스트 입력 사용")
name = st.text_input("이름을 입력하세요:")
if name:
    st.write(f"안녕하세요, {name}님!")

# 3. 슬라이더
st.header("3. 슬라이더 사용")
number = st.slider("0에서 100 사이의 숫자를 선택하세요", 0, 100, 50)
st.write(f"선택한 숫자는 {number}입니다.")

# 4. 데이터프레임 표시
st.header("4. 데이터프레임 표시")
data = {
    "이름": ["철수", "영희", "민수"],
    "점수": [85, 90, 78]
}
df = pd.DataFrame(data)
st.write("학생들의 점수:")
st.dataframe(df)

# 5. 차트 그리기
st.header("5. 랜덤 데이터 차트 그리기")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)
st.line_chart(chart_data)

# 6. 지도 표시
st.header("6. 지도 표시")
map_data = pd.DataFrame(
    {
        "lat": [37.5665, 37.5678, 37.5651],
        "lon": [126.9780, 126.9792, 126.9768]
    }
)
st.map(map_data)

# 7. 파일 업로드
st.header("7. 파일 업로드 기능")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")
if uploaded_file is not None:
    file_data = pd.read_csv(uploaded_file)
    st.write("업로드한 데이터:")
    st.dataframe(file_data)

# 8. 사용자 인터랙션 요약
st.header("8. 입력 요약")
st.write("현재 입력한 정보 요약:")
st.write(f"- 이름: {name}")
st.write(f"- 선택한 숫자: {number}")

# Markdown 연습 섹션
st.header("9. Markdown 연습")

# Markdown 활용 예제
st.markdown("# 큰 제목")
st.markdown("## 중간 제목")
st.markdown("### 작은 제목")
st.markdown("""
- **굵은 텍스트**와 *기울어진 텍스트*를 사용할 수 있습니다.
- `코드 블록`을 작성하거나, 
- 아래와 같은 목록을 만들 수 있습니다:
  1. 첫 번째 항목
  2. 두 번째 항목
  3. 세 번째 항목
""")
st.markdown("> 인용구도 사용할 수 있습니다!")

# 치킨 먹을지 피자 먹을지 선택하는 게임
st.header("10. 치킨 vs 피자 게임 🍕🍗")

st.markdown("**오늘 저녁은 뭐 먹을까요?** 아래에서 선택해보세요!")

# 옵션 제공
choice = st.radio("메뉴를 선택하세요:", ["치킨", "피자"])

if choice == "치킨":
    st.markdown("# 🍗 치킨을 선택하셨군요!")
    st.write("치킨엔 역시 **콜라**가 딱이죠! 맛있게 드세요! 😋")
elif choice == "피자":
    st.markdown("# 🍕 피자를 선택하셨군요!")
    st.write("피자엔 역시 **사이다**가 최고죠! 맛있게 드세요! 🤤")

# 추가 Markdown 활용
st.markdown("### 재미있는 음식 게임")
st.markdown("""
- 치킨이나 피자 중에 하나만 골라야 한다면?
- 선택한 메뉴를 가족과 공유해 보세요!
- **좋은 음식 선택이 행복한 하루를 만듭니다!**
""")

# 11. 뉴스 데이터 가져오기
st.header("11. 실시간 뉴스 헤드라인")

# 뉴스 데이터를 가져오는 함수 정의
def get_latest_news():
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:10]:  # 최신 기사 10개 가져오기
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary
        })
    return articles

# 12. 버튼 클릭 시 뉴스 가져오기
if st.button("최신 뉴스 가져오기"):
    news_list = get_latest_news()
    if news_list:
        for i, news in enumerate(news_list, start=1):
            st.subheader(f"{i}. {news['title']}")
            st.write(news['summary'])
            st.write(f"[기사 원문 보기]({news['link']})")
    else:
        st.write("뉴스를 가져올 수 없습니다.")



        # 버튼 클릭 예제
st.title("버튼 클릭 예제")

if st.button("클릭하세요!"):
    st.write("버튼이 클릭되었습니다! 🎉")
else:
    st.write("아직 버튼을 클릭하지 않았습니다.")

#13.  간단한 계산기
st.title("간단한 계산기")

# 숫자 입력
st.header("숫자를 입력하세요")
num1 = st.number_input("첫 번째 숫자", value=0.0)
num2 = st.number_input("두 번째 숫자", value=0.0)

# 연산자 선택
operation = st.selectbox("연산자를 선택하세요", ["더하기 (+)", "빼기 (-)", "곱하기 (x)", "나누기 (÷)"])

# 계산 및 결과 출력
st.header("결과")
if operation == "더하기 (+)":
    result = num1 + num2
    st.write(f"결과: {num1} + {num2} = {result}")
elif operation == "빼기 (-)":
    result = num1 - num2
    st.write(f"결과: {num1} - {num2} = {result}")
elif operation == "곱하기 (x)":
    result = num1 * num2
    st.write(f"결과: {num1} × {num2} = {result}")
elif operation == "나누기 (÷)":
    if num2 != 0:
        result = num1 / num2
        st.write(f"결과: {num1} ÷ {num2} = {result}")
    else:
        st.error("0으로 나눌 수 없습니다!")


import streamlit as st
from PIL import Image, ImageFilter

# 이미지 필터 적용
st.title("이미지 필터 적용")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="업로드한 이미지", use_column_width=True)

    st.markdown("### 필터 적용")
    option = st.selectbox("필터를 선택하세요", ["블러", "엠보스", "샤프닝"])

    if option == "블러":
        filtered_img = img.filter(ImageFilter.BLUR)
    elif option == "엠보스":
        filtered_img = img.filter(ImageFilter.EMBOSS)
    else:
        filtered_img = img.filter(ImageFilter.SHARPEN)

    st.image(filtered_img, caption="필터 적용 결과", use_column_width=True)

import streamlit as st
import pandas as pd
import numpy as np
import time

# 실시간 데이터 시각화
st.title("실시간 데이터 시각화")
st.markdown("### 랜덤 데이터의 실시간 업데이트 예제")

# 랜덤 데이터 생성
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)

chart = st.line_chart(chart_data)

# 실시간 업데이트
for _ in range(50):
    time.sleep(0.1)
    new_data = pd.DataFrame(
        np.random.randn(1, 3),
        columns=["A", "B", "C"]
    )
    chart.add_rows(new_data)

import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Plotly 애니메이션 그래프
st.title("Plotly 애니메이션 그래프")

# 데이터 생성
n_frames = 20  # 애니메이션 프레임 수
df = pd.DataFrame({
    "x": np.random.rand(n_frames),  # x축 데이터
    "y": np.random.rand(n_frames),  # y축 데이터
    "time": np.arange(n_frames)     # 시간 축 (프레임)
})

# Plotly 애니메이션
fig = px.scatter(
    df,
    x="x",
    y="y",
    animation_frame="time",          # 애니메이션 프레임 설정
    title="시간에 따른 점의 이동",
    range_x=[0, 1],                  # x축 범위
    range_y=[0, 1]                   # y축 범위
)

# Streamlit에서 Plotly 그래프 표시
st.plotly_chart(fig)

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# 제목
st.title("Matplotlib 실시간 애니메이션")

# 초기 데이터
x = np.linspace(0, 2 * np.pi, 100)  # x축 데이터 (0 ~ 2π)
y = np.sin(x)  # 초기 y값 (sin 함수)

# 차트 생성
placeholder = st.empty()  # Streamlit에서 차트를 업데이트할 공간 생성
fig, ax = plt.subplots()  # Matplotlib 서브플롯 생성
line, = ax.plot(x, y)  # 초기 플롯 생성

# 실시간 애니메이션
for i in range(50):  # 50번 업데이트
    y = np.sin(x + i / 10.0)  # 시간에 따른 y값 변화
    line.set_ydata(y)  # y 데이터 업데이트
    ax.relim()  # 축 범위 재설정
    ax.autoscale_view()  # 축 자동 스케일링
    placeholder.pyplot(fig)  # Streamlit에서 Matplotlib 그래프 업데이트
    time.sleep(0.1)  # 0.1초 대기

import streamlit as st
import time
import numpy as np

# 제목
st.title("실시간 값 변화 애니메이션")

# 초기 설정
progress_bar = st.progress(0)  # 진행률 바
status_text = st.empty()  # 상태 표시 텍스트
chart_placeholder = st.empty()  # 차트 플레이스홀더

data = []  # 데이터를 저장할 리스트

# 애니메이션 루프
for i in range(101):  # 0부터 100까지 진행
    new_value = np.random.randint(0, 100)  # 0~100 사이의 랜덤 값 생성
    data.append(new_value)  # 데이터 리스트에 추가

    # 업데이트
    progress_bar.progress(i)  # 진행률 바 업데이트
    status_text.text(f"현재 값: {new_value}")  # 현재 상태 출력
    chart_placeholder.line_chart(data)  # 실시간 라인 차트 업데이트

    time.sleep(0.1)  # 0.1초 대기
