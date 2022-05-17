from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "8a42ca4c-c0f8-11ec-91b2-00e0514217b3"

socketio = SocketIO(app)

@socketio.on("message")
def handle(msg):
    print(f"message: {msg}")
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)
