import platform
import subprocess
import sys
import os
import urllib.request
import tempfile
import shutil
from pathlib import Path

def install_java(java_version="11", install_path=None, verbose=False):
    """
    Automatically installs Java on the current system if not already installed.
    
    This function detects the operating system and architecture, checks if Java
    is already available in the system PATH, and if not, downloads and installs
    the appropriate Java distribution (AdoptOpenJDK by default).
    
    Parameters:
    -----------
    java_version : str, optional
        Java version to install (default: "11"). Common values: "8", "11", "17".
    install_path : str, optional
        Custom installation directory. If None, uses system default locations:
        - Windows: %ProgramFiles%\\Java
        - macOS: /Library/Java/JavaVirtualMachines
        - Linux: /usr/lib/jvm
    verbose : bool, optional
        If True, prints detailed installation progress information.
    
    Returns:
    --------
    tuple (bool, str)
        - success: True if Java is available or was successfully installed
        - message: Status message describing the outcome
    
    Raises:
    -------
    RuntimeError
        If the operating system is not supported or installation fails.
    PermissionError
        If the script lacks permissions to install Java.
    
    Examples:
    ---------
    >>> success, message = install_java(java_version="11")
    >>> if success:
    >>>     print(f"Java is ready: {message}")
    >>> else:
    >>>     print(f"Installation failed: {message}")
    
    Notes:
    ------
    - On Linux/macOS, may require sudo privileges for system-wide installation.
    - Uses AdoptOpenJDK distributions which are open-source and freely available.
    - The function first checks if 'java' and 'javac' are already in PATH.
    """
    
    def log(message):
        """Helper function for verbose logging."""
        if verbose:
            print(f"[Java Installer] {message}")
    
    def check_java_installed():
        """Check if Java is already installed and available in PATH."""
        try:
            # Check for java runtime
            result = subprocess.run(["java", "-version"], 
                                  capture_output=True, text=True, timeout=5)
            # Check for java compiler
            compiler_result = subprocess.run(["javac", "-version"], 
                                           capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0 and compiler_result.returncode == 0:
                return True, f"Java is already installed: {result.stderr.split('\\n')[0]}"
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return False, "Java not found in PATH"
    
    # First, check if Java is already installed
    log("Checking if Java is already installed...")
    is_installed, message = check_java_installed()
    if is_installed:
        return True, message
    
    # Get system information
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    log(f"Detected system: {system}, architecture: {machine}")
    
    # Map architecture names to download names
    arch_map = {
        "x86_64": "x64",
        "amd64": "x64",
        "x64": "x64",
        "i386": "x86",
        "i686": "x86",
        "x86": "x86",
        "arm64": "aarch64",
        "aarch64": "aarch64",
        "arm": "arm"
    }
    
    architecture = arch_map.get(machine, "x64")
    
    # Define OS-specific installation methods
    installers = {
        "windows": _install_windows,
        "darwin": _install_macos,
        "linux": _install_linux
    }
    
    if system not in installers:
        raise RuntimeError(f"Unsupported operating system: {system}")
    
    try:
        # Call OS-specific installer
        success, message = installers[system](java_version, architecture, install_path, verbose)
        return success, message
    except PermissionError:
        error_msg = (
            "Permission denied. Installation may require administrator/root privileges.\n"
            f"On Linux/macOS, try running with sudo.\n"
            f"On Windows, run as Administrator."
        )
        raise PermissionError(error_msg)
    except Exception as e:
        raise RuntimeError(f"Java installation failed: {str(e)}")


def _install_windows(java_version, architecture, install_path, verbose):
    """Windows-specific Java installation."""
    
    # Default installation path for Windows
    if install_path is None:
        program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        install_path = os.path.join(program_files, "Java")
    
    log = lambda msg: verbose and print(f"[Windows Installer] {msg}")
    log(f"Installing Java {java_version} to {install_path}")
    
    # For Windows, we would typically download an MSI or EXE installer
    # This is a simplified example - in production, you'd want to:
    # 1. Download the AdoptOpenJDK MSI/EXE
    # 2. Execute it with silent install parameters
    # 3. Update PATH environment variable
    
    # Example download URL pattern (AdoptOpenJDK)
    # url = f"https://github.com/adoptium/temurin{java_version}-binaries/releases/download/..."
    
    # For now, we'll provide instructions
    message = (
        "Windows automatic installation requires downloading and running an installer.\n"
        f"Please download Java {java_version} from:\n"
        "https://adoptium.net/temurin/releases/\n"
        f"Or install manually via Chocolatey: choco install temurin{java_version}"
    )
    
    return False, message


def _install_macos(java_version, architecture, install_path, verbose):
    """macOS-specific Java installation."""
    
    # Default installation path for macOS
    if install_path is None:
        install_path = "/Library/Java/JavaVirtualMachines"
    
    log = lambda msg: verbose and print(f"[macOS Installer] {msg}")
    log(f"Installing Java {java_version} to {install_path}")
    
    try:
        # Try using Homebrew (most common on macOS)
        log("Attempting installation via Homebrew...")
        
        # Check if Homebrew is installed
        brew_check = subprocess.run(["which", "brew"], 
                                   capture_output=True, text=True)
        
        if brew_check.returncode == 0:
            # Install Java using Homebrew
            formula = f"temurin{java_version}"
            log(f"Installing {formula} via Homebrew...")
            
            install_cmd = ["brew", "install", "--cask", formula]
            result = subprocess.run(install_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, f"Successfully installed Java {java_version} via Homebrew"
            else:
                log(f"Homebrew installation failed: {result.stderr}")
        
        # Alternative: Provide manual instructions
        message = (
            f"Java {java_version} not installed.\n"
            "Installation options:\n"
            "1. Install Homebrew, then run: brew install --cask temurin{java_version}\n"
            "2. Download from: https://adoptium.net/temurin/releases/\n"
            "3. Use SDKMAN: sdk install java {java_version}.0.0-tem"
        )
        
        return False, message
        
    except Exception as e:
        return False, f"macOS installation error: {str(e)}"


def _install_linux(java_version, architecture, install_path, verbose):
    """Linux-specific Java installation."""
    
    # Default installation path for Linux
    if install_path is None:
        install_path = "/usr/lib/jvm"
    
    log = lambda msg: verbose and print(f"[Linux Installer] {msg}")
    log(f"Installing Java {java_version} to {install_path}")
    
    try:
        # Detect package manager
        pkg_managers = {
            "apt": ["apt-get", "update", "&&", "apt-get", "install", "-y"],
            "yum": ["yum", "install", "-y"],
            "dnf": ["dnf", "install", "-y"],
            "zypper": ["zypper", "install", "-y"],
            "pacman": ["pacman", "-S", "--noconfirm"]
        }
        
        # Try to detect which package manager is available
        pkg_cmd = None
        java_package = None
        
        for manager, cmd_base in pkg_managers.items():
            check = subprocess.run(["which", manager], 
                                 capture_output=True, text=True)
            if check.returncode == 0:
                pkg_cmd = cmd_base
                
                # Determine package name based on distribution
                if manager in ["apt", "dnf"]:
                    java_package = f"openjdk-{java_version}-jdk"
                elif manager in ["yum", "zypper"]:
                    java_package = f"java-{java_version}-openjdk-devel"
                elif manager == "pacman":
                    java_package = f"jdk{java_version}-openjdk"
                
                break
        
        if pkg_cmd and java_package:
            log(f"Using package manager: {pkg_cmd[0]}")
            log(f"Installing package: {java_package}")
            
            # Build the full command
            if pkg_cmd[0] == "apt-get":
                # Update package lists first
                update_cmd = ["apt-get", "update"]
                subprocess.run(update_cmd, capture_output=True, text=True)
            
            # Install Java
            install_cmd = pkg_cmd + [java_package]
            result = subprocess.run(install_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Set Java alternatives if on Debian/Ubuntu
                if pkg_cmd[0] == "apt-get":
                    try:
                        alt_cmd = ["update-alternatives", "--config", "java"]
                        subprocess.run(alt_cmd, input=f"{java_version}\\n", 
                                     capture_output=True, text=True)
                    except:
                        pass  # Alternative setting is optional
                
                return True, f"Successfully installed {java_package} via {pkg_cmd[0]}"
        
        # If no package manager found or installation failed
        message = (
            f"Java {java_version} not installed.\n"
            "Installation options:\n"
            "1. Install manually via your package manager\n"
            "2. Download from: https://adoptium.net/temurin/releases/\n"
            "3. Use SDKMAN: sdk install java {java_version}.0.0-tem\n\n"
            "Note: System-wide installation may require sudo privileges."
        )
        
        return False, message
        
    except PermissionError:
        raise  # Re-raise permission errors
    except Exception as e:
        return False, f"Linux installation error: {str(e)}"


def verify_java_installation():
    """
    Verifies that Java is properly installed and returns version information.
    
    Returns:
    --------
    dict or None
        Dictionary containing Java installation details, or None if not installed.
        Keys: 'runtime_version', 'compiler_version', 'home' (if available)
    """
    try:
        # Get Java runtime version
        runtime_result = subprocess.run(["java", "-version"], 
                                       capture_output=True, text=True, timeout=5)
        
        # Get Java compiler version
        compiler_result = subprocess.run(["javac", "-version"], 
                                        capture_output=True, text=True, timeout=5)
        
        # Try to get JAVA_HOME
        java_home = os.environ.get("JAVA_HOME", "")
        
        if runtime_result.returncode == 0 and compiler_result.returncode == 0:
            # Parse version info (first line of stderr for java -version)
            runtime_info = runtime_result.stderr.split('\\n')[0]
            compiler_info = compiler_result.stdout or compiler_result.stderr
            
            return {
                'runtime_version': runtime_info,
                'compiler_version': compiler_info.strip(),
                'home': java_home,
                'available': True
            }
    except:
        pass
    
    return None


def basicinst(ver: str = "25"):
    '''
    # BASIC JAVA INSTALLATION
    '''
    # Example 1: Basic installation check
    print("=" * 60)
    print("Java Automatic Installer")
    print("=" * 60, end='\n\n')
    
    # First, check current Java status
    java_info = verify_java_installation()
    if java_info:
        print(f"✓  Java is already installed:")
        print(f"   Runtime: \n{java_info['runtime_version']}")
        print(f"   Compiler: {java_info['compiler_version']}")
        if java_info['home']:
            print(f"   JAVA_HOME: {java_info['home']}")
    else:
        print("✗  Java is not installed or not in PATH")
    
    print("\n" + "=" * 60)
    
    print("\nAttempting Java installation...")
    try:
        # Try to install Java 25 with verbose output
        success, message = install_java(
            java_version=ver,
            verbose=True
        )
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
            print("\nManual installation may be required.")
            
    except Exception as e:
        print(f"Installation error: {e}")
    
    print("\n" + "=" * 60)
    
    # Example 3: Platform-specific information
    print("\nSystem Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python: {platform.python_version()}")

# Installation
if __name__ == "__main__":
    basicinst()