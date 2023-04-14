import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (userInput.trim() === "") {
      return;
    }
  
    setMessages((prevMessages) => [...prevMessages, { from: "user", text: userInput }]);
    setUserInput("");
  
    try {
      const response = await axios.post("http://localhost:8000/api/chatbot/", {
      message: userInput,
    });
      setMessages((prevMessages) => [...prevMessages, { from: "bot", text: response.data.response }]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="App">
      <h1>Chatbot</h1>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message.from === "user" ? "You" : "Bot"}: {message.text}</li>
        ))}
      </ul>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyPress={(e) => {
          if (e.key === "Enter") {
            sendMessage();
          }
        }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;

