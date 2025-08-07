import re  # For regex operations
from http.server import BaseHTTPRequestHandler, HTTPServer  # For HTTP server handling
import urllib.parse  # For parsing URLs and query strings
import json  # For JSON encoding/decoding

# Main App class for routing and server
class App:
    def __init__(self):
        # Dictionary to store routes for each HTTP method
        self.routes = {
            'GET': [],
            'POST': [],
            'PUT': [],
            'DELETE': [],
            'OPTIONS': []
        }

    # Methods to register route handlers
    def get(self, path): return self._add_route('GET', path)
    def post(self, path): return self._add_route('POST', path)
    def put(self, path): return self._add_route('PUT', path)
    def delete(self, path): return self._add_route('DELETE', path)
    def options(self, path): return self._add_route('OPTIONS', path)

    # Internal method to add route to self.routes
    def _add_route(self, method, path):
        # Find path parameters like :id => ["id"]
        param_names = re.findall(r':(\w+)', path)  #"/user/:id" → ["id"]
        # Replace path parameters with regex group matcher
        regex_path = re.sub(r':\w+', r'([^/]+)', path)  # "/user/([^/]+)"
        # Final regex to match entire URL path
        regex = f"^{regex_path}$"

        # Wrapper to bind handler function to the route
        def wrapper(handler):
            self.routes[method].append((re.compile(regex), param_names, handler))
            return handler  # return original handler
        return wrapper

    # Start the HTTP server
    def run(self, host='localhost', port=5000):
        app = self  # alias for use inside nested class

        # HTTP Request Handler class
        class Handler(BaseHTTPRequestHandler):
            # Core request handling logic for all methods
            def _handle(self, method):
                # Parse URL path and query params
                parsed_path = urllib.parse.urlparse(self.path)
                path = parsed_path.path
                query = urllib.parse.parse_qs(parsed_path.query)

                # Loop through registered routes for this method
                for regex, param_names, handler in app.routes[method]:
                    match = regex.match(path)
                    if match:
                        # If path matches, prepare params and body
                        self.query = query  # GET query params
                        self.params = dict(zip(param_names, match.groups()))  # URL params (e.g., id)
                        self.body = None
                        if method in ('POST', 'PUT', 'OPTIONS'):
                            length = int(self.headers.get('Content-Length', 0))
                            self.body = self.rfile.read(length).decode('utf-8')  # Read request body
                        return handler(self)  # Call the matched handler

                # If no route matched
                self.send_error(404, f"No {method} handler for {path}")

            # HTTP method handlers (all delegate to _handle)
            def do_GET(self): self._handle('GET')
            def do_POST(self): self._handle('POST')
            def do_PUT(self): self._handle('PUT')
            def do_DELETE(self): self._handle('DELETE')
            def do_OPTIONS(self): self._handle('OPTIONS')

            # Send response with status and JSON body
            def send(self, status, body):
                self.send_response(status)
                # CORS headers
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE ,OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                # Convert body to JSON string if not already
                if not isinstance(body, str):
                    body = json.dumps(body)
                self.wfile.write(body.encode('utf-8'))  # Write response

            # Parse JSON body from request
            def json(self):
                try:
                    return json.loads(self.body) if self.body else {}
                except json.JSONDecodeError:
                    return {}

        # Start the HTTP server with the custom Handler
        print(f"server running at http://{host}:{port}")
        try:
            HTTPServer((host, port), Handler).serve_forever()
        except KeyboardInterrupt:
            print("\nserver stopped.")
