import os
import sys
import re
import subprocess
import logging
from importlib.metadata import version, PackageNotFoundError

logger = logging.getLogger("qwenpaw.DreamEngine.DepManager")

class DependencyManager:
    """Modernized automatic dependency resolver (v6.3.1)."""
    
    @staticmethod
    def resolve_dependencies(python_code: str) -> (bool, str):
        """Scan imports and install missing packages automatically using modern importlib."""
        imports = DependencyManager._extract_imports(python_code)
        missing = []
        
        for pkg in imports:
            if not DependencyManager._is_installed(pkg):
                missing.append(pkg)
        
        if not missing:
            return True, "All dependencies present."
            
        logger.info(f"Missing dependencies found: {missing}. Executing auto-install...")
        
        try:
            # Atomic subprocess call for pip install with timeout
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing, timeout=60)
            return True, f"Successfully installed: {missing}"
        except Exception as e:
            return False, f"Dependency installation failed: {str(e)}"

    @staticmethod
    def _extract_imports(code: str):
        # Optimized regex for import detection
        pattern = r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)"
        matches = re.findall(pattern, code, re.MULTILINE)
        return list(set(matches))

    @staticmethod
    def _is_installed(package_name: str):
        """Check availability using importlib.metadata (modern replacement for pkg_resources)."""
        # 1. Check built-ins
        if package_name in sys.modules or package_name in sys.builtin_module_names:
            return True
        # 2. Check installed packages
        try:
            version(package_name)
            return True
        except PackageNotFoundError:
            return False
