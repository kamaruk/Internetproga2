import json
import os
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader


with open(os.path.join('data', 'product.json'), 'r', encoding='utf-8') as f:
    product_data = json.load(f)

env = Environment(loader=FileSystemLoader('patterns'))

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path.startswith('/static/'):
            self.handle_static_file(path)
            return

        if path == '/':
            template = env.get_template('index.html')
            content = template.render()
        elif path == '/about':
            template = env.get_template('about.html')
            content = template.render()
        elif path == '/products':
            template = env.get_template('products.html')
            content = template.render(products=product_data)
        elif path == '/contact':
            template = env.get_template('contact.html')
            content = template.render()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Page not found')
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))


    def do_POST(self):
        if self.path == '/Smessage':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            name = data.get('name', [None])[0]
            email = data.get('email', [None])[0]
            message = data.get('message', [None])[0]

            if not name:
                self.send_response(400)
                self.end_headers()
                self.wfile.write('Ошибка: Имя обязательно к заполнению.'.encode('utf-8'))
                return
            if not email or not email.strip():
                self.send_response(400)
                self.end_headers()
                self.wfile.write('Ошибка: Электронная почта обязательна.'.encode('utf-8'))
                return
            if not message:
                self.send_response(400)
                self.end_headers()
                self.wfile.write('Ошибка: Сообщение обязательно к заполнению.'.encode('utf-8'))
                return

            print(f'Получено сообщение от ({email}): {message}')
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('Сообщение отправлено!'.encode('utf-8'))


    def handle_static_file(self, path):
        filename = path.split('/', 2)[-1]
        file_path = os.path.join('static', filename)

        if os.path.exists(file_path):
            self.send_response(200)
            if filename.endswith('.css'):
                self.send_header('Content-Type', 'text/css; charset=utf-8')
            else:
                self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')



def run(server_class=HTTPServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, RequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()