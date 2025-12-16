
from .core.kernel import Kernel
import asyncio

class OS:
    def __init__(self, token: str = None):
        self.kernel = Kernel()
        self.token = token

    def start(self, token: str = None):
        if token:
            self.token = token
            
        if not self.token:
            raise ValueError("Token is required to start the bot.")
            
        try:
            asyncio.run(self.kernel.start(self.token))
        except KeyboardInterrupt:
            pass
