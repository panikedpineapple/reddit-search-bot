import os

# The prefix that will be used to parse commands.
# It doesn't have to be a single character!
COMMAND_PREFIX = "!"

# The bot token. Keep this secret!
BOT_TOKEN = "ODI2MDgyMzE0MjYxMjMzNjk0.YGHTGw.kYvZg5vVhpPneAFyxZFUrcAAeVQ"

# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = COMMAND_PREFIX + "commands"

# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Reddit search endpoint
REDDIT_ENDPOINT = 'https://www.reddit.com'

#number of results to show
LIMIT = '10'