"""
CLI interface for DevDash
"""

import sys

try:
    import typer
    from typing_extensions import Annotated
    TYPER_AVAILABLE = True
except ImportError:
    TYPER_AVAILABLE = False

from . import __version__
from .dashboard import DevDash
from .git_utils import GitInfo
from .system_utils import SystemInfo
from .port_utils import PortScanner

if TYPER_AVAILABLE:
    app = typer.Typer(
        name="devdash",
        help="⚡ DevDash - Developer Dashboard CLI",
        add_completion=False,
        rich_markup_mode="rich"
    )
else:
    app = None


def check_dependencies():
    """Check and install missing dependencies"""
    missing = []
    
    try:
        import rich
    except ImportError:
        missing.append("rich")
    
    try:
        import typer
    except ImportError:
        missing.append("typer")
    
    try:
        import psutil
    except ImportError:
        missing.append("psutil")
    
    if missing:
        print(f"Installing dependencies: {', '.join(missing)}")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing + ["-q"])
        print("Dependencies installed! Please run the command again.")
        sys.exit(0)


if TYPER_AVAILABLE:
    @app.command()
    def dashboard(
        path: Annotated[str, typer.Option("--path", "-p", help="Project path")] = ".",
        once: Annotated[bool, typer.Option("--once", "-1", help="Show once without live updates")] = False,
        refresh: Annotated[float, typer.Option("--refresh", "-r", help="Refresh rate in seconds")] = 2.0
    ):
        """
        ⚡ Launch the main developer dashboard
        
        Shows git status, system info, ports, and packages in a beautiful TUI.
        """
        check_dependencies()
        dash = DevDash(path)
        
        if once:
            dash.show_once()
        else:
            dash.run(refresh_rate=refresh)


    @app.command()
    def git(
        path: Annotated[str, typer.Option("--path", "-p", help="Repository path")] = "."
    ):
        """
        📂 Show git repository status
        """
        check_dependencies()
        dash = DevDash(path)
        dash.show_git()


    @app.command()
    def system():
        """
        🖥️  Show system information
        """
        check_dependencies()
        dash = DevDash()
        dash.show_system()


    @app.command()
    def ports():
        """
        🌐 Show listening ports and services
        """
        check_dependencies()
        dash = DevDash()
        dash.show_ports()


    @app.command()
    def packages(
        path: Annotated[str, typer.Option("--path", "-p", help="Project path")] = "."
    ):
        """
        📦 Show outdated packages
        """
        check_dependencies()
        dash = DevDash(path)
        dash.show_packages()


    @app.command()
    def info():
        """
        ℹ️  Show quick system info (one-liner)
        """
        check_dependencies()
        
        from rich.console import Console
        from rich.text import Text
        
        console = Console()
        
        cpu = SystemInfo.get_cpu_percent()
        mem = SystemInfo.get_memory_info()
        os_info = SystemInfo.get_os_info()
        port_count = len(PortScanner.get_listening_ports())
        
        info_text = Text()
        info_text.append("⚡ ", style="yellow")
        info_text.append(f"{os_info['system']} ", style="cyan")
        info_text.append("│ ", style="dim")
        info_text.append(f"CPU: {cpu:.0f}% ", style="green" if cpu < 50 else "yellow")
        info_text.append("│ ", style="dim")
        info_text.append(f"RAM: {mem['percent']:.0f}% ", style="green" if mem['percent'] < 50 else "yellow")
        info_text.append("│ ", style="dim")
        info_text.append(f"Ports: {port_count} ", style="blue")
        info_text.append("│ ", style="dim")
        info_text.append(f"Python: {os_info['python']}", style="dim")
        
        console.print(info_text)


    @app.command()
    def version():
        """
        Show DevDash version
        """
        from rich.console import Console
        from rich.text import Text
        
        console = Console()
        text = Text()
        text.append("⚡ DevDash ", style="bold cyan")
        text.append(f"v{__version__}", style="green")
        text.append(" by ", style="dim")
        text.append("DAXXTEAM", style="bold magenta")
        console.print(text)


def main():
    """Main entry point"""
    if not TYPER_AVAILABLE:
        check_dependencies()
        print("Dependencies installed. Please run again.")
        return
    
    app()


if __name__ == "__main__":
    main()
