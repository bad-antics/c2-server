#!/usr/bin/env python3
"""C2 Server - Basic Usage"""
from c2_server.config import C2Config
from c2_server.core import C2Server

config = C2Config()
config.listen_port = 4443

server = C2Server(config)
server.start()

# List agents
agents = server.list_agents()
print(f"Active agents: {len(agents)}")

# Task an agent
# server.task_agent("agent_id", "shell", {"cmd": "whoami"})
