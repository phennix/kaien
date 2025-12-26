"""Kaien Web Client - Flask interface"""

from flask import Flask, render_template, request, jsonify
import httpx
import json

app = Flask(__name__)

# Configuration
SERVER_URL = "http://localhost:8000"

@app.route('/')
def home():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/tools')
def get_tools():
    """Get available tools from Kaien Nexus"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{SERVER_URL}/api/v1/tools")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/execute', methods=['POST'])
def execute_tool():
    """Execute a tool via Kaien Nexus"""
    try:
        data = request.json
        tool = data.get('tool')
        args = data.get('args', {})
        
        with httpx.Client() as client:
            response = client.post(
                f"{SERVER_URL}/api/v1/execute",
                json={"tool": tool, "args": args}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health():
    """Check Kaien Nexus health"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{SERVER_URL}/health")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        message = data.get('message', '')
        
        # For now, simple echo response
        # In Phase 2, this will connect to the LLM router
        response_message = f"Received: {message}"
        
        return jsonify({
            "status": "success",
            "response": response_message,
            "source": "echo"  # Will be "llm" in Phase 2
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)