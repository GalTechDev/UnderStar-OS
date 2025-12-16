
# UnderStar-OS V2

A modular and robust Python library for building advanced Discord bots.

## Installation

```bash
pip install understar
```

## Usage

Create a file `main.py`:

```python
from understar import OS

if __name__ == "__main__":
    bot = OS()
    bot.start() # Reads token from data/token/bot_token
    # Or: bot.start("YOUR_TOKEN")
```

## Docker

```bash
docker run -d -v $(pwd)/data:/app/data -v $(pwd)/plugins:/app/plugins galtechdev/understar
```
