#!/usr/bin/env python3

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


FILES = {"/example.txt": b"This is a sample file.\n"}


class FileHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        content = FILES.get(path)
        if content is None:
            self.send_error(404, "File not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        path = urlsplit(self.path).path

        if path == "/":
            self.send_error(400, "Specify a filename, such as /notes.txt")
            return

        try:
            length = int(self.headers.get("Content-Length", ""))
            if length < 0:
                raise ValueError
        except ValueError:
            self.send_error(400, "A valid Content-Length is required")
            return

        content = self.rfile.read(length)
        if len(content) != length:
            self.send_error(400, "Incomplete upload")
            return

        created = path not in FILES
        FILES[path] = content

        self.send_response(201 if created else 200)
        self.send_header("Location", path)
        self.send_header("Content-Length", "0")
        self.end_headers()



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), FileHandler)
    print(f"Server running at http://127.0.0.1:{args.port}", flush=True)
    print("Sample file: /example.txt | Stop with Ctrl+C", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
