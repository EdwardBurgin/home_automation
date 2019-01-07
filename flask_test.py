from flask import Flask
from flask_ask import Ask, statement, convert_errors

app = Flask(__name__)

ask = Ask(app, '/')

@ask.intent('temperature')

def temperature():
	x = 'The temperature is 20'
#   x = 'The temperature is %d'%read_temp()

	return statement(x)


app.run(debug=True)
