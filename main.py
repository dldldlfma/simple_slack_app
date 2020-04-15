import json
import os
from slack import WebClient
from slack.errors import SlackApiError
from pprint import pprint

from flask import Flask, request, make_response


app = Flask(__name__)

client = WebClient(token="token_value")
verification_token = os.environ['SLACK_VERIFICATION_TOKEN']

def event_handler(event_type, slack_event):
    if event_type =="app_mention":
        try:
            client.chat_postMessage(channel="#random", text = slack_event["event"]['text'])
            return make_response("send message", 200, {"X-Slack-No-Retry":1})
        except:
            return make_response("슬랙 요청에 이벤트가 없습니다.", 404, {"X-Slack-No-Retry":1})
    
@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello World!"


@app.route("/slack", methods=["GET", "POST"])
def slack_hears():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("슬랙 요청에 이벤트가 없습니다.", 404, {"X-Slack-No-Retry":1})

if __name__ == "__main__":
    app.run('0.0.0.0', port=8080)


    