"""
Main Dashboard for DevDash
Beautiful terminal UI using Rich
"""

import time
from datetime import datetime
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.align import Align
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .git_utils import GitInfo
from .system_utils import SystemInfo
from .port_utils import PortScanner
from .package_utils import PackageInfo


class DevDash:
    """Main DevDash Dashboard"""
    
    VERSION = "1.0.0"
    
    def __init__(self, path: str = "."):
        if not RICH_AVAILABLE:
            print("Error: 'rich' library required. Install: pip install rich")
            return
        
        self.console = Console()
        self.path = path
        self.git = GitInfo(path)
        self.running = False
    
    def create_header(self) -> Panel:
        """Create dashboard header"""
        header_text = Text()
        header_text.append("⚡ ", style="bold yellow")
        header_text.append("DEVDASH", style="bold cyan")
        header_text.append(" v" + self.VERSION, style="dim")
        header_text.append(" │ ", style="dim")
        header_text.append(datetime.now().strftime("%H:%M:%S"), style="green")
        header_text.append(" │ ", style="dim")
        header_text.append("Developer Dashboard", style="italic dim")
        
        return Panel(
            Align.center(header_text),
            style="cyan",
            box=box.DOUBLE
        )
    
    def create_git_panel(self) -> Panel:
        """Create git information panel"""
        git_info = Table(show_header=False, box=None, padding=(0, 1))
        git_info.add_column("Key", style="dim")
        git_info.add_column("Value", style="bold")
        
        if self.git.is_git_repo:
            branch = self.git.get_branch()
            status = self.git.get_status()
            last_commit = self.git.get_last_commit()
            uncommitted = self.git.get_uncommitted_count()
            today_commits = self.git.get_today_commits()
            
            branch_display = f"[cyan]{branch}[/cyan]"
            if uncommitted > 0:
                branch_display += f" [yellow]({uncommitted} changes)[/yellow]"
            
            git_info.add_row("📁 Project", f"[bold white]{self.git.get_repo_name()}[/bold white]")
            git_info.add_row("🌿 Branch", branch_display)
            git_info.add_row("📝 Last Commit", f"[dim]{last_commit['message']}[/dim]")
            git_info.add_row("⏰ Committed", f"[green]{last_commit['time']}[/green]")
            git_info.add_row("👤 Author", f"{last_commit['author']}")
            git_info.add_row("📊 Today", f"[cyan]{today_commits}[/cyan] commits")
            
            if status['modified'] > 0:
                git_info.add_row("✏️  Modified", f"[yellow]{status['modified']}[/yellow] files")
            if status['untracked'] > 0:
                git_info.add_row("❓ Untracked", f"[red]{status['untracked']}[/red] files")
            
            stash = self.git.get_stash_count()
            if stash > 0:
                git_info.add_row("📦 Stashed", f"[magenta]{stash}[/magenta]")
        else:
            git_info.add_row("⚠️  Status", "[yellow]Not a git repository[/yellow]")
        
        return Panel(
            git_info,
            title="[bold cyan]📂 GIT STATUS[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        )
    
    def create_system_panel(self) -> Panel:
        """Create system information panel"""
        sys_info = Table(show_header=False, box=None, padding=(0, 1))
        sys_info.add_column("Key", style="dim")
        sys_info.add_column("Value")
        
        cpu = SystemInfo.get_cpu_percent()
        mem = SystemInfo.get_memory_info()
        disk = SystemInfo.get_disk_info()
        os_info = SystemInfo.get_os_info()
        uptime = SystemInfo.get_uptime()
        
        cpu_color = "green" if cpu < 50 else "yellow" if cpu < 80 else "red"
        mem_color = "green" if mem['percent'] < 50 else "yellow" if mem['percent'] < 80 else "red"
        disk_color = "green" if disk['percent'] < 70 else "yellow" if disk['percent'] < 90 else "red"
        
        sys_info.add_row("💻 OS", f"{os_info['system']} {os_info['release']}")
        sys_info.add_row("🐍 Python", f"v{os_info['python']}")
        sys_info.add_row("⏱️  Uptime", uptime)
        sys_info.add_row("", "")
        sys_info.add_row("🔥 CPU", f"[{cpu_color}]{cpu:.1f}%[/{cpu_color}]")
        sys_info.add_row("🧠 RAM", f"[{mem_color}]{mem['percent']:.1f}%[/{mem_color}] ({mem['used']:.1f}GB / {mem['total']:.1f}GB)")
        sys_info.add_row("💾 Disk", f"[{disk_color}]{disk['percent']:.1f}%[/{disk_color}] ({disk['free']:.0f}GB free)")
        
        processes = SystemInfo.get_process_count()
        sys_info.add_row("⚙️  Processes", f"{processes}")
        
        battery = SystemInfo.get_battery_info()
        if battery:
            bat_color = "green" if battery['percent'] > 50 else "yellow" if battery['percent'] > 20 else "red"
            bat_status = "🔌" if battery['plugged'] else "🔋"
            sys_info.add_row(f"{bat_status} Battery", f"[{bat_color}]{battery['percent']}%[/{bat_color}]")
        
        return Panel(
            sys_info,
            title="[bold green]🖥️  SYSTEM[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
    
    def create_ports_panel(self) -> Panel:
        """Create ports information panel"""
        ports_table = Table(show_header=True, box=box.SIMPLE, padding=(0, 1))
        ports_table.add_column("Port", style="cyan", justify="right")
        ports_table.add_column("", width=2)
        ports_table.add_column("Service", style="white")
        ports_table.add_column("Process", style="dim")
        
        ports = PortScanner.get_listening_ports()
        
        if ports:
            for p in ports[:8]:
                ports_table.add_row(
                    str(p['port']),
                    p['icon'],
                    p['service'],
                    p['process'][:15]
                )
        else:
            ports_table.add_row("-", "", "No active ports", "")
        
        return Panel(
            ports_table,
            title="[bold yellow]🌐 PORTS[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED
        )
    
    def create_packages_panel(self) -> Panel:
        """Create packages information panel"""
        pkg_table = Table(show_header=True, box=box.SIMPLE, padding=(0, 1))
        pkg_table.add_column("Package", style="white")
        pkg_table.add_column("Current", style="red")
        pkg_table.add_column("Latest", style="green")
        
        project_type = PackageInfo.detect_project_type(self.path)
        
        if project_type:
            outdated = PackageInfo.get_outdated_packages(self.path)
            
            if outdated:
                for pkg in outdated[:5]:
                    pkg_table.add_row(
                        pkg['name'][:20],
                        pkg['current'],
                        pkg['latest']
                    )
            else:
                pkg_table.add_row("✅", "All packages", "up to date")
        else:
            pkg_table.add_row("-", "No package", "manager found")
        
        return Panel(
            pkg_table,
            title="[bold magenta]📦 PACKAGES[/bold magenta]",
            border_style="magenta",
            box=box.ROUNDED
        )
    
    def create_stats_panel(self) -> Panel:
        """Create today's coding stats panel"""
        stats_table = Table(show_header=False, box=None, padding=(0, 1))
        stats_table.add_column("Key", style="dim")
        stats_table.add_column("Value", style="bold")
        
        if self.git.is_git_repo:
            today_stats = self.git.get_today_stats()
            today_commits = self.git.get_today_commits()
            
            stats_table.add_row("📊 Commits Today", f"[cyan]{today_commits}[/cyan]")
            stats_table.add_row("➕ Lines Added", f"[green]+{today_stats['added']}[/green]")
            stats_table.add_row("➖ Lines Removed", f"[red]-{today_stats['removed']}[/red]")
            
            branches = len(self.git.get_branches())
            stats_table.add_row("🌿 Branches", f"{branches}")
        else:
            stats_table.add_row("📊 Stats", "[dim]No git repo[/dim]")
        
        return Panel(
            stats_table,
            title="[bold blue]📈 TODAY[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        )
    
    def create_help_panel(self) -> Panel:
        """Create help/shortcuts panel"""
        help_text = Text()
        help_text.append("  [Q]", style="bold cyan")
        help_text.append(" Quit  ", style="dim")
        help_text.append("[R]", style="bold cyan")
        help_text.append(" Refresh  ", style="dim")
        help_text.append("[G]", style="bold cyan")
        help_text.append(" Git  ", style="dim")
        help_text.append("[P]", style="bold cyan")
        help_text.append(" Ports  ", style="dim")
        help_text.append("[S]", style="bold cyan")
        help_text.append(" System  ", style="dim")
        
        return Panel(
            Align.center(help_text),
            style="dim",
            box=box.SIMPLE
        )
    
    def create_layout(self) -> Layout:
        """Create the main layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right", ratio=1)
        )
        
        layout["left"].split_column(
            Layout(name="git", ratio=1),
            Layout(name="stats", ratio=1)
        )
        
        layout["right"].split_column(
            Layout(name="system", ratio=1),
            Layout(name="bottom_right", ratio=1)
        )
        
        layout["bottom_right"].split_row(
            Layout(name="ports", ratio=1),
            Layout(name="packages", ratio=1)
        )
        
        return layout
    
    def update_layout(self, layout: Layout) -> None:
        """Update layout with current data"""
        layout["header"].update(self.create_header())
        layout["git"].update(self.create_git_panel())
        layout["system"].update(self.create_system_panel())
        layout["ports"].update(self.create_ports_panel())
        layout["packages"].update(self.create_packages_panel())
        layout["stats"].update(self.create_stats_panel())
        layout["footer"].update(self.create_help_panel())
    
    def run(self, refresh_rate: float = 2.0) -> None:
        """Run the dashboard"""
        if not RICH_AVAILABLE:
            return
        
        self.running = True
        layout = self.create_layout()
        
        try:
            with Live(layout, console=self.console, refresh_per_second=1, screen=True) as live:
                while self.running:
                    self.update_layout(layout)
                    live.update(layout)
                    time.sleep(refresh_rate)
        except KeyboardInterrupt:
            self.running = False
    
    def show_once(self) -> None:
        """Show dashboard once without live updates"""
        if not RICH_AVAILABLE:
            return
        
        layout = self.create_layout()
        self.update_layout(layout)
        self.console.print(layout)
    
    def show_git(self) -> None:
        """Show only git information"""
        if not RICH_AVAILABLE:
            return
        self.console.print(self.create_git_panel())
    
    def show_system(self) -> None:
        """Show only system information"""
        if not RICH_AVAILABLE:
            return
        self.console.print(self.create_system_panel())
    
    def show_ports(self) -> None:
        """Show only ports information"""
        if not RICH_AVAILABLE:
            return
        self.console.print(self.create_ports_panel())
    
    def show_packages(self) -> None:
        """Show only packages information"""
        if not RICH_AVAILABLE:
            return
        self.console.print(self.create_packages_panel())
