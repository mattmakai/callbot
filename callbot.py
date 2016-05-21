import os
import time
import uuid
from slackclient import SlackClient
from twilio.rest import TwilioRestClient


BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">:"
CALL_COMMAND = "call"
ADD_PHONE_COMMAND = "my_number"
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
TWIMLET = "https://twimlets.com/echo?Twiml=%3CResponse%3E%0A%20%20%3CDial%3E%3CConference%3E{{name}}%3C%2FConference%3E%3C%2FDial%3E%0A%3C%2FResponse%3E&"

slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))
twilio_client = TwilioRestClient()



def handle_command(command, channel):
    response = "Not sure what you mean. Use *call* or *add_phone* commands."
    if command.startswith(CALL_COMMAND):
        response = call_command(command[len(CALL_COMMAND):].strip())
    elif command.startswith(ADD_PHONE_COMMAND):
        response = add_number_command( \
                        command[len(ADD_NUMBER_COMMAND):].strip())
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def call_command(command):
    response = "calling"
    conference_name = str(uuid.uuid4())
    phone_numbers = []
    for phone_number in phone_numbers:
        print("calling " + str(phone_number))
        twilio_client.calls.create(to=phone_number, from_=TWILIO_NUMBER,
                                   url=TWIMLET.replace('{{name}}',
                                   conference_name))
    return response


def add_number_command(command):
    response = "added your phone number!"
    return response


def parse_slack_output(slack_rtm_output):
    output = slack_rtm_output
    if output and 'text' in output[0]:
        if AT_BOT in output[0]['text']:
            # return text after the @ mention, whitespace removed
            return output[0]['text'].split(AT_BOT)[1].strip(), \
                   output[0]['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Phonebot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

