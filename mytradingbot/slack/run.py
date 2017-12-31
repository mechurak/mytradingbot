from slackbot.bot import Bot
import os
import sys

# slackbot_settings.py should be located in PYTHONPATH
sys.path.append(os.path.dirname(__file__))


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
