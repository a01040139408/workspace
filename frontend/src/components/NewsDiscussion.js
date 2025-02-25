import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Form, Button, Card, ListGroup, Badge, Spinner } from "react-bootstrap";

const NewsDiscussion = ({ title, url, onDiscussionData = () => {} }) => {
  const [discussionPoints, setDiscussionPoints] = useState([]);
  const [opinion, setOpinion] = useState("");
  const [conversationHistory, setConversationHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null); // 🟨🟨 자동 스크롤 적용을 위한 ref 추가 🟨🟨

  const handleDiscussion = () => {
    setLoading(true);
    axios.get("http://127.0.0.1:8000/discuss", { params: { title, url } })
      .then((response) => {
        const points = response.data.discussion_points;
        setDiscussionPoints(points);
        onDiscussionData({
          discussion_point1: points[0] || "논점 1",
          discussion_point2: points[1] || "논점 2",
          question1: points[2] || "질문 1",
          question2: points[3] || "질문 2",
          full_discussion: conversationHistory.length
            ? conversationHistory
                .map((entry) => `사용자: ${entry.user}\nAI: ${entry.ai}`)
                .join("\n\n")
            : "",
        });
        setLoading(false);
      })
      .catch((error) => {
        console.error("토론 논점 가져오기 실패:", error);
        setDiscussionPoints([]);
        setLoading(false);
      });
  };

  const handleOpinionSubmit = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/respond", {
        params: { title, url, opinion },
      });
      const updatedHistory = [
        ...conversationHistory,
        { user: opinion, ai: response.data.ai_response },
      ];
      setConversationHistory(updatedHistory);
      setOpinion("");

      // 🟨🟨 새로운 메시지가 추가될 때 자동 스크롤 적용 🟨🟨
      setTimeout(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
      
    } catch (error) {
      console.error("❌ AI 응답 실패:", error);
    }
  };

  useEffect(() => {
    const fullDiscussionText = conversationHistory
      .map((entry) => `사용자: ${entry.user}\nAI: ${entry.ai}`)
      .join("\n\n");
    onDiscussionData({
      discussion_point1: discussionPoints[0] || "논점 1",
      discussion_point2: discussionPoints[1] || "논점 2",
      question1: discussionPoints[2] || "질문 1",
      question2: discussionPoints[3] || "질문 2",
      full_discussion: fullDiscussionText,
    });
  }, [conversationHistory, discussionPoints, onDiscussionData]);

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
            <ListGroup.Item>
              <Badge bg="primary">논점 1</Badge> {discussionPoints[0]}
            </ListGroup.Item>
            <ListGroup.Item>
              <Badge bg="secondary">논점 2</Badge> {discussionPoints[1]}
            </ListGroup.Item>
            {discussionPoints.length > 2 && (
              <>
                <ListGroup.Item>
                  <Badge bg="info">질문 1</Badge> {discussionPoints[2]}
                </ListGroup.Item>
                <ListGroup.Item>
                  <Badge bg="success">질문 2</Badge> {discussionPoints[3]}
                </ListGroup.Item>
              </>
            )}
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
        <Card className="mt-3">
          <Card.Header>🗨️ 토론 내역</Card.Header>
          <Card.Body style={{ maxHeight: "300px", overflowY: "auto" }} className="discussion-container">
            {conversationHistory.length === 0 ? (
              <p className="text-center">아직 토론이 시작되지 않았습니다.</p>
            ) : (
              conversationHistory.map((entry, index) => (
                <div key={index} className="d-flex flex-column mb-3">
                  {/* 🟨🟨 사용자 메시지 (오른쪽 파란색 말풍선) 🟨🟨 */}
                  <div className="user-message" 
                       style={{ backgroundColor: "#0d6efd", maxWidth: "80%", borderRadius: "10px", padding: "8px" }}>
                    <strong>사용자:</strong> {entry.user}
                  </div>
                  {/* 🟨🟨 AI 메시지 (왼쪽 회색 말풍선) 🟨🟨 */}
                  <div className="ai-message" 
                       style={{ backgroundColor: "#e9ecef", maxWidth: "80%", borderRadius: "10px", padding: "8px" }}>
                    <strong>AI:</strong> {entry.ai}
                  </div>
                </div>
              ))
            )}
            <div ref={chatEndRef} /> {/* 🟨🟨 자동 스크롤 기능 추가 🟨🟨 */}
          </Card.Body>
        </Card>
      </Card.Body>
    </Card>
  );
};

export default NewsDiscussion;
