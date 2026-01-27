# ⚡ DevDash - Developer Dashboard CLI

<div align="center">

![DevDash Banner](https://img.shields.io/badge/DevDash-Developer%20Dashboard-cyan?style=for-the-badge&logo=python)

[![PyPI version](https://badge.fury.io/py/devdash-cli.svg)](https://pypi.org/project/devdash-cli/)
[![Python](https://img.shields.io/pypi/pyversions/devdash-cli.svg)](https://pypi.org/project/devdash-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/devdash-cli)](https://pepy.tech/project/devdash-cli)

**Beautiful terminal dashboard for developers - Git status, system info, ports & packages in one view!**

[Installation](#-installation) •
[Usage](#-usage) •
[Features](#-features) •
[Screenshots](#-screenshots) •
[Contributing](#-contributing)

</div>

---

## 🎯 What is DevDash?

DevDash is a beautiful, real-time terminal dashboard that shows everything a developer needs:

- 📂 **Git Status** - Branch, commits, changes, stashes
- 🖥️ **System Info** - CPU, RAM, Disk, Battery
- 🌐 **Active Ports** - What's running on which port
- 📦 **Package Updates** - Outdated npm/pip packages
- 📈 **Coding Stats** - Today's commits, lines added/removed

All in one beautiful TUI (Terminal User Interface)!

---

## 📦 Installation

```bash
pip install devdash-cli
```

That's it! Now run:

```bash
devdash
```

---

## 🚀 Usage

### Main Dashboard (Live Updates)

```bash
devdash
```

This launches the full dashboard with auto-refresh every 2 seconds.

### One-time View

```bash
devdash dashboard --once
```

### Individual Commands

```bash
# Git status only
devdash git

# System info only
devdash system

# Active ports only
devdash ports

# Outdated packages only
devdash packages

# Quick one-liner info
devdash info

# Version
devdash version
```

### Options

```bash
# Custom refresh rate (in seconds)
devdash dashboard --refresh 5

# Different project path
devdash dashboard --path /path/to/project

# Show once without live updates
devdash dashboard --once
```

---

## ✨ Features

### 📂 Git Information
- Current branch with change indicator
- Last commit message and time
- Modified, added, deleted, untracked files count
- Stash count
- Today's commit count
- Lines added/removed today

### 🖥️ System Monitoring
- OS and Python version
- CPU usage with color indicators
- RAM usage (used/total)
- Disk usage and free space
- System uptime
- Process count
- Battery status (if available)

### 🌐 Port Scanner
- All listening ports
- Process name for each port
- Service identification (Node, Python, PostgreSQL, etc.)
- Process icons for quick identification

### 📦 Package Manager
- Detects project type (npm, pip, etc.)
- Lists outdated packages
- Shows current vs latest version
- Top 5 packages needing updates

---

## 📸 Screenshots

```
╔══════════════════════════════════════════════════════════════════════════╗
║                    ⚡ DEVDASH v1.0.0 │ 14:32:05 │ Developer Dashboard    ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  ╭─────────── 📂 GIT STATUS ───────────╮  ╭─────── 🖥️  SYSTEM ────────╮  ║
║  │ 📁 Project    my-awesome-project    │  │ 💻 OS      Linux 6.1      │  ║
║  │ 🌿 Branch     main (3 changes)      │  │ 🐍 Python  v3.11.4        │  ║
║  │ 📝 Last       "feat: add feature"   │  │ ⏱️  Uptime  2d 5h 23m      │  ║
║  │ ⏰ Committed  2 hours ago           │  │                           │  ║
║  │ 👤 Author     DAXXTEAM              │  │ 🔥 CPU     23.5%          │  ║
║  │ 📊 Today      5 commits             │  │ 🧠 RAM     45.2% (8/16GB) │  ║
║  │ ✏️  Modified   3 files               │  │ 💾 Disk    67.3% (120GB)  │  ║
║  ╰─────────────────────────────────────╯  ╰───────────────────────────╯  ║
║                                                                          ║
║  ╭─────────── 📈 TODAY ────────────────╮  ╭──── 🌐 PORTS ──── 📦 PKG ─╮  ║
║  │ 📊 Commits Today   5                │  │ 3000 ⬢ Node    │ express │  ║
║  │ ➕ Lines Added     +234             │  │ 5000 🐍 Flask   │ 4.18→19 │  ║
║  │ ➖ Lines Removed   -45              │  │ 5432 🐘 Postgres│ react   │  ║
║  │ 🌿 Branches        3                │  │ 6379 🔴 Redis  │ 18.2→19 │  ║
║  ╰─────────────────────────────────────╯  ╰───────────────────────────╯  ║
║                                                                          ║
║           [Q] Quit  [R] Refresh  [G] Git  [P] Ports  [S] System          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🛠️ Requirements

- Python 3.8+
- Git (for git features)
- Works on: Linux, macOS, Windows

### Dependencies (auto-installed)

- `rich` - Beautiful terminal UI
- `typer` - CLI framework
- `psutil` - System information

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**DAXXTEAM**

- GitHub: [@DAXXTEAM](https://github.com/DAXXTEAM)
- Portfolio: [portfolio.vclub.tech](https://portfolio.vclub.tech)
- LinkedIn: [Arpit Singh](https://linkedin.com/in/arpit-singh-168a7b2a1)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

Made with ❤️ by DAXXTEAM

**⚡ DevDash - Because developers deserve beautiful tools!**

</div>
