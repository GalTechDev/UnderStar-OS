<div align="center">

# 🚀 UnderStar-OS

**A modular, strictly-typed Python framework for Discord bots**

[![PyPI](https://img.shields.io/pypi/v/understar?style=flat-square&color=6366f1)](https://pypi.org/project/understar/)
[![Docker](https://img.shields.io/docker/v/galteck/understar-os?style=flat-square&label=docker&color=2496ed)](https://hub.docker.com/r/galteck/understar-os)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

[Documentation](https://galtechdev.github.io/UnderStar-OS/) • [PyPI](https://pypi.org/project/understar/) • [Docker Hub](https://hub.docker.com/r/galteck/understar-os)

</div>

---

## ✨ Features

- **🧩 Modular Plugin System** — Split your features into isolated plugins
- **⚡ Event Bus** — Decoupled communication between plugins
- **💾 Smart Persistence** — Built-in JSON storage (global, per-guild, per-user)
- **🔧 Slash Commands** — Easy decorator-based command creation
- **📦 Easy Installation** — Available on PyPI and Docker Hub

---

## 📦 Installation

### PyPI
```bash
pip install understar
```

### Docker
```bash
docker pull galteck/understar-os
```

---

## 🚀 Quick Start

Create a file `main.py`:

```python
from understar import OS

if __name__ == "__main__":
    bot = OS()
    bot.start()  # Token will be requested on first launch
```

Run it:
```bash
python main.py
```

---

## 🧩 Create a Plugin

```python
from understar.core.plugin import Plugin, slash_command

class HelloPlugin(Plugin):
    @slash_command(name="hello", description="Say hello!")
    async def hello(self, interaction):
        await interaction.response.send_message("Hello World! 🌌")

    async def on_load(self):
        self.logger.info("Plugin loaded!")
```

Place it in `plugins/hello/__init__.py` and it will be auto-loaded.

---

## 🐳 Docker Usage

```bash
docker run -d \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/plugins:/app/plugins \
  galteck/understar-os
```

---

## 📁 Project Structure

```
my-bot/
├── main.py
├── plugins/
│   └── my_plugin/
│       └── __init__.py
└── data/
    ├── token/
    └── storage/
```

---

## 📚 Documentation

Full documentation available at: **[galtechdev.github.io/UnderStar-OS](https://galtechdev.github.io/UnderStar-OS/)**

---

## 📄 License

MIT License © 2025 GalTechDev
