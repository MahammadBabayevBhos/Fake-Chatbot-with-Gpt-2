# server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import os
import json
from model_runner import get_falcon_response  # GPT-2 cavab funksiyası

BASE_DIR = "C:/Users/Lenovo/Desktop/HTTP_project"
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(TEMPLATE_DIR, "index.html"), "rb") as file:
                self.wfile.write(file.read())
        elif self.path.startswith("/static/"):
            file_name = self.path.split("/static/")[1]
            file_path = os.path.join(STATIC_DIR, file_name)

            if os.path.exists(file_path):
                if file_path.endswith(".css"):
                    self.send_response(200)
                    self.send_header("Content-type", "text/css; charset=utf-8")
                elif file_path.endswith(".js"):
                    self.send_response(200)
                    self.send_header("Content-type", "application/javascript")
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "application/octet-stream")

                self.end_headers()
                with open(file_path, "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File not found.")
        else:
            self.send_error(404, "Page not found.")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        data = urllib.parse.parse_qs(post_data)
        message = data.get("message", [""])[0]

        response_text = get_falcon_response(message)

        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        response = {"reply": response_text}
        self.wfile.write(json.dumps(response).encode("utf-8"))

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server started at: http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
