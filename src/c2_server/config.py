"""C2 Server Configuration"""
import os, json

class C2Config:
    def __init__(self):
        self.listen_host = os.getenv("C2_HOST", "0.0.0.0")
        self.listen_port = int(os.getenv("C2_PORT", "4443"))
        self.protocol = os.getenv("C2_PROTO", "https")
        self.encryption_key = os.getenv("C2_KEY", "")
        self.heartbeat_interval = 30
        self.max_agents = 100
        self.log_level = "INFO"
        self.db_path = "c2_data.db"
        self.ssl_cert = "certs/server.pem"
        self.ssl_key = "certs/server.key"
        self.jitter = 0.3
        self.user_agent = "Mozilla/5.0"
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}
    
    @classmethod
    def from_file(cls, path):
        cfg = cls()
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
                for k, v in data.items():
                    setattr(cfg, k, v)
        return cfg
