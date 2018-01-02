# slackbot_settings.py should be located in PYTHONPATH

from slackbot.bot import Bot
import logging
logger = logging.getLogger("MyLogger")


def main():
    logger.info("start slack_bot")
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
