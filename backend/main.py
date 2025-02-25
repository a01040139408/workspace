import os
import sys
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.crud import save_article, get_all_articles, delete_article
from pydantic import BaseModel
from news_scraper import get_top_news, get_article_image
try:
    from gpt_processor import summarize_news, discuss_news, respond_to_opinion, continue_chat
except ImportError:
    from gpt_processor import summarize_news, discuss_news, respond_to_opinion, continue_chat
import urllib.parse

import requests
import sqlite3
from bs4 import BeautifulSoup
import random
import io
from fastapi.responses import StreamingResponse
from docx import Document
from fpdf import FPDF
from database.crud import save_article, get_all_articles, delete_article
from fastapi import Body
from database.bookmark_crud import bookmark_article, get_bookmarked_articles, delete_bookmark
from fastapi.responses import FileResponse  # 이미 import 되어 있더라도 다시 선언해도 무방




app = FastAPI()

DB_PATH = "C:/Users/20101/news-talk-ai/backend/database/news.db"

# 🟨🟨 현재 작업 디렉토리를 추가하여 `crud.py`를 올바르게 import 🟨🟨
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

class ArticleData(BaseModel):
    title: str
    summary: str
    discussion_point1: str = "논점 1"
    discussion_point2: str = "논점 2"
    question1: str = "질문 1"
    question2: str = "질문 2"
    full_discussion: str = "토론 내역"

# 추가: 대화 요청 모델 정의
class ChatRequest(BaseModel):
    conversation_history: list  # [{ "role": "system"/"user"/"assistant", "content": "..." }, ...]
    message: str    

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

@app.post("/save_article/")
def save_article_api(article: ArticleData):
    """🟨🟨 뉴스 데이터를 DB에 저장하는 API 엔드포인트 🟨🟨"""
      # 로깅 추가: 수신된 데이터 확인
    print("🟨🟨 Received article data:", article.dict())
    save_article(
        article.title, 
        article.summary, 
        article.discussion_point1, 
        article.discussion_point2, 
        article.question1, 
        article.question2, 
        article.full_discussion
    )
     # 🟨🟨 저장 후 DB에서 모든 데이터를 가져와 로그로 출력 🟨🟨
    articles = get_all_articles()
    print("🟨🟨 Current articles in DB:", articles)
    return {"message": "내역 저장 성공!"}

@app.get("/export/txt/")
def export_txt():
    """🟨🟨 저장된 데이터를 TXT 파일로 변환 후 다운로드 🟨🟨"""
    file_path = "exported_data.txt"
    
    # SQLite에서 데이터 가져오기
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    conn.close()
    
    # TXT 파일 생성
    with open(file_path, "w", encoding="utf-8") as f:
        for article in articles:
            f.write(f"제목: {article[1]}\n")
            f.write(f"요약: {article[2]}\n")
            f.write(f"논점 1: {article[3]}\n")
            f.write(f"논점 2: {article[4]}\n")
            f.write(f"질문 1: {article[5]}\n")
            f.write(f"질문 2: {article[6]}\n")
            f.write(f"토론 내용: {article[7]}\n")
            f.write("="*50 + "\n\n")

    return FileResponse(file_path, filename="news_discussion.txt", media_type="text/plain")


@app.get("/articles/")
def get_articles():
    """🟨🟨 저장된 기사 목록 조회 API 🟨🟨"""
    articles = get_all_articles()
    # 🟨🟨 id를 순차적으로 재정렬하여 반환 💚
    reordered_articles = [(i + 1, *article[1:]) for i, article in enumerate(articles)]
    return {"articles": reordered_articles}

@app.get("/get-saved-news")
async def get_saved_news():
    """🟨🟨 저장된 뉴스 데이터 반환 API (id 순차적으로 재정렬) 🟨🟨"""
    articles = get_all_articles()
    # 🟨🟨 id를 순차적으로 재정렬하여 반환 💚
    reordered_articles = [(i + 1, *article[1:]) for i, article in enumerate(articles)]
    formatted_articles = [
        {
            "id": article[0],  # 순차 번호 (1부터 시작)
            "title": article[1],
            "summary": article[2],
            "discussion_point1": article[3],
            "discussion_point2": article[4],
            "question1": article[5],
            "question2": article[6],
            "full_discussion": article[7],
        }
        for article in reordered_articles
    ]
    return {"saved_news": formatted_articles}

@app.delete("/delete_article/{article_id}")
def delete_article(article_id: int):
    """🟨🟨 기사 삭제 후 id를 1부터 순차적으로 재정렬하는 API 엔드포인트 🟨🟨"""
    try:
        if delete_article(article_id):  # 💙💙 crud.delete_article 호출 💙💙
            articles = get_all_articles()
            reordered_articles = [(i + 1, *article[1:]) for i, article in enumerate(articles)]
            return {"message": "기사 삭제 성공!", "remaining_ids": [article[0] for article in reordered_articles]}
        raise HTTPException(status_code=500, detail="기사 삭제 실패")
    except Exception as e:
        print(f"🟨🟨 삭제 API 오류: {e}")
        raise HTTPException(status_code=500, detail=f"기사 삭제 실패: {str(e)}")

@app.post("/chat")
def chat_endpoint(chat_req: ChatRequest):
    if not chat_req.message:
        raise HTTPException(status_code=400, detail="메시지가 없습니다.")
    ai_response, updated_history = continue_chat(chat_req.conversation_history, chat_req.message)
    return {"response": ai_response, "conversation_history": updated_history}


@app.post("/bookmark_article/")
def bookmark_article_api(data: dict = Body(...)):
    title = data.get("title")
    url = data.get("url")
    image = data.get("image")
    if not title or not url:
        raise HTTPException(status_code=400, detail="필수 필드 누락")
    bookmark_article(title, url, image)
    return {"message": "북마크 저장 성공!"}

@app.get("/get_bookmarks/")
def get_bookmarks():
    bookmarks = get_bookmarked_articles()
    return {"bookmarks": bookmarks}

@app.delete("/delete_bookmark/{bookmark_id}")
def delete_bookmark_api(bookmark_id: int):
    """북마크를 삭제하는 API 엔드포인트"""
    try:
        if delete_bookmark(bookmark_id):
            return {"message": "북마크 삭제 성공!"}
        raise HTTPException(status_code=500, detail="북마크 삭제 실패")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"북마크 삭제 API 오류: {e}")
        raise HTTPException(status_code=500, detail=f"북마크 삭제 실패: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
