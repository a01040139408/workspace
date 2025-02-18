import os
import openai
import random
from dotenv import load_dotenv
from news_scraper import get_top_news

# .env 파일에서 API 키 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def summarize_news(news_title, news_url):
    """GPT-4o Mini를 사용해 뉴스 요약 생성"""
    prompt = f"다음 뉴스 기사 1줄 요약\n\n제목: {news_title}\n링크: {news_url}\n\n요약:"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "당신은 유능한 뉴스 요약가입니다."},
                      {"role": "user", "content": prompt}],
            temperature=0.5
        )

        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        print(f"⚠ 오류 발생: {e}")
        return "요약 생성 실패"

def discuss_news(news_title, news_url):
    """GPT-4o Mini를 사용해 뉴스 논점 2개와 질문 2개 제공"""
    prompt = f"이 뉴스에 대한 중요한 토론 논점 2개를 제공하세요. 그런 다음 기사와 관련된 유의미한 질문 2개도 제공하세요.\n\n제목: {news_title}\n링크: {news_url}\n\n논점 1:\n논점 2:\n질문 1:\n질문 2:"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "당신은 유능한 뉴스 논평토론론가입니다."},
                      {"role": "user", "content": prompt}],
            temperature=0.5
        )

        content = response.choices[0].message.content.strip()
        discussion_points = content.split("\n")
        discussion_points = [point.split(":")[1].strip() for point in discussion_points if ":" in point]
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
            messages=[{"role": "system", "content": "당신은 유능한 뉴스 토론 전문가입니다."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100 #**응답길이 100자로 제한**
        )

        ai_response = response.choices[0].message.content.strip()

        # **응답을 100자로 제한**
        ai_response = ai_response[:100]  # 최대 100자까지만 자르기

        return ai_response

    except Exception as e:
        print(f"⚠ 오류 발생: {e}")
        return "AI 응답 생성 실패"