from flask import Flask, render_template, request
from serial_py import arduino_1
from alertchan.models import ConfigData

app = Flask(__name__)


class Message(object):
    """Slackのメッセージクラス"""
    token = ""
    team_id = ""
    channel_id = ""
    channel_name = ""
    timestamp = 0
    user_id = ""
    user_name = ""
    text = ""
    trigger_word = ""

    def __init__(self, params):
        self.team_id = params["team_id"]
        self.channel_id = params["channel_id"]
        self.channel_name = params["channel_name"]
        self.timestamp = params["timestamp"]
        self.user_id = params["user_id"]
        self.user_name = params["user_name"]
        self.text = params["text"]
        self.trigger_word = params["trigger_word"]

    def __str__(self):
        res = self.__class__.__name__
        res += "@{0.token}[channel={0.channel_name}, user={0.user_name}, text={0.text}]".format(self)
        return res


@app.route('/')
def index():
    title = "Alert=Chan"
    contents = ConfigData.query.all()
    return render_template('index.html', title=title, contents=contents)


@app.route("/api/v1/get_request", methods=['POST'])
def webhook():
    msg = Message(request.form)

    print(msg)
    print(msg.user_name)

    if msg.user_name == "twitter":
        arduino_1("1")
    elif msg.user_name == "JAlert":
        arduino_1("3")
    else:
        arduino_1("2")
    return request.data

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
