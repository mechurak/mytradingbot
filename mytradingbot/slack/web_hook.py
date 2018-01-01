import requests

from mytradingbot.keys import slack_hook_url


def send_to_slack(the_payload):
    requests.post(slack_hook_url, json=the_payload)


if __name__ == "__main__":
    payload = {
        "text": "Test message.\ntest test"
    }
    send_to_slack(payload)
