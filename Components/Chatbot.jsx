import axios from "axios";
import React, { useEffect, useState } from "react";

const Chatbot = () => {
  const [message, setMessage] = useState("");
  const [chatResponse, setChatResponse] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  // ✅ Initialize session ID once
  useEffect(() => {
    const id = localStorage.getItem("session_id") || crypto.randomUUID();
    localStorage.setItem("session_id", id);
    setSessionId(id);
  }, []);

  // ✅ Load chat history after session ID is set
  useEffect(() => {
    if (sessionId) {
      axios
        .get(`http://localhost:5000/api/history/${sessionId}`)
        .then((res) => setChatHistory(res.data.chat_history))
        .catch((err) => console.error("Error loading chat history:", err));
    }
  }, [sessionId]);

  // ✅ Handle input field changes
  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  // ✅ Handle Enter key press
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  // ✅ Send message to backend
  const sendMessage = async () => {
    if (!message.trim()) return;
    try {
      const res = await axios.post("http://localhost:5000/api/chat", {
        session_id: sessionId,
        message,
      });

      // Update chat history locally
      setChatHistory((prev) => [
        ...prev,
        { sender: "You", message },
        { sender: "Bot", message: res.data.response },
      ]);

      setMessage(""); // Clear input
      setChatResponse(""); // No need for separate response state anymore
    } catch (error) {
      console.error("Chat API error:", error);
      setChatHistory((prev) => [
        ...prev,
        { sender: "You", message },
        { sender: "Bot", message: "Something went wrong. Please try again." },
      ]);
      setMessage("");
    }
  };

  return (
    <div className="chatbot-container">
      <div className="header">
        <div className="bot-icon">🤖</div>
        <h2>Gemini Chat</h2>
      </div>
      <div className="chat-history-container">
        {chatHistory.map((chat, index) => (
          <div
            key={index}
            className={chat.sender === "You" ? "user-message" : "bot-message"}
          >
            {chat.message}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          className="input-field"
          value={message}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Send message..."
        />
        <button className="send-button" onClick={sendMessage}>
          <span role="img" aria-label="send">
            ➡️
          </span>
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
