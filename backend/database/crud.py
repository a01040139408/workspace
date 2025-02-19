import sqlite3

DB_PATH = "C:/Users/user/projects/news-talk-ai/backend/database/news.db"

def save_article(title, summary, discussion_point1, discussion_point2, question1, question2, full_discussion):
    """🟨🟨 뉴스 데이터를 SQLite에 저장하는 함수 🟨🟨"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 🟨🟨 테이블 존재 여부 확인 후 생성 🟨🟨
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            discussion_point1 TEXT,
            discussion_point2 TEXT,
            question1 TEXT,
            question2 TEXT,
            full_discussion TEXT
        )
        """)

        # 🟨🟨 데이터 삽입 (논점, 질문, 토론 내역 포함) 🟨🟨
        cursor.execute("""
        INSERT INTO articles (title, summary, discussion_point1, discussion_point2, question1, question2, full_discussion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, summary, discussion_point1, discussion_point2, question1, question2, full_discussion))

        conn.commit()
    except sqlite3.Error as e:
        print("데이터 저장 실패:", e)
    finally:
        conn.close()


def get_all_articles():
    """🟨🟨 저장된 모든 기사 데이터 조회 🟨🟨"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, title, summary, discussion_point1, discussion_point2, question1, question2, full_discussion FROM articles
        """)
        articles = cursor.fetchall()

        return articles
    except sqlite3.Error as e:
        print("데이터 조회 실패:", e)
        return []
    finally:
        conn.close()
