from typing import Any, Dict

def format_response(success: bool, message: str, data: Any = None) -> Dict[str, Any]:
    return {
        "success": success,
        "message": message,
        "data": data
    }
