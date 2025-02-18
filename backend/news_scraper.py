import requests
from bs4 import BeautifulSoup

# 네이버 인기 뉴스 URL
NAVER_NEWS_URL = "https://news.naver.com/main/ranking/popularDay.naver"

def is_video_news(url):
    """네이버 뉴스 기사 URL이 동영상 뉴스인지 확인"""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return False  # 요청 실패 시 일반 기사로 간주
    soup = BeautifulSoup(response.text, "html.parser")
    meta_tag = soup.find("meta", {"property": "og:type"})
    if meta_tag and "video" in meta_tag.get("content", ""):
        return True  # 동영상 뉴스
    return False  # 일반 뉴스

def get_article_image(url):
    """뉴스 기사 페이지에서 og:image 메타 태그를 추출하여 이미지 URL 반환"""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        meta_tag = soup.find("meta", property="og:image")
        if meta_tag and meta_tag.get("content"):
            return meta_tag["content"]
    except Exception as e:
        print("Error fetching image from", url, ":", e)
    return None

def get_top_news():
    """네이버 인기 뉴스 중 일반 뉴스만 가져오기 (제목, URL, 이미지 포함)"""
    response = requests.get(NAVER_NEWS_URL, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print("⚠ 네이버 뉴스 페이지 요청 실패!")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    news_list = []
    for link in soup.select("a"):
        url = link.get("href", "")
        title = link.text.strip()
        if url.startswith("https://n.news.naver.com/article/") and title:
            if "동영상" in title:
                continue  
            if not is_video_news(url):
                image_url = get_article_image(url)
                news_list.append({"title": title, "url": url, "image": image_url})
        if len(news_list) == 7:  # 7개까지만 저장
            break
    return news_list

# 실행 예시
if __name__ == "__main__":
    news = get_top_news()
    for n in news:
        print(n)
