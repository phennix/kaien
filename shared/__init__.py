"""Shared utilities and constants for Kaien system"""

# Shared constants
KAIEN_VERSION = "0.1.0"
DEFAULT_SERVER_URL = "http://localhost:8000"

# Tool definitions
TOOL_CATEGORIES = {
    "core": ["shell", "write_file", "read_file", "list_files"],
    "dev": ["test_code", "lint_code", "run_tests"],
    "research": ["web_search", "scrape_page", "summarize"],
    "osint": ["domain_scan", "port_scan", "whois_lookup"]
}