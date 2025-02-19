import sqlite3

# 🟨🟨 SQLite 데이터베이스 연결 🟨🟨
DB_PATH = "C:/Users/user/projects/news-talk-ai/backend/database/news.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 🟨🟨 뉴스 데이터 저장 테이블 생성 🟨🟨
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

conn.commit()
conn.close()
