from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
import base64


USERNAME = "user"
PASSWORD = "pass"

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.authenticate():
            self.send_auth_request()
            return

        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/':
            self.send_static_response('index.html')
        elif parsed_path.path == '/dynamic':
            self.send_dynamic_response()
        else:
            self.send_error(404, 'File Not Found')

    def do_POST(self):
        if not self.authenticate():
            self.send_auth_request()
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Received POST request!</h1><p>Data: " + post_data + b"</p></body></html>")

    def do_DELETE(self):
        if not self.authenticate():
            self.send_auth_request()
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>DELETE request received!</h1></body></html>")

    def do_PUT(self):
        if not self.authenticate():
            self.send_auth_request()
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>PUT request received!</h1></body></html>")

    def send_static_response(self, filename):
        try:
            with open(os.path.join(os.getcwd(), filename), 'rb') as file:
                content = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File Not Found')

    def send_dynamic_response(self):
        response_content = b'<html><body><h1>Dynamic Content</h1></body></html>'
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response_content)

    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header:
           
            auth_data = auth_header.split(' ')[1]
            
            decoded_auth_data = base64.b64decode(auth_data).decode('utf-8')
            
            username, password = decoded_auth_data.split(':')
            return username == USERNAME and password == PASSWORD
        return False

    def send_auth_request(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Secure Area"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<!DOCTYPE html><html><body><h1>Authentication Required</h1></body></html>")

def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
