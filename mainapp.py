from flask import Flask, request, send_file
from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler
from os import environ
from gevent.pywsgi import WSGIServer
from incrementor import Noob, Blob

uid = Noob()
t0 = Blob()
t1 = Blob()
app = Flask(__name__)
websocket = Sockets(app)


@websocket.route('/echo')
def echo(ws):
    user = int(request.cookies.get('id'))
    wshash = 0
    while True:
        msg = ws.receive()
        if msg:
            if user == 0:
                t0.set_data(msg)
        if user != 0 and wshash != hash(t0):
            ws.send(t0.get_data())
            wshash = hash(t0)


@app.route('/')
def hi():
    resp = send_file("static/Recording.html")
    resp.set_cookie('id', str(uid.val))
    uid.increment()
    return resp


if __name__ == '__main__':
    http_server = WSGIServer(('', int(environ.get('PORT'))), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
