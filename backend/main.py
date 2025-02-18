from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from news_scraper import get_top_news, get_article_image
try:
    from gpt_processor import summarize_news, discuss_news, respond_to_opinion
except ImportError:
    from gpt_processor import summarize_news, discuss_news, respond_to_opinion
import urllib.parse

import requests
from bs4 import BeautifulSoup
import random

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 뉴스별 대화 히스토리 저장
conversation_history = {}

# 기존 전체 뉴스 엔드포인트 (변경 없음)
@app.get("/news")
async def fetch_news():
    news = get_top_news()
    return {"news": news}

# 카테고리별 뉴스 크롤링을 위한 설정 및 함수 (이미지 포함)
NAVER_NEWS_CATEGORIES = {
    "ranking": "https://news.naver.com/main/ranking/popularDay.naver",
    "politics": "https://news.naver.com/section/100",
    "economy": "https://news.naver.com/section/101",
    "society": "https://news.naver.com/section/102",
    "life": "https://news.naver.com/section/103",
    "it": "https://news.naver.com/section/105",
    "world": "https://news.naver.com/section/104",
}

def fetch_category_news(category: str):
    url = NAVER_NEWS_CATEGORIES.get(category)
    if not url:
        raise ValueError("올바르지 않은 카테고리")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="네이버 뉴스 페이지 요청 실패")
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = []
    if category == "ranking":
        news_items = soup.select(".rankingnews_list li a.list_title")
    else:
        news_items = soup.select("ul.sa_list li a.sa_text_title")
    if not news_items:
        raise HTTPException(status_code=404, detail=f"{category} 카테고리에서 뉴스를 찾을 수 없음")
    sampled_news = random.sample(news_items, min(7, len(news_items)))
    for item in sampled_news:
        title = item.text.strip()
        link = item["href"]
        if not link.startswith("http"):
            link = "https://news.naver.com" + link
        image_url = get_article_image(link)
        news_list.append({"title": title, "url": link, "image": image_url})
    return news_list

@app.get("/news/{category}")
async def get_news_by_category(category: str):
    try:
        news = fetch_category_news(category)
        return {"category": category, "news": news}
    except ValueError:
        raise HTTPException(status_code=400, detail="잘못된 카테고리 요청")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summarize")
async def fetch_summary(title: str, url: str):
    summary = summarize_news(title, url)
    return {"title": title, "url": url, "summary": summary}

@app.get("/discuss")
async def fetch_discussion(title: str, url: str):
    discussion_points = discuss_news(title, url)
    return {"title": title, "url": url, "discussion_points": discussion_points}

@app.get("/respond")
async def fetch_response(title: str = Query(...), url: str = Query(...), opinion: str = Query(...)):
    title = urllib.parse.unquote(title)
    url = urllib.parse.unquote(url)
    opinion = urllib.parse.unquote(opinion)
    if (title, url) not in conversation_history:
        conversation_history[(title, url)] = []
    ai_response = respond_to_opinion(title, url, opinion)
    conversation_history[(title, url)].append({"user": opinion, "ai": ai_response})
    print(f"✅ 대화 히스토리 업데이트: {conversation_history[(title, url)]}")
    return {
        "title": title,
        "url": url,
        "opinion": opinion,
        "ai_response": ai_response,
        "conversation_history": conversation_history[(title, url)]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
