import base64
from flask import Flask
import datetime
from util import *

def str_format():
    t = datetime.datetime.now().time()
    return "The time is %d:%d and the temperature is...  %.3f degrees"%(t.hour, t.minute, read_temp())

def web_page(im_tag):
    page = """

    <html>
    <head>
    <style>
    body {
            color: red;
    }
    </style>
    <body bgcolor="#000000">
        <head>
            <title>Temperature Plot</title>
        </head>
        <body>
            <h1>""" + str_format() + """ </h1> 
            """ + im_tag + """

        </body>
    </html>


    """
    return page


app = Flask(__name__)

@app.route('/')
def hello_world():
    data_uri = base64.b64encode(open('graph.png', 'rb').read()).decode('utf-8').replace('\n', '')
    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
    return web_page(img_tag) #str_format()

app.run(host='0.0.0.0', port=8080)
