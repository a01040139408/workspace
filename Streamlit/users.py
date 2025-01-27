import streamlit as st
import oracledb
# 추가: 로깅 모듈 import
import logging

# 추가: 로깅 설정
logging.basicConfig(level=logging.ERROR)

# DB 연결 설정
def get_connection():
    return oracledb.connect(
        user="system",
        password="oracle",
        dsn="localhost:1521/xe"
    )

# Streamlit 앱
st.title("회원 관리 시스템")

menu = st.sidebar.selectbox("메뉴", ["로그인", "회원가입", "비밀번호 찾기"])

if menu == "로그인":
    st.subheader("로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT *
        FROM users
        WHERE LOWER(username) = LOWER(:username) AND password = :password
        """
        cursor.execute(query, {"username": username.strip(), "password": password.strip()})
        result = cursor.fetchone()
        conn.close()

        if result:
            st.success(f"환영합니다, {username.strip()}님!")

            # 인삿말 남기기 기능 시작
            st.subheader("인삿말 남기기")
            greeting_username = st.text_input("아이디 입력", value=username.strip())
            greeting_message = st.text_input("인삿말 작성")

            if st.button("인삿말 저장"):
                if not greeting_message.strip():
                    st.error("인삿말을 입력해주세요.")
                else:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        
                        # 데이터 저장
                        insert_query = """
                        INSERT INTO greetings (id, username, message)
                        VALUES (greetings_seq.NEXTVAL, :username, :message)
                        """
                        cursor.execute(insert_query, {"username": greeting_username.strip(), "message": greeting_message.strip()})
                        conn.commit()

                        # 추가: 저장 성공 여부 확인
                        check_query = "SELECT * FROM greetings WHERE username = :username ORDER BY id DESC"
                        cursor.execute(check_query, {"username": greeting_username.strip()})
                        saved_greeting = cursor.fetchone()

                        if saved_greeting:
                            st.success(f"인삿말이 저장되었습니다: \"{saved_greeting[2]}\"")
                        else:
                            st.error("저장이 실패했습니다.")
                            # 추가: 로깅
                            logging.error("인삿말 저장 실패: 데이터베이스에서 저장된 인삿말을 찾을 수 없음")

                    except Exception as e:
                        st.error(f"오류 발생: {e}")
                        # 추가: 로깅
                        logging.error(f"인삿말 저장 중 오류 발생: {e}")
                    finally:
                        # 수정: cursor도 명시적으로 닫기
                        cursor.close()
                        conn.close()
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")

elif menu == "회원가입":
    st.subheader("회원가입")
    new_username = st.text_input("아이디")
    new_password = st.text_input("비밀번호", type="password")
    confirm_password = st.text_input("비밀번호 확인", type="password")

    if st.button("회원가입"):
        if new_password != confirm_password:
            st.error("비밀번호가 일치하지 않습니다. 다시 입력해주세요.")
        elif not new_username or not new_password:
            st.error("아이디와 비밀번호를 모두 입력해주세요.")
        else:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                query = """
                INSERT INTO users (username, password)
                VALUES (:username, :password)
                """
                cursor.execute(query, {"username": new_username.strip(), "password": new_password.strip()})
                conn.commit()
                st.success("회원가입이 완료되었습니다!")
            except oracledb.IntegrityError:
                st.error("이미 존재하는 아이디입니다. 다른 아이디를 입력해주세요.")
            except Exception as e:
                st.error(f"오류 발생: {e}")
                # 추가: 로깅
                logging.error(f"회원가입 중 오류 발생: {e}")
            finally:
                # 수정: cursor도 명시적으로 닫기
                cursor.close()
                conn.close()

elif menu == "비밀번호 찾기":
    st.subheader("비밀번호 찾기")
    username = st.text_input("아이디")

    if "step" not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        if st.button("아이디 확인"):
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT username FROM users WHERE LOWER(username) = LOWER(:username)"
            cursor.execute(query, {"username": username.strip()})
            result = cursor.fetchone()
            # 수정: cursor도 명시적으로 닫기
            cursor.close()
            conn.close()

            if result:
                st.success("아이디가 확인되었습니다. 추가 질문에 답변해주세요.")
                st.session_state.step = 2
                st.session_state.username = username.strip()
            else:
                st.error("존재하지 않는 아이디입니다.")

    if st.session_state.step == 2 and "username" in st.session_state:
        security_answer = st.text_input("관리자의 휴대폰번호 마지막 4자리는 무엇입니까?")
        if st.button("답변 제출"):
            if security_answer == "5187":
                conn = get_connection()
                cursor = conn.cursor()
                query = "SELECT password FROM users WHERE LOWER(username) = LOWER(:username)"
                cursor.execute(query, {"username": st.session_state.username})
                result = cursor.fetchone()
                # 수정: cursor도 명시적으로 닫기
                cursor.close()
                conn.close()

                if result:
                    st.info(f"비밀번호: {result[0]}")
                    st.session_state.step = 1  # 초기화
                else:
                    st.error("비밀번호를 가져오는 데 실패했습니다.")
                    # 추가: 로깅
                    logging.error(f"비밀번호 찾기 실패: {st.session_state.username}의 비밀번호를 찾을 수 없음")
            else:
                st.error("추가 질문의 답변이 틀렸습니다.")
