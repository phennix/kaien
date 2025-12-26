#!/usr/bin/env python3
"""Verify Kaien system components are working"""

import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'modules'))

def test_imports():
    """Test that all components can be imported"""
    print("Testing imports...")
    
    try:
        # Test server imports
        from server.main import app
        from server.api import router
        from server.state import state
        from server.config import config
        from server.schemas import ToolDefinition
        from server.database import KaienDatabase
        from server.mcp_client import MCPClient
        from server.agent_client import AgentClient
        from server.tools.shell_agent import shell_agent
        from server.tools.dev_agent import dev_agent
        
        # Test module imports
        from modules.mcp_client import MCPClient as ModuleMCPClient
        
        print("✓ All imports successful")
        return True
        
    except Exception as e:
        print(f"✗ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration"""
    print("Testing configuration...")
    
    try:
        from server.config import config
        
        # Test basic config
        assert config.get("host") == "0.0.0.0"
        assert config.get("port") == 8000
        
        # Test modules config
        modules = config.get("modules", {})
        assert isinstance(modules, dict)
        
        print("✓ Configuration test passed")
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {str(e)}")
        return False


def test_database():
    """Test database operations"""
    print("Testing database...")
    
    try:
        from server.database import KaienDatabase
        
        # Create test database
        test_db = KaienDatabase("test_verify.db")
        
        # Test tool operations
        test_db.register_tool("test_tool", "Test tool", {"param": "value"})
        tools = test_db.get_tools()
        assert len(tools) > 0
        
        # Test session operations
        test_db.log_session("test_session", "Hello", "World")
        history = test_db.get_session_history("test_session")
        assert len(history) == 1
        
        # Test state operations
        test_db.set_state("test_key", "test_value")
        value = test_db.get_state("test_key")
        assert value == "test_value"
        
        # Cleanup
        os.remove("test_verify.db")
        
        print("✓ Database test passed")
        return True
        
    except Exception as e:
        print(f"✗ Database test failed: {str(e)}")
        if os.path.exists("test_verify.db"):
            os.remove("test_verify.db")
        return False


def test_schemas():
    """Test Pydantic schemas"""
    print("Testing schemas...")
    
    try:
        from server.schemas import ToolDefinition, SessionMessage, ToolRequest
        
        # Test ToolDefinition
        tool = ToolDefinition(
            name="test_tool",
            description="Test tool",
            parameters={"param": {"type": "string"}}
        )
        assert tool.name == "test_tool"
        
        # Test SessionMessage
        message = SessionMessage(
            session_id="test_session",
            message="Test message"
        )
        assert message.session_id == "test_session"
        
        # Test ToolRequest
        request = ToolRequest(
            tool="test_tool",
            args={"param": "value"}
        )
        assert request.tool == "test_tool"
        
        print("✓ Schema test passed")
        return True
        
    except Exception as e:
        print(f"✗ Schema test failed: {str(e)}")
        return False


def test_state():
    """Test state management"""
    print("Testing state management...")
    
    try:
        from server.state import state
        from server.schemas import ToolDefinition
        
        # Test tool registration
        tool = ToolDefinition(
            name="verify_tool",
            description="Verification tool",
            parameters={"action": {"type": "string"}}
        )
        state.register_tool(tool)
        assert "verify_tool" in state.tools
        
        # Test session management
        state.create_session("verify_session")
        assert "verify_session" in state.active_sessions
        
        # Test message logging
        state.log_message("verify_session", "Test user", "Test assistant")
        session = state.get_session("verify_session")
        assert len(session["history"]) == 1
        
        print("✓ State management test passed")
        return True
        
    except Exception as e:
        print(f"✗ State management test failed: {str(e)}")
        return False


def main():
    """Run verification tests"""
    print("=" * 60)
    print("Kaien System Verification")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_schemas,
        test_database,
        test_state
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {str(e)}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✓ All verification tests passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())