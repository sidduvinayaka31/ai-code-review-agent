import ast
import javalang

def validate_python(code: str) -> tuple[bool, str]:
    """Validates Python code syntax."""
    if not code.strip():
        return False, "Code is empty."
    try:
        ast.parse(code)
        return True, "Valid Python syntax."
    except SyntaxError as e:
        return False, f"Syntax Error: {e.msg} at line {e.lineno}, offset {e.offset}"
    except Exception as e:
        return False, f"Error validating Python code: {str(e)}"

def validate_java(code: str) -> tuple[bool, str]:
    """Validates Java code syntax."""
    if not code.strip():
        return False, "Code is empty."
    try:
        javalang.parse.parse(code)
        return True, "Valid Java syntax."
    except javalang.parser.JavaSyntaxError as e:
        return False, f"Syntax Error: {str(e)}"
    except Exception as e:
        # Fallback for simple classless snippets if needed, but javalang expects valid CompilationUnits
        if "CompilationUnit" in str(e):
            return False, "Syntax Error: Java code must be a valid CompilationUnit (e.g., inside a class)."
        return False, f"Error validating Java code: {str(e)}"

def validate_code(code: str, language: str) -> tuple[bool, str]:
    """Route validation based on language."""
    if language.lower() == 'python':
        return validate_python(code)
    elif language.lower() == 'java':
        return validate_java(code)
    else:
        return False, f"Unsupported language: {language}"
