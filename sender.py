#!/usr/bin/env python3
"""
sender.py – pushes one file to a listening receiver.py instance
"""
import argparse
import os
import socket
import struct

PORT  = 5001
CHUNK = 4096

def send_file(ip: str, filepath: str) -> None:
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        print(f"[+] Connecting to {ip}:{PORT}")
        sock.connect((ip, PORT))

        # --- fixed-size headers ---
        sock.sendall(struct.pack("!H", len(filename)))  # name length (2 B)
        sock.sendall(filename.encode())                 # file name
        sock.sendall(struct.pack("!Q", filesize))       # file size (8 B)

        # --- stream the file ---
        sent = 0
        with open(filepath, "rb") as f:
            while chunk := f.read(CHUNK):
                sock.sendall(chunk)
                sent += len(chunk)

        print(f"[✓] Sent {filename} ({sent:,} bytes)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Send an MP3 (or any file) to a receiver on your LAN")
    ap.add_argument("ip",   help="Receiver’s LAN IP (e.g. 192.168.1.42)")
    ap.add_argument("file", help="Path to the .mp3 file to send")
    args = ap.parse_args()

    send_file(args.ip, args.file)
