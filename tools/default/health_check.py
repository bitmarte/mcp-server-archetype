from mcp_core.core import core_api

@core_api.mcp.tool
def health_check() -> dict:
    """Ritorna lo stato del server MCP."""
    core_api.logger.info("Eseguo health_check")
    return {"status": "ok"}