
from flask import Flask, render_template, request, redirect, flash
import socket, hashlib
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
app.secret_key = 'some_secret_key'
PORT = 45678  # Đã đổi PORT

def load_private_key(path='private_key.pem'):
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

def sign_data(data: bytes, private_key):
    signature = private_key.sign(
        hashlib.sha256(data).digest(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def send_file(ip, file_data, signature):
    with socket.create_connection((ip, PORT)) as s:
        s.sendall(len(file_data).to_bytes(4, 'big'))
        s.sendall(file_data)
        s.sendall(len(signature).to_bytes(4, 'big'))
        s.sendall(signature)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ip = request.form["ip"]
        uploaded_file = request.files["file"]
        if not ip or not uploaded_file:
            flash("Vui lòng nhập IP và chọn file.")
            return redirect("/")

        file_data = uploaded_file.read()
        try:
            private_key = load_private_key()
            signature = sign_data(file_data, private_key)
            send_file(ip, file_data, signature)
            flash("File và chữ ký đã được gửi thành công.", "success")
        except Exception as e:
            flash(f"Lỗi khi gửi file: {str(e)}", "danger")
        return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False, port=5000)
