#!/usr/bin/env python3
"""
receiver.py – waits for a single file and saves it under ./received
"""
import os
import socket
import struct

HOST = ""          # empty string = listen on all local interfaces
PORT = 5001        # change if you like, but keep sender & receiver in sync
CHUNK = 4096       # bytes per network read

def main() -> None:
    os.makedirs("received", exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind((HOST, PORT))
        srv.listen(1)
        print(f"[+] Listening on 0.0.0.0:{PORT}")

        conn, addr = srv.accept()
        with conn:
            print(f"[+] Connection from {addr[0]}:{addr[1]}")

            # --- fixed-size headers ---
            name_len = struct.unpack("!H", conn.recv(2))[0]      # 2 bytes
            filename  = conn.recv(name_len).decode()
            filesize  = struct.unpack("!Q", conn.recv(8))[0]     # 8 bytes

            print(f"[+] Receiving {filename} ({filesize:,} bytes)")
            path = os.path.join("received", filename)

            # --- stream the file ---
            received = 0
            with open(path, "wb") as f:
                while received < filesize:
                    chunk = conn.recv(min(CHUNK, filesize - received))
                    if not chunk:
                        raise ConnectionError("Sender closed unexpectedly")
                    f.write(chunk)
                    received += len(chunk)

            print(f"[✓] Saved to {path}")

if __name__ == "__main__":
    main()
