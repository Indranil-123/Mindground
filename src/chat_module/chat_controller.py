from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
import joblib
import os

# Load your trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "mental_health_model.pkl")

# Load the churn model
model = joblib.load(MODEL_PATH)

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Mental Health Chatbot</title>
    </head>
    <body>
        <h1>Mental Health WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/interact");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""


@router.get("/chat")
async def get():
    return HTMLResponse(html)


@router.websocket("/interact")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("🧠 Hello! How can I help you today?")
    while True:
        try:
            data = await websocket.receive_text()
            prediction = model.predict([data])[0]
            bot_response = generate_response(data, prediction)

            await websocket.send_text(f"👤 You: {data}")
            await websocket.send_text(f"🤖 Bot: {bot_response}")
            await websocket.send_text(f"📊 Predicted Mental Condition: {prediction}")

        except Exception as e:
            await websocket.send_text("❌ Error: Could not process the message.")
            break


def generate_response(message: str, condition: str) -> str:
    if condition == "Anxiety":
        return "It seems like you're feeling anxious. Try taking deep breaths and slowing down."
    elif condition == "Depression":
        return "You're not alone. Talking to someone or seeking help can make a difference."
    elif condition == "Suicidal":
        return "This sounds serious. Please reach out to a suicide prevention hotline or professional help immediately."
    elif condition == "Bipolar":
        return "Your message indicates mood shifts. Consider monitoring this with a healthcare provider."
    else:
        return "Glad to hear you're feeling okay. Let me know if something’s bothering you."
