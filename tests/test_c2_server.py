import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from c2_server.config import C2Config
from c2_server.core import Agent, TaskQueue, C2Server
from c2_server.crypto import C2Crypto

class TestC2Config(unittest.TestCase):
    def test_defaults(self):
        cfg = C2Config()
        self.assertEqual(cfg.listen_port, 4443)
        self.assertEqual(cfg.protocol, "https")
        self.assertEqual(cfg.max_agents, 100)

class TestAgent(unittest.TestCase):
    def test_creation(self):
        a = Agent("abc123", ("127.0.0.1", 1234))
        self.assertEqual(a.id, "abc123")
        self.assertTrue(a.alive)

class TestTaskQueue(unittest.TestCase):
    def test_add_get(self):
        q = TaskQueue()
        tid = q.add_task("agent1", "shell", {"cmd": "whoami"})
        tasks = q.get_tasks("agent1")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["type"], "shell")

class TestCrypto(unittest.TestCase):
    def test_encrypt_decrypt(self):
        c = C2Crypto()
        ct = c.encrypt("secret message")
        pt = c.decrypt(ct)
        self.assertEqual(pt, b"secret message")

if __name__ == "__main__":
    unittest.main()
