
from flask import Flask, render_template, jsonify
import threading
from receiver_thread import start_server, log_buffer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def get_logs():
    return jsonify(log_buffer)

def run_receiver():
    threading.Thread(target=start_server, daemon=True).start()

if __name__ == "__main__":
    run_receiver()
    app.run(debug=False, port=5001)
