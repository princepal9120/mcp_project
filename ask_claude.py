import sys
import os
import requests
import argparse
import json
from claude_mcp_client import ClaudeMCPClient


def check_mcp_server():
    mcp_url= os.environ.get("MCP_SERVER_URL", "http://localhost:5001")
    try:
        response= requests.get(f"{mcp_url}/health", timeout=2)
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False
    
def main():

    parser =argparse.ArgumentParser(description="Ask Claude question with web search capability")
    parser.add_argument("query", nargs="*", help="The question to ask Claude")
    args= parser.parse_args()

    if not os.environ.get("CLAUDE_API_KEY"):
        print("Please set CLAUDE_API_KEY environment variable")
        sys.exit(1)

    if args.query:
        query= " ".join(args.query)
    else:
        query= input("Ask Claude: ")

    if check_mcp_server():
        client= ClaudeMCPClient()
        response= client.ask(query)
        print(response)
    else: