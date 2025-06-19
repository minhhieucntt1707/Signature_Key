## Signature Key File Transfer
A Python-based project to demonstrate secure file transfer using public/private key cryptography with a Flask web interface for both sender and receiver roles.

this is a project structure
Signature_key_file_transfer/
├── key_generate.py                        # Script to generate public/private key pairs
├── receiver_web/                          # Receiver web app
│   ├── app.py                             # Flask app to receive files
│   ├── public_key.pem                     # Public key used to verify signature
│   ├── received_file.bin                  # Output file received
│   ├── receiver_thread.py                 # Handles background receiving logic
│   ├── static/
│   │   ├── script.js                      # JavaScript for UI interaction
│   │   └── style.css                      # Styling for the receiver web UI
│   └── templates/
│       └── index.html                     # Web page for the receiver
├── sender_web/                            # Sender web app
│   ├── app.py                             # Flask app to send files
│   ├── private_key.pem                    # Private key used to sign files
│   ├── static/
│   │   └── style.css                      # Styling for the sender web UI
│   └── templates/
│       └── index.html                     # Web page for the sender

## How It Works
Key Generation
Run key_generate.py to generate a public/private key pair (public_key.pem and private_key.pem).

Sender Web App

Launch using python sender_web/app.py

Upload a file which will be signed using private_key.pem and sent to the receiver.

Receiver Web App

Launch using python receiver_web/app.py

Waits for incoming signed files and verifies them using public_key.pem.

## Requirements
Python 3.10+

Flask

Cryptography library (e.g., pycryptodome or cryptography)

## Security Note
Ensure that private keys (private_key.pem) are stored securely and not exposed in production environments.
