import sqlite3

DB_PATH = "C:/Users/20101/news-talk-ai/backend/database/news.db"

def create_bookmark_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            image TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def bookmark_article(title, url, image):
    create_bookmark_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookmarks (title, url, image) VALUES (?, ?, ?)", (title, url, image))
    conn.commit()
    conn.close()

def get_bookmarked_articles():
    create_bookmark_table()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookmarks")
    results = cursor.fetchall()
    conn.close()
    return results

# 추가된 북마크 삭제 함수
def delete_bookmark(bookmark_id):
    """북마크를 데이터베이스에서 삭제하는 함수"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookmarks WHERE id = ?", (bookmark_id,))
        if cursor.rowcount == 0:
            raise ValueError(f"ID {bookmark_id}에 해당하는 북마크를 찾을 수 없습니다.")
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"북마크 삭제 실패: {e}")
        raise
    finally:
        conn.close()