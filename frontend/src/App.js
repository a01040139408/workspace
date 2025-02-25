import React, { useState, useEffect } from "react";
import axios from "axios";
import NewsDiscussion from "./components/NewsDiscussion";
import { Container, Button, Card, ListGroup, Row, Col, Spinner, Form, Navbar, Nav } from "react-bootstrap";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { BsSun, BsMoon, BsNewspaper, BsArrowRepeat, BsSearch } from "react-icons/bs";
import bookmarkIcon from "./assets/icons/bookmark.png";

import Home from "./pages/Home";
import SavedNews from "./pages/SavedNews";
import ExportData from "./pages/ExportData";
import Settings from "./pages/Settings";

function App() {
  return (
    <Router>
      {/* 💚 네비게이션 바 수정: bg="dark"와 variant="dark" 유지, 추가 클래스 제거 가능 */}
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand as={Link} to="/">📢 뉴스 토론 AI</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <Nav.Link as={Link} to="/">🏠 홈</Nav.Link>
              <Nav.Link as={Link} to="/saved-news">📌 토론내역 보관소</Nav.Link>
              <Nav.Link as={Link} to="/export-data">📂 북마크 기사모음</Nav.Link>
              <Nav.Link as={Link} to="/settings">⚙️ 뭐로할까?</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* 💚 컨테이너 클래스 조정: narrow-container가 다른 페이지에서 필요 없을 경우 제거 고려 */}
      <Container className="mt-4">
        <Routes>
          <Route path="/" element={<HomeContent />} />
          <Route path="/saved-news" element={<SavedNews />} />
          <Route path="/export-data" element={<ExportData />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Container>
    </Router>
  );
}

// Home 페이지 콘텐츠를 별도 컴포넌트로 분리
function HomeContent() {
  const [news, setNews] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedNews, setSelectedNews] = useState(null);
  const [summary, setSummary] = useState("");
  const [loadingNews, setLoadingNews] = useState(true);
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [discussionPoints, setDiscussionPoints] = useState([]);
  const [loadingDiscussion, setLoadingDiscussion] = useState(false);
 
  const [discussionInput, setDiscussionInput] = useState({
    discussion_point1: "",
    discussion_point2: "",
    question1: "",
    question2: "",
    full_discussion: ""
  });

  const categoryMapping = {
    "정치": "politics",
    "경제": "economy",
    "사회": "society",
    "생활문화": "life",
    "IT과학": "it",
    "세계": "world",
    "랭킹": "ranking",
  };

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

  const handleInputChange = (e) => {
    setDiscussionInput({ ...discussionInput, [e.target.name]: e.target.value });
  };

  const handleSaveArticle = () => {
    if (!selectedNews || !summary) {
      alert("기사 요약이 완료된 후 저장 가능합니다.");
      return;
    }

    const articleData = {
      title: selectedNews.title,
      summary: summary,
      discussion_point1: discussionInput.discussion_point1,
      discussion_point2: discussionInput.discussion_point2,
      question1: discussionInput.question1,
      question2: discussionInput.question2,
      full_discussion: discussionInput.full_discussion,
    };

    axios.post("http://127.0.0.1:8000/save_article/", articleData)
      .then((response) => {
        alert(response.data.message);
      })
      .catch((error) => {
        console.error("데이터 저장 실패:", error);
        alert("데이터 저장 실패!");
      });
  };

  const handleBookmark = (item) => {
    axios
      .post("http://127.0.0.1:8000/bookmark_article/", {
        title: item.title,
        url: item.url,
        image: item.image,
      })
      .then((response) => {
        alert(response.data.message);
      })
      .catch((error) => {
        console.error("북마크 저장 실패:", error);
        alert("북마크 저장 실패!");
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
    axios
      .get("http://127.0.0.1:8000/discuss", { params: { title: selectedNews.title, url: selectedNews.url } })
      .then((response) => {
        console.log("📢 토론 API 응답:", response.data);
        setDiscussionPoints(response.data.discussion_points);
        const [arg1, arg2, q1, q2] = response.data.discussion_points;
        setDiscussionInput({
          discussion_point1: arg1 || "논점 1",
          discussion_point2: arg2 || "논점 2",
          question1: q1 || "질문 1",
          question2: q2 || "질문 2",
          full_discussion: "토론 내역",
        });
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

  const handleExportTXT = () => {
    if (!selectedNews || !summary) {
      alert("기사 요약이 완료된 후 내보내기가 가능합니다.");
      return;
    }

    const {
      discussion_point1 = "논점 1",
      discussion_point2 = "논점 2",
      question1 = "질문 1",
      question2 = "질문 2",
      full_discussion = "토론 내역",
    } = discussionInput || {};

    const content = `
  제목: ${selectedNews.title}
  
  요약: ${summary}
  
  논점 1: ${discussion_point1}
  논점 2: ${discussion_point2}
  질문 1: ${question1}
  질문 2: ${question2}
  토론 내역: ${full_discussion}
    `.trim();

    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "article_summary.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
                <div className="text-center loading-news">
                  <Spinner animation="border" variant="primary" />
                  <p>뉴스 불러오는 중...</p>
                </div>
              ) : (
                <ListGroup variant="flush" className="bg-light p-3 rounded">
                  {news.map((item, index) => (
// 기존 뉴스 리스트 렌더링 부분에서 북마크 아이콘 부분을 아래와 같이 수정
<ListGroup.Item key={index} className="d-flex justify-content-between align-items-center">
  <div className="d-flex align-items-center">
    {item.image && (
      <img src={item.image} alt={item.title} className="news-image" />
    )}
    <a
      href={item.url}
      target="_blank"
      rel="noopener noreferrer"
      className="text-decoration-none text-dark fw-semibold ms-2"
    >
      {item.title}
    </a>
  </div>
  <div className="d-flex align-items-center">
    <img
      src={bookmarkIcon}
      alt="북마크"
      style={{ width: "16px", height: "16px", marginRight: "4px", cursor: "pointer" }}
      onClick={() => handleBookmark(item)}
    />
    <Button variant="success" size="sm" onClick={() => handleSummarize(item.title, item.url)}>
      요약 보기
    </Button>
  </div>
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
                  <div className="text-center loading-summary">
                    <Spinner animation="grow" variant="info" />
                    <p>요약 생성 중...</p>
                  </div>
                ) : (
                  <Card.Text>{summary}</Card.Text>
                )}
                <NewsDiscussion
                  title={selectedNews.title}
                  url={selectedNews.url}
                  onDiscussionData={(data) => setDiscussionInput(data)}
                />
                <div className="d-flex justify-content-end">
                  <Button className="mt-3 custom-save-button" onClick={handleSaveArticle}>
                    데이터 저장
                  </Button>
                  <Button variant="warning" className="ms-2 d-flex align-items-center" onClick={handleExportTXT}>
                    <i className="bi bi-file-earmark-text me-1"></i> TXT 내보내기
                  </Button>
                </div>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default App;