import os
import requests
import json
import time
from typing import Dict, List, Optional, Any


CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/api/v1/messages"
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:5001")


class ClaudeMCPClient:
    def __init__(self, api_key=CLAUDE_API_KEY, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model
        self.headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        self.tools = [
            {
                "name": "fetch_web_content",
                "description": "Retrieves infrom from website based on user queries",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to be used to search the website",
                        }
                    },
                    "required": ["query"],
                },
            }
        ]
        self._check_mcp_server()

    def _check_mcp_server(self):
        try:
            response = requests.get(f"{MCP_SERVER_URL}/health", timeout=2)
            if response.status_code == 200:
                return True
            return False
        except requests.exceptions.RequestException:
            pass
        return False

    def send_message(
        self, message: str, conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("API key is needed!")

        if conversation_history is None:
            conversation_history = []

        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": conversation_history + [{"role": "user", "content": message}],
            "tools": self.tools,
        }
        print("Sending request to claude", payload)
        try:
            response= requests.post(
                CLAUDE_API_URL,
                headers=self.headers,
                json=payload,
            )
            if response.status_code != 200:
                print(response.json)
                raise Exception(f"Error {response.status_code}: {response.json()}")
            
            response.raise_for_status()

            result= response.json()
            print(f"Claude results: {result}")

            has_tool_call=False
            tool_call ={}
            if "content" in result:
                for content_block
                