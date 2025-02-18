import React, { useState, useEffect } from "react";
import axios from "axios";
import NewsDiscussion from "./components/NewsDiscussion";
import { Container, Button, Card, ListGroup, Row, Col, Spinner, Form } from "react-bootstrap";
import { BsSun, BsMoon, BsNewspaper, BsArrowRepeat, BsSearch } from "react-icons/bs";

function App() {
  const [news, setNews] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedNews, setSelectedNews] = useState(null);
  const [summary, setSummary] = useState("");
  const [loadingNews, setLoadingNews] = useState(true);
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [discussionPoints, setDiscussionPoints] = useState([]);
  const [loadingDiscussion, setLoadingDiscussion] = useState(false);

  // 카테고리 버튼의 한글 이름과 백엔드 엔드포인트에 쓰일 영어 키 매핑
  const categoryMapping = {
    "정치": "politics",
    "경제": "economy",
    "사회": "society",
    "생활문화": "life",
    "IT과학": "it",
    "세계": "world",
    "랭킹": "ranking",
  };

  // 초기 전체 뉴스 호출 (기존 기능 유지)
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/news")
      .then((response) => {
        setNews(response.data.news);
      })
      .catch((error) => {
        console.error("뉴스 가져오기 실패:", error);
      })
      .finally(() => {
        setLoadingNews(false);
      });
  }, []);

  // 카테고리 버튼 클릭 시 호출되는 함수
  const handleCategoryClick = (label) => {
    const category = categoryMapping[label];
    if (!category) return;
    setLoadingNews(true);
    axios.get(`http://127.0.0.1:8000/news/${category}`)
      .then((response) => {
        setNews(response.data.news);
      })
      .catch((error) => {
        console.error("카테고리 뉴스 가져오기 실패:", error);
      })
      .finally(() => {
        setLoadingNews(false);
      });
  };

  const handleSummarize = (title, url) => {
    setSelectedNews({ title, url });
    setSummary("");
    setLoadingSummary(true);
    axios.get("http://127.0.0.1:8000/summarize", { params: { title, url } })
      .then((response) => {
        setSummary(response.data.summary);
      })
      .catch((error) => {
        console.error("요약 실패:", error);
        setSummary("요약 실패 😢");
      })
      .finally(() => {
        setLoadingSummary(false);
      });
  };

  const handleDiscussionStart = () => {
    if (!selectedNews) return;
    setLoadingDiscussion(true);
    axios.get("http://127.0.0.1:8000/discuss", { params: { title: selectedNews.title, url: selectedNews.url } })
      .then((response) => {
        console.log("📢 토론 API 응답:", response.data);
        setDiscussionPoints(response.data.discussion_points);
      })
      .catch((error) => {
        console.error("토론 시작 오류:", error);
        setDiscussionPoints(["토론 데이터를 불러올 수 없습니다."]);
      })
      .finally(() => {
        setLoadingDiscussion(false);
      });
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle("dark-mode");
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim() === "") return;
    const searchUrl = `https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query=${encodeURIComponent(searchQuery)}`;
    window.open(searchUrl, "_blank");
  };

  return (
    <Container className="narrow-container mt-4">
      <h1 className="text-center mb-4">📰 실시간 인기 뉴스와 토론하기 📰</h1>
      <Form className="mb-3" onSubmit={handleSearch}>
        <Form.Group className="d-flex align-items-center">
          <Form.Control
            type="text"
            placeholder="🔍 관심있는 뉴스도 검색해보세요!   예) 트럼프 희토류"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="me-2 flex-grow-1"
          />
          <Button type="submit" variant="primary" className="flex-shrink-0">
            <BsSearch /> 검색
          </Button>
        </Form.Group>
      </Form>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <Form.Check 
          type="switch"
          id="dark-mode-toggle"
          label={darkMode ? "🌙 다크 모드" : "☀️ 라이트 모드"}
          checked={darkMode}
          onChange={toggleDarkMode}
        />  
      </div>
      <Row className="mb-4">
        <Col>
          <Card className="shadow-lg p-3 bg-white rounded">
            <Card.Body>
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h4 className="fw-bold text-secondary">🔥 최신 인기 뉴스 🔥</h4>
                <div className="d-flex flex-wrap gap-2">
                  <Button className="category-btn" size="sm" onClick={() => handleCategoryClick("정치")}>정치</Button>
                  <Button className="category-btn" size="sm" onClick={() => handleCategoryClick("경제")}>경제</Button>
                  <Button className="category-btn" size="sm" onClick={() => handleCategoryClick("사회")}>사회</Button>
                  <Button className="category-btn" size="sm" onClick={() => handleCategoryClick("생활문화")}>생활문화</Button>
                  <Button className="category-btn" size="sm" onClick={() => handleCategoryClick("IT과학")}>IT과학</Button>
                  <Button className="category-btn" size="sm" onClick={() => handleCategoryClick("세계")}>세계</Button>
                  <Button className="category-btn" size="sm" onClick={() => handleCategoryClick("랭킹")}>랭킹</Button>
                </div>
              </div>
              {loadingNews ? (
                <div className="text-center">
                  <Spinner animation="border" variant="primary" />
                  <p>뉴스 불러오는 중...</p>
                </div>
              ) : (
                <ListGroup variant="flush" className="bg-light p-3 rounded">
                  {news.map((item, index) => (
                    <ListGroup.Item key={index} className="d-flex justify-content-between align-items-center">
                      <div className="d-flex align-items-center">
                        {item.image && (
                          <img src={item.image} alt={item.title} className="news-image"/>
                        )}
                        <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-decoration-none text-dark fw-semibold">
                          {item.title}
                        </a>
                      </div>                               
                      <Button variant="success" size="sm" onClick={() => handleSummarize(item.title, item.url)}>요약 보기</Button>
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row>
        <Col>
          {selectedNews && (
            <Card className="border-primary">
              <Card.Body>
                <Card.Title className="text-primary">📰 {selectedNews.title}</Card.Title>
                {loadingSummary ? (
                  <div className="text-center">
                    <Spinner animation="grow" variant="info" />
                    <p>요약 생성 중...</p>
                  </div>
                ) : (
                  <Card.Text>{summary}</Card.Text>
                )}
                <NewsDiscussion title={selectedNews.title} url={selectedNews.url} />
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default App;
