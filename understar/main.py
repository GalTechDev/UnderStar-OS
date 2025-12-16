
import asyncio
import os
import sys
from core.kernel import kernel

async def main():
    # Load Token
    token_path = os.path.join("data", "token", "bot_token")
    if not os.path.exists(token_path):
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, "w") as f:
            f.write("PUT_TOKEN_HERE")
        print(f"Token file created at {token_path}. Please insert your bot token.")
        return

    with open(token_path, "r") as f:
        token = f.read().strip()
    
    if token == "PUT_TOKEN_HERE":
        print("Please configure your bot token.")
        return

    await kernel.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping Bot...")
