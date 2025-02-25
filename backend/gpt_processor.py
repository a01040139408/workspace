import os
import openai
import random
from dotenv import load_dotenv
from news_scraper import get_top_news
import json  # 🟩 JSON 파싱을 위해 추가

# .env 파일에서 API 키 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def summarize_news(news_title, news_url):
    """GPT-4o Mini를 사용해 뉴스 요약 생성"""
    prompt = f"다음 뉴스 기사 1줄 요약\n\n제목: {news_title}\n링크: {news_url}\n\n요약:"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 유능한 뉴스 요약가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"⚠ 오류 발생: {e}")
        return "요약 생성 실패"

def discuss_news(news_title, news_url):
    """GPT-4o Mini를 사용해 뉴스 논점 2개와 질문 2개 제공 (JSON 형식)"""
    # 🟩 프롬프트를 명확한 JSON 형식으로 요청
    prompt = f"""아래 뉴스 기사에 대해 JSON 형식으로 답변해 주세요.
형식은 다음과 같이 출력합니다.
{{
  "논점 1": "첫 번째 논점 내용",
  "논점 2": "두 번째 논점 내용",
  "질문 1": "첫 번째 질문 내용",
  "질문 2": "두 번째 질문 내용"
}}

제목: {news_title}
링크: {news_url}"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 유능한 뉴스 논평토론론가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        content = response.choices[0].message.content.strip()
        print("GPT 응답 원문:", content)  # 응답 원문 디버깅용
        
        # 🟩 JSON 형식으로 파싱 시도
        try:
            data = json.loads(content)
            discussion_points = [
                data.get("논점 1", "논점 생성 실패"),
                data.get("논점 2", "논점 생성 실패"),
                data.get("질문 1", "질문 생성 실패"),
                data.get("질문 2", "질문 생성 실패")
            ]
            return discussion_points
        except Exception as json_e:
            print("JSON 파싱 오류:", json_e)
            # JSON 파싱이 안되면 기존 방식으로 파싱 시도
            lines = content.split("\n")
            result = {}
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    result[key.strip()] = value.strip()
            discussion_points = [
                result.get("논점 1", "논점 생성 실패"),
                result.get("논점 2", "논점 생성 실패"),
                result.get("질문 1", "질문 생성 실패"),
                result.get("질문 2", "질문 생성 실패")
            ]
            return discussion_points

    except Exception as e:
        print(f"오류 발생: {e}")
        return ["논점 생성 실패", "논점 생성 실패", "질문 생성 실패", "질문 생성 실패"]

def respond_to_opinion(news_title, news_url, opinion):
    """GPT-4o Mini를 사용해 사용자의 의견에 응답"""
    prompt = f"사용자가 다음 뉴스 기사에 대해 의견을 제시했습니다.\n\n제목: {news_title}\n링크: {news_url}\n\n사용자 의견: {opinion}\n\n이 의견에 대해 논리적이고 흥미로운 반론을 해주세요. 100자로 답하세요"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 유능한 뉴스 토론 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        ai_response = response.choices[0].message.content.strip()
        ai_response = ai_response[:50]  # 최대 100자 제한
        return ai_response
    except Exception as e:
        print(f"⚠ 오류 발생: {e}")
        return "AI 응답 생성 실패"

def continue_chat(conversation_history, user_message):
    """
    대화 내역과 새 사용자 메시지를 받아 GPT-4o Mini API를 호출한 후,
    AI 응답과 업데이트된 대화 내역을 반환합니다.
    """
    # 사용자 메시지 추가 (프론트엔드에서 이미 추가되었을 수 있으므로 중복되지 않도록 주의)
    # conversation_history.append({"role": "user", "content": user_message})
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            temperature=0.7,
            max_tokens=100  # 필요에 따라 조정하세요.
        )
        ai_response = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response, conversation_history
    except Exception as e:
        print(f"⚠ 대화 이어가기 오류: {e}")
        return "AI 응답 생성 실패", conversation_history