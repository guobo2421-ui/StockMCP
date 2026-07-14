import math

def success_response(**kwargs):
    return {
        "success": True,
        **kwargs
    }


def error_response(code: str, message: str):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        }
    }

def clean_value(value: Any) -> Any:

    if value is None:
        return None

    if hasattr(value, "item"):
        value = value.item()

    if isinstance(value, float) and math.isnan(value):
        return None

    return value  

def safe_divide(a, b):
    if a is None or b is None or b == 0:
        return None

    return a / b
 