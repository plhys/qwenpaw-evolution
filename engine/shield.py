import ast
import logging

logger = logging.getLogger("qwenpaw.DreamEngine.Shield")

class SecurityShield:
    """A Loose, Power-user focused Safety Layer for AI-generated code."""
    
    # We only block EXTREMELY destructive patterns.
    # Focus on cross-platform extreme system-level danger.
    EXTREME_DANGER = [
        "os.system('rm -rf /')", 
        "shutil.rmtree('/')",
        "os.system('format C:')",
        "os.system('del /F /S /Q')"
    ]

    @classmethod
    def audit_code(cls, code_content: str) -> (bool, str):
        """
        Statically audit the AI-generated code.
        Focus on extreme safety issues while leaving 99% of functionality open.
        """
        try:
            # Check for the most extreme text patterns first
            for pattern in cls.EXTREME_DANGER:
                if pattern in code_content:
                    return False, f"Detected extreme system-level danger: {pattern}"

            # Ensure the code is valid Python
            ast.parse(code_content)
            
            return True, "Code passed basic sanity check. AI is free to execute."
            
        except SyntaxError as e:
            return False, f"Syntax error in generated code: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error during audit: {str(e)}"
