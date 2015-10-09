from __future__ import print_function

import flask

from sr.robot import Robot


R = Robot()
app = flask.Flask(__name__)


@app.route('/pages')
def pages():
    return flask.jsonify(pages=[
        {
            'name': 'sr-camera-page',
            'title': 'Camera',
        }
    ]), 200, {'Access-Control-Allow-Origin': '*'}


app.run(port=10000)
