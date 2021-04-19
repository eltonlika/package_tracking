import argparse

__parser__ = argparse.ArgumentParser()
__parser__.add_argument('--telegram-bot-token', required=True)
__args__ = __parser__.parse_args()

TELEGRAM_BOT_TOKEN = __args__.telegram_bot_token
