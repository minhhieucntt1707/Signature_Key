
import socket, threading, hashlib
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime

PORT = 45678
log_buffer = []

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    log_buffer.append(entry)
    if len(log_buffer) > 100:
        log_buffer.pop(0)

def load_public_key(path='public_key.pem'):
    with open(path, "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read(), backend=default_backend())

def verify_signature(data: bytes, signature: bytes, public_key):
    try:
        public_key.verify(
            signature,
            hashlib.sha256(data).digest(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

def handle_client(conn, addr):
    log(f"Kết nối từ {addr}")
    try:
        data_len_bytes = conn.recv(4)
        if len(data_len_bytes) < 4:
            log("Lỗi: Không đủ kích thước file")
            return
        data_len = int.from_bytes(data_len_bytes, 'big')
        file_data = b''
        while len(file_data) < data_len:
            file_data += conn.recv(min(4096, data_len - len(file_data)))

        sig_len_bytes = conn.recv(4)
        if len(sig_len_bytes) < 4:
            log("Lỗi: Không đủ kích thước chữ ký")
            return
        sig_len = int.from_bytes(sig_len_bytes, 'big')
        signature = b''
        while len(signature) < sig_len:
            signature += conn.recv(min(4096, sig_len - len(signature)))

        public_key = load_public_key()
        if verify_signature(file_data, signature, public_key):
            with open("received_file.bin", "wb") as f:
                f.write(file_data)
            log("✔ Chữ ký hợp lệ. Đã lưu file.")
        else:
            log("✘ Chữ ký không hợp lệ. Từ chối file.")
    except Exception as e:
        log(f"Lỗi xử lý: {str(e)}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('0.0.0.0', PORT))
        server.listen(5)
        log(f"🟢 Server lắng nghe cổng {PORT}...")
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except Exception as e:
        log(f"Lỗi khởi động server: {e}")
