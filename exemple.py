
from understar import OS

# Ensure you have a 'plugins' folder in this directory for your custom plugins.
# The bot will automatically load:
# 1. System plugins (config, maintenance) from the library.
# 2. User plugins from your local 'plugins/' folder.

if __name__ == "__main__":
    # You can pass the token here or let the bot find it in 'data/token/bot_token'
    bot = OS() 
    bot.start()