# Customer Support Chatbot

A scalable, user-friendly chatbot designed to enhance customer service by providing instant, accurate, and context-aware responses. The chatbot automates common customer queries, escalates complex issues to human agents, and supports 24/7 service. It leverages the GitHub Models API (`openai/gpt-4o`) for natural language processing and intent detection.

## Features
- **Automated Responses**: Handles common queries like greetings, order status, returns, and technical issues.
- **Escalation**: Seamlessly escalates complex issues (e.g., urgent or legal matters) to human agents.
- **User-Friendly Interface**: Clean chat interface with quick reply buttons for common queries.
- **Real-Time Communication**: Uses WebSocket for instant message exchange between the frontend and backend.
- **Scalable Backend**: Built with FastAPI for high performance and scalability.

## Project Structure
- `chatbot_app.py`: Backend server using FastAPI, handling WebSocket communication and API calls to GitHub Models.
- `index.html`: Frontend interface built with HTML, Tailwind CSS, and JavaScript, providing a chat UI with quick reply buttons.
- `.env`: Environment file for storing the GitHub token (not included in version control).

## Prerequisites
- **Python 3.8+**: For running the backend.
- **GitHub Token**: Required for accessing the GitHub Models API (`https://models.github.ai/inference`).
- **Node.js**: Optional, for testing WebSocket connections with tools like `wscat`.

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install fastapi uvicorn openai python-dotenv websockets
```

### 4. Configure Environment Variables
Create a `.env` file in the project root and add your GitHub token:
```
GITHUB_TOKEN=your-github-token-here
```
- Generate a token at [GitHub Settings](https://github.com/settings/tokens) with appropriate scopes for GitHub Models.
- Ensure `.env` is added to `.gitignore` to avoid exposing your token.

### 5. Run the Backend
Start the FastAPI server:
```bash
uvicorn chatbot_app:app --reload
```
The server will run at `http://localhost:8000`. The `--reload` flag enables auto-reload for development.

### 6. Serve the Frontend
Serve the `index.html` file to access the chat interface:
- **Using Python HTTP Server**:
  ```bash
  python -m http.server 8080
  ```
  Open `http://localhost:8080/index.html` in a browser.
- **Using VSCode Live Server**:
  - Install the Live Server extension in VSCode.
  - Right-click `index.html` and select `Open with Live Server` (typically opens at `http://127.0.0.1:5500/index.html`).

## Usage
1. Open the frontend URL in a browser.
2. The chat starts with a bot message: "Hello! I'm here to assist you. How may I help you today?"
3. Use the quick reply buttons ("Track Order", "Returns", "Product Info", "Shipping") to send predefined messages.
4. Type custom messages in the input field and press Enter or click the send button.
5. For complex queries (e.g., "urgent complaint"), the bot will escalate to a human agent.

### Example Messages
- **Greeting**: "Hello", "Hi there"
- **Order Status**: "Track my order", "Where is my order?"
- **Returns**: "I want to return an item", "How do I get a refund?"
- **Technical Issue**: "My device isn't working", "I'm getting an error"
- **Escalation**: "This is urgent!", "I have a legal issue"

## Troubleshooting
- **Backend Fails to Start**:
  - Ensure all dependencies are installed (`pip list` to verify).
  - Check `.env` for a valid `GITHUB_TOKEN`.
  - Verify the GitHub Models API is accessible (`https://models.github.ai/inference`).
- **Frontend Doesn't Receive Responses**:
  - Confirm the backend is running (`http://localhost:8000`).
  - Check the browser console (`F12` > "Console") for WebSocket errors.
  - Ensure the frontend is served via an HTTP server to avoid CORS issues.
- **WebSocket Errors**:
  - Install WebSocket support if missing: `pip install websockets`.
  - Test the WebSocket endpoint with `wscat`:
    ```bash
    npm install -g wscat
    wscat -c ws://localhost:8000/ws/chat
    # Send: {"message": "Hello"}
    ```

## Future Improvements
- Add a database to store chat history and feedback.
- Implement user authentication for personalized experiences.
- Enhance the frontend with more interactive elements (e.g., typing indicators).
- Fine-tune the `openai/gpt-4o` model with domain-specific data for better intent detection.

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [FastAPI](https://fastapi.tiangolo.com/) and [Tailwind CSS](https://tailwindcss.com/).
- Powered by [GitHub Models](https://github.com/features/models) (`openai/gpt-4o`).
