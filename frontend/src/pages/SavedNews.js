import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Container,
  Row,
  Col,
  Card,
  ListGroup,
  Spinner,
  Button,
  Form,
  InputGroup
} from "react-bootstrap";
import 'bootstrap-icons/font/bootstrap-icons.css';

function SavedNews() {
  const [savedArticles, setSavedArticles] = useState([]);
  const [loadingSavedArticles, setLoadingSavedArticles] = useState(true);
  const [selectedNews, setSelectedNews] = useState(null);
  const [summary, setSummary] = useState("");
  const [discussionInput, setDiscussionInput] = useState({
    discussion_point1: "",
    discussion_point2: "",
    question1: "",
    question2: "",
    full_discussion: "",
  });
  const [searchQuery, setSearchQuery] = useState("");

  // 채팅 인터페이스 관련 상태
  const [showChat, setShowChat] = useState(false);
  const [chatMessages, setChatMessages] = useState([]); // { sender: "user" or "gpt", text: "" }
  const [chatInput, setChatInput] = useState("");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/articles/")
      .then((response) => {
        console.log("🟨🟨✅ 받은 데이터:", response.data.articles);
        setSavedArticles(
          response.data.articles.sort((a, b) => a[0] - b[0])
        );
      })
      .catch((error) => {
        console.error("❌ API 호출 실패:", error);
      })
      .finally(() => {
        setLoadingSavedArticles(false);
      });
  }, []);

  const handleDeleteArticle = (articleId) => {
    if (!window.confirm("이 기사를 삭제하시겠습니까?")) return;
    axios
      .delete(`http://127.0.0.1:8000/delete_article/${articleId}`)
      .then((response) => {
        alert(response.data.message);
        setSavedArticles((prevArticles) =>
          prevArticles
            .filter((article) => article[0] !== articleId)
            .sort((a, b) => a[0] - b[0])
        );
        if (selectedNews && selectedNews.id === articleId) {
          setSelectedNews(null);
          setSummary("");
          setDiscussionInput({
            discussion_point1: "",
            discussion_point2: "",
            question1: "",
            question2: "",
            full_discussion: "",
          });
        }
      })
      .catch((error) => {
        console.error("❌ 기사 삭제 실패:", error);
        alert("기사 삭제에 실패했습니다.");
      });
  };

  const handleLoadSavedArticle = (article) => {
    console.log("📢 저장된 기사 로드 함수 실행됨:", article);
    setSelectedNews({ id: article[0], title: article[1], url: "#" });
    setSummary(article[2]);
    setDiscussionInput({
      discussion_point1: article[3] || "논점 1",
      discussion_point2: article[4] || "논점 2",
      question1: article[5] || "질문 1",
      question2: article[6] || "질문 2",
      full_discussion: article[7] || "토론 내역 없음",
    });
    // 새로운 기사를 선택할 땐 이전 채팅 내역을 초기화하고 채팅창 숨김
    setChatMessages([]);
    setChatInput("");
    setShowChat(false);
  };

  const filteredArticles = savedArticles.filter((article) => {
    const query = searchQuery.toLowerCase();
    return (
      article[1].toLowerCase().includes(query) ||
      (article[3] && article[3].toLowerCase().includes(query)) ||
      (article[4] && article[4].toLowerCase().includes(query)) ||
      (article[5] && article[5].toLowerCase().includes(query)) ||
      (article[6] && article[6].toLowerCase().includes(query)) ||
      (article[7] && article[7].toLowerCase().includes(query))
    );
  });

  const handleChatSend = async () => {
    if (!chatInput.trim()) return;
    const userMessage = { sender: "user", text: chatInput };
    setChatMessages((prev) => [...prev, userMessage]);
    
    // 백엔드 /chat 엔드포인트에 대화 내역과 새 메시지 전송
    try {
      const response = await axios.post("http://127.0.0.1:8000/chat", {
        conversation_history: [
          { role: "system", content: "당신은 명쾌한 한줄답변 전문가입니다." },
          ...chatMessages.map(msg => msg.sender === "user" ? { role: "user", content: msg.text } : { role: "assistant", content: msg.text }),
          { role: "user", content: chatInput }
        ],
        message: chatInput
      });
      
      const gptResponse = { sender: "gpt", text: response.data.response };
      setChatMessages((prev) => [...prev, gptResponse]);
      setChatInput("");
    } catch (error) {
      console.error("채팅 요청 실패:", error);
    }
  };

  return (
    <Container className="mt-4">
      <h2 className="text-center mb-4"> 📝 토론했던 뉴스 한눈에 보기 📝</h2>
      <Row>
        {/* 저장된 뉴스 목록: 대화창이 열리면 폭이 좁아짐 */}
        <Col md={showChat ? 3 : 6} className="saved-news-list">
          <Card className="shadow-lg p-3 bg-white rounded h-100">
            <Card.Body>
              <h4 className="fw-bold text-secondary">📌 저장된 뉴스 목록</h4>
              <Form.Group className="mb-3" controlId="search">
                <Form.Control
                  type="text"
                  placeholder="검색어를 입력하세요..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  style={{
                    borderRadius: "25px",
                    boxShadow: "0 2px 5px rgba(0, 0, 0, 0.15)",
                    border: "1px solid #ced4da",
                    paddingLeft: "15px",
                  }}
                />
              </Form.Group>
              {loadingSavedArticles ? (
                <div className="text-center">
                  <Spinner animation="border" variant="primary" />
                  <p>저장된 뉴스 불러오는 중...</p>
                </div>
              ) : (
                <ListGroup variant="flush" className="saved-news-scroll">
                  {filteredArticles.length === 0 ? (
                    <p className="text-center">검색 결과가 없습니다.</p>
                  ) : (
                    filteredArticles.map((article) => (
                      <ListGroup.Item
                        key={article[0]}
                        className="clickable-news d-flex justify-content-between align-items-center"
                        onClick={() => handleLoadSavedArticle(article)}
                      >
                        <span className="article-number">{article[0]}</span>
                        <strong>{article[1]}</strong>
                        <Button
                          variant="danger"
                          size="sm"
                          className="delete-btn custom-delete-btn"
                          data-tooltip="기사 삭제"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteArticle(article[0]);
                          }}
                        >
                          ❌
                        </Button>
                      </ListGroup.Item>
                    ))
                  )}
                </ListGroup>
              )}
            </Card.Body>
          </Card>
        </Col>

        {/* 오른쪽 영역 */}
        {selectedNews && showChat ? (
          <>
            {/* 토론 내역 카드: 폭을 좀 넓게 설정 */}
            <Col md={5} className="saved-news-detail">
              <Card className="shadow-lg p-3 bg-white rounded h-100">
                <Card.Body className="d-flex flex-column">
                  <div>
                    <h4 className="fw-bold text-primary">📰 {selectedNews.title}</h4>
                    <p><strong>📄 요약:</strong> {summary}</p>
                    <p><strong>📌 논점 1:</strong> {discussionInput.discussion_point1}</p>
                    <p><strong>📌 논점 2:</strong> {discussionInput.discussion_point2}</p>
                    <p><strong>❓ 질문 1:</strong> {discussionInput.question1}</p>
                    <p><strong>❓ 질문 2:</strong> {discussionInput.question2}</p>
                    <p><strong>💬 토론 내역:</strong> {discussionInput.full_discussion}</p>
                  </div>
                  <div className="mt-auto text-end">
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => setShowChat(false)}
                    >
                      대화 종료
                    </Button>
                  </div>
                </Card.Body>
              </Card>
            </Col>
            {/* GPT 대화 카드: 더 넓은 폭으로 설정 */}
            <Col md={4} className="saved-news-chat">
  <Card className="shadow-lg p-3 bg-white rounded h-100">
    <Card.Header className="fw-bold text-success">
      🕵️ 간단한 궁금증 해결사 🕵️
    </Card.Header>
    <Card.Body className="d-flex flex-column">
      <div
        className="chat-messages mb-3 chat-container"
        // 계산식으로 InputGroup 높이(예시 60px 정도)를 뺀 나머지 영역을 스크롤 영역으로 사용
        style={{ flex: 1, overflowY: "auto", maxHeight: "calc(100% - 60px)" }}
      >
        {chatMessages.length === 0 ? (
          <p className="text-muted">메시지가 없습니다.</p>
        ) : (
          chatMessages.map((msg, index) => (
            <div
              key={index}
              className={`chat-bubble ${msg.sender === "user" ? "user" : "assistant"}`}
            >
              <strong>{msg.sender === "user" ? "나" : "해결사"}:</strong> {msg.text}
            </div>
          ))
        )}
      </div>
      <InputGroup>
        <Form.Control
          type="text"
          placeholder="메시지를 입력하세요..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleChatSend();
          }}
        />
        <Button variant="primary" onClick={handleChatSend}>
          전송
        </Button>
      </InputGroup>
    </Card.Body>
  </Card>
</Col>
          </>
        ) : (
          /* 채팅창이 닫힌 경우: 오른쪽은 상세 내용만 넓게 차지 */
          <Col md={6} className="saved-news-detail">
            <Card className="shadow-lg p-3 bg-white rounded h-100">
              <Card.Body className="d-flex flex-column">
                {selectedNews ? (
                  <>
                    <div>
                      <h4 className="fw-bold text-primary">📰 {selectedNews.title}</h4>
                      <p><strong>📄 요약:</strong> {summary}</p>
                      <p><strong>📌 논점 1:</strong> {discussionInput.discussion_point1}</p>
                      <p><strong>📌 논점 2:</strong> {discussionInput.discussion_point2}</p>
                      <p><strong>❓ 질문 1:</strong> {discussionInput.question1}</p>
                      <p><strong>❓ 질문 2:</strong> {discussionInput.question2}</p>
                      <p><strong>💬 토론 내역:</strong> {discussionInput.full_discussion}</p>
                    </div>
                    <div className="mt-auto text-end">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => setShowChat(true)}
                      >
                        대화하기
                      </Button>
                    </div>
                  </>
                ) : (
                  <p className="text-center text-muted">기사를 선택하면 여기에 내용이 표시됩니다.</p>
                )}
              </Card.Body>
            </Card>
          </Col>
        )}
      </Row>
    </Container>
  );
}

export default SavedNews;