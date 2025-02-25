import React, { useState, useEffect } from "react";
import axios from "axios";
import { Container, Row, Col, Card, Button, Form } from "react-bootstrap";

function ExportData() {
  const [bookmarks, setBookmarks] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/get_bookmarks/")
      .then((response) => {
        setBookmarks(response.data.bookmarks);
      })
      .catch((error) => {
        console.error("북마크 기사 불러오기 실패:", error);
      });
  }, []);

  const handleDelete = (bookmarkId) => {
    axios
      .delete(`http://127.0.0.1:8000/delete_bookmark/${bookmarkId}/`)
      .then(() => {
        setBookmarks((current) =>
          current.filter((bookmark) => bookmark[0] !== bookmarkId)
        );
      })
      .catch((error) => {
        console.error("북마크 삭제 실패:", error);
      });
  };

  // 검색어에 따라 북마크 필터링 (bookmark[1]이 기사 제목이라고 가정)
  const filteredBookmarks = bookmarks.filter((bookmark) =>
    bookmark[1].toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Container>
      <h2 className="text-center mb-4">📂 북마크 기사모음 📂</h2>
      {/* 검색창 추가 */}
      <Form.Group className="mb-4" controlId="search">
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
      {/* 카드 목록 컨테이너: maxHeight와 스크롤 적용 */}
      <div style={{ maxHeight: "750px", overflowY: "auto" }}>
        <Row xs={1} md={2} lg={4} className="g-4">
          {filteredBookmarks.map((bookmark) => (
            <Col key={bookmark[0]}>
              <Card 
                className="h-100 shadow-sm"
                style={{ 
                  position: "relative",
                  borderRadius: "15px",
                  overflow: "hidden",
                  transition: "transform 0.3s, box-shadow 0.3s" 
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.transform = "scale(1.03)";
                  e.currentTarget.style.boxShadow = "0 8px 16px rgba(0,0,0,0.3)";
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.transform = "scale(1)";
                  e.currentTarget.style.boxShadow = "0 2px 5px rgba(0,0,0,0.15)";
                }}
              >
                {bookmark[3] && (
                  <Card.Img
                    variant="top"
                    src={bookmark[3]}
                    style={{ height: "150px", objectFit: "cover" }}
                  />
                )}
                <Button
                  onClick={() => handleDelete(bookmark[0])}
                  className="delete-btn"
                  style={{
                    position: "absolute",
                    top: "10px",
                    right: "10px",
                    zIndex: 10,
                    background: "rgba(255,255,255,0.8)",
                    border: "none",
                    borderRadius: "50%"
                  }}
                >
                  ❌
                </Button>
                <Card.Body>
                  <Card.Title style={{ fontSize: "1rem" }}>
                    <a
                      href={bookmark[2]}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-decoration-none text-dark"
                    >
                      {bookmark[1]}
                    </a>
                  </Card.Title>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </div>
    </Container>
  );
}

export default ExportData;