import React, { useState } from "react";
import axios from "axios";
import { Form, Button, Card, ListGroup, Badge } from "react-bootstrap";
import { Spinner } from "react-bootstrap";

const NewsDiscussion = ({ title, url }) => {
  const [discussionPoints, setDiscussionPoints] = useState([]);  // 🟨🟨🟨 빈 리스트로 초기화
  const [opinion, setOpinion] = useState("");
  const [conversationHistory, setConversationHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleDiscussion = () => {
    setLoading(true);
    axios.get("http://127.0.0.1:8000/discuss", { params: { title, url } })
      .then((response) => {
        setDiscussionPoints(response.data.discussion_points);
        setLoading(false);
      })
      .catch((error) => {
        console.error("토론 논점 가져오기 실패:", error);
        setDiscussionPoints("논점 가져오기 실패 😢");
        setLoading(false);
      });
  };

  const handleOpinionSubmit = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/respond", {
        params: { title, url, opinion },
      });
      setConversationHistory([...conversationHistory, { user: opinion, ai: response.data.ai_response }]);
      setOpinion("");
    } catch (error) {
      console.error("❌ AI 응답 실패:", error);
    }
  };

  return (
    <Card className="mt-4 p-3">
      <Card.Body>
        <Button variant="dark" onClick={handleDiscussion}>토론 시작</Button>
        {loading && (
  <div className="text-center mt-2">
    <Spinner animation="grow" variant="info" />
    <p>논점 생성 중...</p>
  </div>
)}


        {discussionPoints.length > 0 && (
          <ListGroup className="mt-3">
            {/* 🟨🟨🟨 API 응답이 리스트 형태이므로 인덱스로 접근 */}
            <ListGroup.Item><Badge bg="primary">논점 1</Badge> {discussionPoints[0]}</ListGroup.Item>
            <ListGroup.Item><Badge bg="secondary">논점 2</Badge> {discussionPoints[1]}</ListGroup.Item>
            <ListGroup.Item><Badge bg="info">질문 1</Badge> {discussionPoints[2]}</ListGroup.Item>
            <ListGroup.Item><Badge bg="success">질문 2</Badge> {discussionPoints[3]}</ListGroup.Item>
          </ListGroup>
        )}

        <Form className="mt-3">
          <Form.Group>
            <Form.Control 
              type="text" 
              value={opinion} 
              onChange={(e) => setOpinion(e.target.value)} 
              placeholder="여기에 의견을 입력하세요..." 
            />
          </Form.Group>
          <Button variant="primary" className="mt-2" onClick={handleOpinionSubmit}>의견 제출</Button>
        </Form>

        {/* 🟨🟨🟨 대화 UI 개선 (말풍선 스타일 적용) */}
        <Card className="mt-3">
          <Card.Header>🗨️ 토론 내역</Card.Header>
          <Card.Body style={{ maxHeight: "300px", overflowY: "auto" }}>
            {conversationHistory.length === 0 ? (
              <p className="text-center">아직 토론이 시작되지 않았습니다.</p>
            ) : (
              conversationHistory.map((entry, index) => (
                <div key={index} className="d-flex flex-column mb-3">
                  <div className="align-self-end bg-primary text-white p-2 rounded mb-1" style={{ maxWidth: "80%" }}>
                    <strong>사용자:</strong> {entry.user}
                  </div>
                  <div className="align-self-start bg-light p-2 rounded" style={{ maxWidth: "80%" }}>
                    <strong>AI:</strong> {entry.ai}
                  </div>
                </div>
              ))
            )}
          </Card.Body>
        </Card>
      </Card.Body>
    </Card>
  );
};

export default NewsDiscussion;
