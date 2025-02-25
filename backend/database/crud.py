import sqlite3
import os

DB_PATH = "C:\\Users\\20101\\news-talk-ai\\backend\\database\\news.db"

# 데이터베이스 디렉토리와 파일 확인 및 생성
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        pass  # 빈 파일 생성

# 데이터베이스 파일 권한 확인 (Windows에서 필요 시)
import stat
if os.path.exists(DB_PATH):
    os.chmod(DB_PATH, stat.S_IWRITE | stat.S_IREAD)  # 읽기/쓰기 권한 부여

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
        print(f"데이터 저장 실패: {e}")
        raise
    finally:
        conn.close()

def get_all_articles():
    """🟨🟨 저장된 모든 기사 데이터 조회 (실제 SQLite id 반환) 🟨🟨"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 🟨🟨 실제 SQLite id를 기준으로 조회 💙💙
        cursor.execute("""
        SELECT id, title, summary, discussion_point1, discussion_point2, question1, question2, full_discussion 
        FROM articles 
        ORDER BY id
        """)
        articles = cursor.fetchall()

        return articles  # 실제 SQLite id 반환
    except sqlite3.Error as e:
        print(f"데이터 조회 실패: {e}")
        raise
    finally:
        conn.close()

def delete_article(article_id):
    """🟨🟨 기사 삭제 후 id를 1부터 순차적으로 재정렬하는 함수 🟨🟨"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 🟨🟨 삭제 요청된 article_id가 숫자형인지 확인 💙💙
        article_id = int(article_id)
        cursor.execute("SELECT id FROM articles WHERE id = ?", (article_id,))
        if not cursor.fetchone():
            raise ValueError(f"ID {article_id}에 해당하는 기사를 찾을 수 없습니다.")

        # 🟨🟨 기사 삭제 💙💙
        cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
        if cursor.rowcount == 0:
            raise ValueError(f"ID {article_id} 삭제 실패: 레코드가 없음.")

        # 🟨🟨 삭제 후 남은 레코드의 id를 1부터 순차적으로 재정렬 💙💙
        cursor.execute("SELECT id, title, summary, discussion_point1, discussion_point2, question1, question2, full_discussion FROM articles ORDER BY id")
        remaining_articles = cursor.fetchall()
        
        # 🟨🟨 테이블 데이터 삭제 (모두 삭제 후 재삽입) 💙💙
        cursor.execute("DELETE FROM articles")
        conn.commit()

        # 🟨🟨 순차적으로 id를 재배열하여 삽입 💙💙
        new_id = 1
        for article in remaining_articles:
            cursor.execute("""
            INSERT INTO articles (id, title, summary, discussion_point1, discussion_point2, question1, question2, full_discussion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (new_id, *article[1:]))
            new_id += 1

        conn.commit()
        return True
    except (ValueError, sqlite3.Error) as e:
        print(f"기사 삭제 실패: {e}")
        raise
    finally:
        conn.close()