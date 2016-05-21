from flask import Flask, request, Response
from twilio.rest import TwilioRestClient
from twilio import twiml


app = Flask(__name__)
client = TwilioRestClient()


@app.route("/twilio", methods=['POST'])
def twilio():
    response = twiml.Response()
    conference_name = request.form.get('From', "Default")
    response.dial().conference(conference_name)
    return Response(response.toxml(), mimetype="text/xml"), 200


if __name__ == "__main__":
    app.run(debug=True)
